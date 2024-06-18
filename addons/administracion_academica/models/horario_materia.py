from odoo import models, fields, api

class HorarioMateria(models.Model):
    _name = "administracion_academica.horario_materia"
    _description = "Horario de las amterias"

    horario_id = fields.Many2one(
        "administracion_academica.horario", 
        string="Horario"
    )

    materia_id = fields.Many2one(
        "administracion_academica.materia", 
        string="Materia"
    )

    curso_id = fields.Many2one(
        "administracion_academica.curso", 
        string="Curso"
    )  

    carga_horaria_id = fields.Many2one(
        "administracion_academica.carga_horaria_rel",
        string =" Materia-Profesor"
    )

    sucursal_id = fields.Many2one(
        "administracion_academica.sucursal",
        string =" Sucursal"
    )


    @api.depends("curso_id","carga_horaria_id")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                # f"{self.curso_id.nombre} - {self.materia_id.nombre} - {self.horario_id}"
                f"{self.curso_id.nombre} - {self.carga_horaria_id}"
            ) 

    def create(self, vals):
        horario_materia = super(HorarioMateria, self).create(vals)
        user_id = self.env.uid
        if user_id :
            administrador_logueado = self.env['administracion_academica.administrativo'].search([
                    ('user_id', '=',  user_id)],limit=1)
            
            if administrador_logueado:
                horario_materia.write({
                    'sucursal_id': administrador_logueado.sucursal_id.id
                })
        return horario_materia

