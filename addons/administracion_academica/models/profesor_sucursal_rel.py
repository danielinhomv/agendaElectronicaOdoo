from odoo import models, fields, api


# tabla intermedia entre materia y profesor
class CargaHorariaRel(models.Model):
    _name = "administracion_academica.profesor_sucursal_rel"
    _description = "Relación entre profesores y sucursales"

    profesor_id = fields.Many2one(
        'administracion_academica.profesor',string ="Profesor",required=True)

    sucursal_id = fields.Many2one(
        'administracion_academica.sucursal',string ="Sucursal",required=True)

    @api.depends("profesor_id", "sucursal_id")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.sucursal_id.nombre}-{rec.profesor_id.nombre} {rec.profesor_id.apellidos}"