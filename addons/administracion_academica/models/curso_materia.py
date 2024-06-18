from odoo import models, fields, api

#tabla intermedia entre curso y  materia 
class CursoMateria(models.Model):
    _name = 'administracion_academica.curso_materia'
    _description = 'Relación entre curso y materias'

    #relacion con curso
    curso_id = fields.Many2one('administracion_academica.curso', string="Curso", required=True)
    
    #relacion con materia
    materia_id = fields.Many2one('administracion_academica.materia', string="Materia", required=True)


    display_name = fields.Char(compute='_compute_display_name', store=True)

    @api.depends('curso_id', 'materia_id')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.curso_id.nombre} - {rec.materia_id.nombre}"
    
    _rec_name = 'display_name'
