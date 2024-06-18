from odoo import models, fields, api

class alumnoComunicado(models.Model):
    _name = "administracion_academica.alumno_comunicado"
    _description = "Relacion entre comunicados y alumnos"

    alumno_id = fields.Many2one(
        "administracion_academica.alumno",
        string="Alumno"
    )

    comunicado_id = fields.Many2one(
        "administracion_academica.comunicado",
        string="Comunicado"
    )
