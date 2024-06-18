from odoo import models, fields, api
from datetime import datetime

class comunicado(models.Model):
    _name = "administracion_academica.comunicado"
    _description = "Comunicados para los apoderados"

    tipo = fields.Selection(
        [
            ("Citación", "Citación"),
            ("Invitación", "Invitación"),
            ("Entrega de notas", "Entrega de notas"),
            ("Tarea", "Tarea"),
            ("Examen", "Examen"),
            ("Salida", "Salida"),
            ("General", "General")
        ],
        string="Tipo de comunicado",
        required=True,
        default="General",
    )
    descripcion = fields.Char(string="Descripción")
    fecha = fields.Date(string="Fecha de comunicado", default=datetime.now())
    estado = fields.Boolean( string ="Estado", default=False)

    profesor_id = fields.Many2one(
        "administracion_academica.profesor",
        string="Profesor que emite"
    )

    alumno_comunicados = fields.One2many(
        'administracion_academica.alumno_comunicado', 
        inverse_name="comunicado_id",
        string="Comunicados del apoderado"
    )

    alumnos = fields.Many2many(
        "administracion_academica.alumno",
        compute = "_compute_alumnos",
        string= "Alumnos"
    )

    
    @api.depends("tipo")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (f"{rec.tipo}")


    @api.depends('alumno_comunicados')
    def _compute_alumnos(self):
        for comunicado in self:
            comunicado.alumnos = comunicado.alumno_comunicados.mapped('alumno_id')
