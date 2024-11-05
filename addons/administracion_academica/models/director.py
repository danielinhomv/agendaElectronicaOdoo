from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Director(models.Model):
    _name = "administracion_academica.director"
    _description = "Director de sucursal"

    nombre = fields.Char(string="Nombre", required=True)
    apellidos = fields.Char(string="Apellidos", required=True)
    carnet_identidad = fields.Char(string="Canet de identidad", required=True)
    correo_electronico = fields.Char(string="Email", required=True)
    fecha_nacimiento = fields.Date(string="Fecha de nacimiento", required=True)
    telefono = fields.Char(string="Telefono")
    direccion = fields.Char(string="Dirección")
    foto = fields.Image(string="Foto")
    foto_url = fields.Char(string="URL de la foto")
    tipo = fields.Selection ([
        ('Director General', 'Director General'),
        ('Sub-Director', 'Sub-Director')
    ],
        string="Tipo",
        required=True,
        default="Sub-Director")
    
    sucursal = fields.One2many("administracion_academica.sucursal",
                               inverse_name = "director_id",
                               string ="Centro Educativo")
    
    employee_id = fields.Many2one("hr.employee", 
                                  string="Empleado", 
                                  ondelete="cascade")
    
    user_id = fields.Many2one("res.users", 
                              string="Usuario relacionado", 
                              ondelete="cascade")

    @api.depends("nombre", "apellidos")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.nombre} {rec.apellidos}"

    def create(self, vals):
        # Crear empleado de Odoo
        full_name = f"{vals.get('nombre')} {vals.get('apellidos')}"

        if vals.get('tipo') == 'Director General':
            employee_vals = {
                'name': full_name,
                'job_title': 'Director General',
                'work_phone': vals.get('telefono'),
                'work_email': vals.get('correo_electronico'),
                'image_1920': vals.get('foto'),
                'private_street': vals.get('direccion'),
                "birthday": vals.get('fecha_nacimiento'),
                'resource_id': self.env['resource.resource'].create({'name': full_name}).id,
            }
        else:
            employee_vals = {
            'name': full_name,
            'job_title': 'Director',
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
                self.env.ref('administracion_academica.group_administrativo').id,
                ])], 
        }
        user = self.env['res.users'].sudo().create(user_vals)

        if not user:
            raise ValidationError("Error al crear el usuario del Director.")
        
        vals['user_id'] = user.id
        vals['employee_id'] = employee.id
        return super(Director, self).create(vals)