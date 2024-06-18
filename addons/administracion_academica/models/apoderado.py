from odoo import models, fields, api
from odoo.exceptions import ValidationError


class apoderado(models.Model):
    _name = "administracion_academica.apoderado"
    _description = "Apoderados del alumno"

    nombre = fields.Char(string="Nombre", required=True)
    apellidos = fields.Char(string="Apellidos", required=True)
    carnet_identidad = fields.Char(string="Canet de identidad", required=True)
    correo_electronico = fields.Char(string="Email", required=True)
    telefono = fields.Char(string="Telefono")
    direccion = fields.Char(string="Dirección")
    # un apoderado es responsable de varios alumnos(uno a muchos)
    alumno = fields.One2many(
        "administracion_academica.alumno", inverse_name="apoderado", string="Alumno"
    )

    user_id = fields.Many2one("res.users", string="Usuario relacionado", ondelete="cascade")
    # un apoderado tiene un comunicado relacionado
    comunicados = fields.Many2many(
        "administracion_academica.comunicado_prueba",
        string="Comunicados",
        relation="comunicado_prueba_apoderado_rel",
        column1="apoderado_id",
        column2="comunicado_prueba_id",
        readonly=True
    )
    # un apoderado tiene un token de dispositivo relacionado
    dispositivos_ids = fields.One2many(
        "administracion_academica.dispositivo_token",
        inverse_name="apoderado_id",
        string="Tokens de dispositivos",
    )

    sucursal_id = fields.Many2one("administracion_academica.sucursal", 
                                  string="Sucursal")

    _sql_constraints = [
        (
            "correo_electronico_uniq",
            "unique(correo_electronico)",
            "El correo electrónico debe ser único.",
        ),
        (
            "carnet_identidad_uniq",
            "unique(carnet_identidad)",
            "El carnet de identidad debe ser único.",    
        ),
    ]

    @api.model
    def create(self, values):
        # Crear usuario con el correo electrónico como nombre de usuario
        user_vals = {
            'name': f"{values['nombre']} {values['apellidos']}",
            'login': values['correo_electronico'],
            'password': values.get('carnet_identidad'),  # Usar carnet de identidad como contraseña
            'email': values['correo_electronico'],
        }
        user = self.env['res.users'].create(user_vals)

        # Asegurarse de que el usuario se cree correctamente antes de continuar
        if not user:
            raise ValidationError("Error al crear el usuario del apoderado.")
        
        # Asignar el usuario creado al apoderado
        values['user_id'] = user.id

        # Llamar al método create del modelo padre para crear el apoderado
        return super(apoderado, self).create(values)
    
    
    def unlink(self):
        # Primero eliminamos el usuario asociado si existe
        for record in self:
            if record.user_id:
                record.user_id.sudo().unlink()
        return super(apoderado, self).unlink()
        
    @api.depends("nombre", "apellidos")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                f"{rec.nombre} {rec.apellidos}"
            )
            