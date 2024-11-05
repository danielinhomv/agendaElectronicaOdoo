from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class Profesor(models.Model):
    _name = "administracion_academica.profesor"
    _description = "Relacion de los profesores del colegio"

    nombre = fields.Char(string="Nombre", required=True)
    apellidos = fields.Char(string="Apellidos", required=True)
    carnet_identidad = fields.Char(string="Canet de identidad", required=True)
    telefono = fields.Char(string="Telefono")
    direccion = fields.Char(string="Dirección")
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento")
    foto = fields.Image(string="Foto")

    asignacion_materias = fields.One2many(
        "administracion_academica.carga_horaria_rel",  
        inverse_name="profesor_id", 
        string="Materias asignadas")

    materias = fields.Many2many(
        'administracion_academica.materia', 
        compute="_compute_materias", 
        string="Materias")

    correo_electronico = fields.Char(string="Email")

    calificaciones = fields.One2many(
        'administracion_academica.calificacion', 
        inverse_name="profesor_id",
        string="Calificaciones")
    
    comunicados = fields.One2many(
        'administracion_academica.comunicado', 
        inverse_name="profesor_id",
        string = "Comunicados"
    )  

    asistencias = fields.One2many(
        'administracion_academica.clase',
        inverse_name ="profesor_id",
        string = "Asistencias"
    )
    comunicados_prueba = fields.One2many(
        'administracion_academica.comunicado_prueba', 
        inverse_name="profesor_id",
        string = "Comunicados"
    )
    
    sucursales = fields.Many2many("administracion_academica.sucursal", 
                                 string="Sucursales",
                                 relation ="profesor_sucursal_rel",
                                 column1 = "profesor_id",
                                 column2 = "sucursal_id")
    
    profesor_sucursal_rel_ids = fields.One2many("administracion_academica.profesor_sucursal_rel",
                                                inverse_name= "profesor_id",
                                                string = "Sucursales")
    
    # relacion con el modelo empleado del modulo de Odoo (Recursos Humanos)
    employee_id = fields.Many2one("hr.employee", string="Empleado", ondelete="cascade")


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

    @api.depends('asignacion_materias')
    def _compute_materias(self):
        current_user = self.env.user
        if current_user:
            profesor_logueado = self.env['administracion_academica.profesor'].search(
                [('correo_electronico', '=', current_user.email)])
            for profesor in self:   
                if profesor.id == profesor_logueado.id:
                    profesor.materias = profesor.asignacion_materias.mapped('materia_id')
                else:
                    profesor.materias = []
        else:            
            profesor.materias = []

    @api.model
    def create(self, vals):
        # Crear empleado de Odoo
        full_name = f"{vals.get('nombre')} {vals.get('apellidos')}"
        employee_vals = {
            'name': full_name,
            'job_title': 'Profesor',
            'work_phone': vals.get('telefono'),
            'work_email': vals.get('correo_electronico'),
            'image_1920': vals.get('foto'),
            'private_street': vals.get('direccion'),
            "birthday": vals.get('fecha_nacimiento'),
            'resource_id': self.env['resource.resource'].create({'name': full_name}).id,
        }

        employee = self.env['hr.employee'].sudo().create(employee_vals)
      # Crear usuario de Odoo
        user_vals = {
            'name': full_name,
            'login': vals.get('correo_electronico'),  
            'email': vals.get('correo_electronico'),
            #'password': vals.get('carnet_identidad'), 
            'password': '123456',  # por el momento usar esta
            'image_1920': vals.get('foto'),
            'employee_ids': [(4, employee.id)],
            'groups_id': [(6, 0, [
                self.env.ref('base.group_user').id,
                self.env.ref('administracion_academica.group_profesor').id,
                ])], 
        }
        user = self.env['res.users'].sudo().create(user_vals)

        if not user:
            raise ValidationError("Error al crear el usuario del profesor.")
        
        vals['user_id'] = user.id
        vals['employee_id'] = employee.id
        profesor_creado = super(Profesor, self).create(vals)
        user_id = self.env.uid
        adminstrativo_logueado = self.env['administracion_academica.administrativo'].search(
                [('user_id', '=', user_id)])
        
        if adminstrativo_logueado:
            self.env['administracion_academica.profesor_sucursal_rel'].create({'profesor_id': profesor_creado.id,
                                                      'sucursal_id': adminstrativo_logueado.sucursal_id.id})
            employee.sudo().write({
                'department_id': adminstrativo_logueado.sucursal_id.hr_departament_id.id
                    })


        return profesor_creado
     
    
    def write(self, vals):
        # Actualizar empleado relacionado
        res = super(Profesor, self).write(vals)
        for record in self:
            employee_vals = {}
            if 'nombre' in vals or 'apellidos' in vals:
                employee_vals['name'] = f"{record.nombre} {record.apellidos}"
            if 'telefono' in vals:
                employee_vals['work_phone'] = vals['telefono']
            if 'correo_electronico' in vals:
                employee_vals['work_email'] = vals['correo_electronico']
            if 'direccion' in vals:
                employee_vals['private_street'] = vals['direccion']
            if 'foto' in vals:
                employee_vals['image_1920'] = vals['foto']
            if 'fecha_nacimiento' in vals:
                employee_vals['birthday'] = vals['fecha_nacimiento']
            if employee_vals:
                record.employee_id.resource_id.name = f"{record.nombre} {record.apellidos}"                
                record.employee_id.sudo().write(employee_vals)
        return res
    
    def unlink(self):
        # Primero eliminamos el empleado asociado si existe
        for record in self:
            if record.employee_id:
                record.employee_id.sudo().unlink()
        return super(Profesor, self).unlink()
    
    @api.depends("nombre", "apellidos")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.nombre} {rec.apellidos}"
    