from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


class Sucursal(models.Model):
    _name = "administracion_academica.sucursal"
    _description = "Sucursales del colegio"

    nombre = fields.Char( string= "Nombre de la sucursal", required=True)
    ciudad = fields.Char( string= "Ciudad de la sucursal", required=True)
    direccion = fields.Char( string= "Dirección de la sucursal", required=True)
    telefono = fields.Char( string= "Teléfono de la sucursal", required=True)

    
    profesores = fields.Many2many("administracion_academica.profesor", 
                                 string="Profesores",
                                 relation ="profesor_sucursal_rel",
                                 column1 = "sucursal_id",
                                 column2 = "profesor_id")

    profesor_sucursal_rel_ids = fields.One2many("administracion_academica.profesor_sucursal_rel",
                                                inverse_name= "sucursal_id",
                                                string = "Profesores")

    director_id = fields.Many2one("administracion_academica.director",
                                   string ="Director")

    administrativos = fields.One2many("administracion_academica.administrativo",
                                      inverse_name="sucursal_id",
                                      string ="Administrativos")
    
    inscripciones = fields.One2many("administracion_academica.inscripcion",
                                    inverse_name = "sucursal_id",
                                    string = "Inscripciones")

    mensualidades = fields.One2many ("administracion_academica.mensualidad",
                                     inverse_name = "sucursal_id",
                                     string = "Mensualidades")
    
    horarios_materia = fields.One2many ("administracion_academica.horario_materia",
                                     inverse_name = "sucursal_id",
                                     string = "Horarios")
    
    apoderados = fields.One2many("administracion_academica.apoderado",
                                 inverse_name = "sucursal_id",
                                 string = "Apoderados")
    
    hr_departament_id =fields.Many2one("hr.department",     
                              string="Departamento relacionado", 
                              ondelete="cascade") 
    
    @api.depends("nombre")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                f"{rec.nombre}-{rec.ciudad}"
            )


    def create(self, vals):
        sucursal_datos = {
            'name': vals.get('nombre'),
            'manager_id':vals.get('director_id'),
        }
        sucursal = self.env['hr.department'].sudo().create(sucursal_datos)
        if not sucursal:
                raise ValidationError("Error al crear el departamento.")
        vals['hr_departament_id'] = sucursal.id
        return super(Sucursal, self).create(vals)

            
