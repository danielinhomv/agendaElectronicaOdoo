from odoo import models, fields, api
from ..utils.cloudinary_helper import CloudinaryHelper
from datetime import date
from odoo.exceptions import ValidationError

class alumno(models.Model):
    _name = "administracion_academica.alumno"
    _description = "Relacion de los alumnos del colegio"

    nombre = fields.Char(string="Nombre del alumno", required=True)
    apellidos = fields.Char(string="Apellidos", required=True)
    fecha_nacimiento = fields.Date(string="Fecha de nacimiento")
    carnet_identidad = fields.Char(string="Canet de identidad", required=True)
    correo_electronico = fields.Char(string="Email", required=True)
    direccion = fields.Char(string="Dirección")
    edad = fields.Integer(string="Edad", compute="_compute_edad", readonly=True)
    foto = fields.Image(string="Foto")
    foto_url = fields.Char(string="URL de la foto")
    genero = fields.Selection(
        [
            ("Masculino", "Masculino"),
            ("Femenino", "Femenino"),
            ("Otro", "Otro"),
        ],
        string="Sexo",
        required=True,
        default="Masculino",
    )
    # varios alumnos pertenecen a un alumno (muchos a uno)
    apoderado = fields.Many2one(
        "administracion_academica.apoderado", string="Nombre del apoderado"
    )
    # varios mensualidades pertenecen a un alumno (uno a muchos)
    mensualidades = fields.One2many(
        "administracion_academica.mensualidad",
        inverse_name="alumno",
        string="Mensualidad",
    )

    # mensualidades_alumno = fields.Many2many(
    #     "administracion_academica.mensualidad",
    #     string="Mensualidad",
    # )

    # un alumno puede inscribirse en varios cursos a lo largo del tiempo ( uno a muchos) 
    inscripciones = fields.One2many(
        'administracion_academica.inscripcion', 
        'alumno_id', 
        string="Inscripciones")
    
    # relacion muchos a muchos con cursos
    cursos = fields.Many2many(
        'administracion_academica.curso', 
        compute='_compute_cursos', 
        string="Cursos")

    calificaciones = fields.One2many(
        'administracion_academica.calificacion', 
        inverse_name="alumno_id",
        string="Calificaciones")
    
    alumno_comunicados = fields.One2many(
        'administracion_academica.alumno_comunicado', 
        inverse_name="alumno_id",
        string="Comunicados para el alumno"
    )

    comunicados = fields.Many2many(
        "administracion_academica.comunicado",
        compute = "_compute_comunicados",
        string= "Comunicados"       
    )

    asistencias = fields.One2many(
        "administracion_academica.asistencia",
        inverse_name = "alumno_id",
        string = "Asistencias"
    )

    clases = fields.Many2many(
        "administracion_academica.clase",
        compute = "_compute_clase",
        string = "Clases"
    )

    user_id = fields.Many2one("res.users", 
    string="Usuario relacionado", 
    ondelete="cascade")

    _sql_constraints = [
        (
            "correo_electronico_uniq",
            "unique(correo_electronico)",
            "El correo electrónico debe ser único.",
        ),
        (
            "carnet_identidad_uniq",
            "unique(carnet_identidad)",
            "El carnet de identidad debe ser único. Ingresa otro carnet de identidad.",
        )
    ]

    @api.constrains("nombre", "apellidos")
    def _check_names(self):
        for record in self:
            if not record.nombre:
                raise ValidationError("El nombre es requerido")
            if not record.apellidos:
                raise ValidationError("El apellido es requerido")
            
    @api.depends("fecha_nacimiento")
    def _compute_edad(self):
        today = date.today()
        for record in self:
            if record.fecha_nacimiento:
                birthdate = record.fecha_nacimiento
                age = (
                    today.year
                    - birthdate.year
                    - ((today.month, today.day) < (birthdate.month, birthdate.day))
                )
                record.edad = age
            else:
                record.edad = 0

    @api.depends('inscripciones')
    def _compute_cursos(self):
        for alumno in self:
            alumno.cursos = alumno.inscripciones.mapped('curso_id')

    @api.depends('alumno_comunicados')
    def _compute_comunicados(self):
        for alumno in self:
            alumno.comunicados = alumno.alumno_comunicados.mapped('comunicado_id')

    @api.depends('asistencias')
    def _compute_clase(self):
        for alumno in self:
            alumno.clases = alumno.asistencias.mapped('clase_id')

    @api.model
    def create(self, values):
        user_vals = {
            'name': f"{values['nombre']} {values['apellidos']}",
            'login': values['correo_electronico'],
            'password': values.get('carnet_identidad'),  # Usar carnet de identidad como contraseña
            'email': values['correo_electronico'],
        }      
        user = self.env['res.users'].create(user_vals)
        if not user:
            raise ValidationError("Error al crear el usuario del alumno.")
         # Asignar el usuario creado al apoderado
        values['user_id'] = user.id

        return super(alumno, self).create(values)

    def write(self, vals):
        if vals.get("foto"):
            if self.foto_url:
                # Eliminar la imagen de Cloudinary
                CloudinaryHelper.delete_image(self.foto_url)
            # Subir la imagen a Cloudinary
            vals["foto_url"] = CloudinaryHelper.upload_image(vals["foto"])
        elif "foto" in vals and not vals.get("foto"):
            if self.foto_url:
                # Eliminar la imagen de Cloudinary
                CloudinaryHelper.delete_image(self.foto_url)
            # Establecer foto_url en null
            vals["foto_url"] = None
        return super(alumno, self).write(vals)

    def unlink(self):
        for rec in self:
            # Eliminar la imagen de Cloudinary si existe
            if rec.foto_url:
                CloudinaryHelper.delete_image(rec.foto_url)
        return super(alumno, self).unlink()

    @api.depends("nombre", "apellidos")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                f"{rec.nombre} {rec.apellidos}"
            )
            
