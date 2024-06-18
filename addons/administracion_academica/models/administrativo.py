from odoo import models, fields, api
from ..utils.cloudinary_helper import CloudinaryHelper
from datetime import date
from odoo.exceptions import ValidationError


class Administrativo(models.Model):
    _name = "administracion_academica.administrativo"
    _description = "Administrativo del colegio"

    nombre = fields.Char(string="Nombre", required=True)
    apellidos = fields.Char(string="Apellidos", required=True)
    fecha_nacimiento = fields.Date(string="Fecha de nacimiento")
    carnet_identidad = fields.Char(string="Carnet de identidad")
    correo_electronico = fields.Char(string="Correo electrónico")
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
    tipo =fields.Selection(
        [
            ("Administrativo", "Administrativo"),
            ("Limpieza y Mantenimiento", "Limpieza y Mantenimiento"),
        ],
        string="Tipo",
        required=True,
        default="Administrativo",
    )

    sucursal_id = fields.Many2one("administracion_academica.sucursal",
                                  string="Sucursal")
    
    employee_id = fields.Many2one("hr.employee", 
                                  string="Empleado", 
                                  ondelete="cascade")
    
    user_id = fields.Many2one("res.users",     
                              string="Usuario relacionado", 
                              ondelete="cascade")
    
    def create(self, vals):
        # Crear empleado de Odoo
        full_name = f"{vals.get('nombre')} {vals.get('apellidos')}"
        employee_vals = {
            'name': full_name,
            'job_title': vals.get('tipo'),
            'work_phone': vals.get('telefono'),
            'work_email': vals.get('correo_electronico'),
            'image_1920': vals.get('foto'),
            'private_street': vals.get('direccion'),
            "birthday": vals.get('fecha_nacimiento'),
            'resource_id': self.env['resource.resource'].create({'name': full_name}).id,
        }
        #se le asigna el empleado al departamento o sucursal
        sucursal = self.env['administracion_academica.sucursal'].browse(vals.get('sucursal_id'))
        if sucursal:
            department_id = sucursal.hr_departament_id.id  
            employee_vals.update({'department_id': department_id})
       
        employee = self.env['hr.employee'].sudo().create(employee_vals)

        if vals.get('tipo') == 'Administrativo':
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
                    self.env.ref('hr.group_hr_user').id,  #crear empleados
                    self.env.ref('administracion_academica.group_administrativo').id,
                    ])], 
            }
            user = self.env['res.users'].sudo().create(user_vals)
            if not user:
                raise ValidationError("Error al crear el usuario del administrativo.")

            vals['user_id'] = user.id

        vals['employee_id'] = employee.id
        return super(Administrativo, self).create(vals)