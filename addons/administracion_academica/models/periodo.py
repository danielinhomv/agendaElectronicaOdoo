from odoo import models, fields, api


class periodo(models.Model):
    _name = "administracion_academica.periodo"
    _description = "periodos de la gestión académica"

    fecha_inicio = fields.Date(string="Inicio de período")
    fecha_final = fields.Date(string="Fin de período")
    # muchos periodos pertencen a una gestion
    gestion = fields.Many2one("administracion_academica.gestion", string="Gestión")
    # muchos periodos pertencen a un tipo de periodo
    tipo_periodo = fields.Many2one(
        "administracion_academica.tipo_periodo", string="Tipo de periodo"
    )

   # un periodo tiene muchas calificaciones ( uno a muchos)
    calificaciones = fields.One2many(
        'administracion_academica.calificacion', 
        inverse_name="periodo_id",
        string="Calificacion")

    @api.depends("tipo_periodo", "gestion")
    def _compute_display_name(self):
        for rec in self:
            tipo_periodo_nombre = (
                rec.tipo_periodo.descripcion if rec.tipo_periodo else ""
            )
            gestion_nombre = rec.gestion.year if rec.gestion else ""
            rec.display_name = f"{tipo_periodo_nombre} - {gestion_nombre}".strip()
