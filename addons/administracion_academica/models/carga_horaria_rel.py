from odoo import models, fields, api
from odoo.exceptions import ValidationError


# tabla intermedia entre materia y profesor
class CargaHorariaRel(models.Model):
    _name = "administracion_academica.carga_horaria_rel"
    _description = "Relación entre profesores y materias"

    # relacion con materia
    materia_id = fields.Many2one(
        "administracion_academica.materia", string="Materia", required=True,
    )

    profesor_id = fields.Many2one(
        'administracion_academica.profesor',string ="Profesor",required=True)

    horario_materia_ids = fields.One2many(
        "administracion_academica.horario_materia",
        inverse_name = "carga_horaria_id",
        string = " Materia-Profesor")

    @api.depends("materia_id","profesor_id")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                f"{rec.materia_id.nombre}-{rec.profesor_id.nombre} {rec.profesor_id.apellidos}"
            )
    # horarios_materia = fields.One2many(
    #     'administracion_academica.horario_materia', 
    #     'materia_id', 
    #     string='Horario de las clases',
    #     ondelete='cascade') 
    
    @api.constrains('materia_id', 'profesor_id')
    def _check_unique_materia_profesor(self):
        for rec in self:
            existing = self.search([
                ('materia_id', '=', rec.materia_id.id),
                ('profesor_id', '=', rec.profesor_id.id),
                ('id', '!=', rec.id)
            ])
            if existing:
                raise ValidationError("Este profesor ya está asignado a esta materia.")  