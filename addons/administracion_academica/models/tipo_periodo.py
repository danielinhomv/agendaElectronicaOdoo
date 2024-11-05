from odoo import models, fields, api
from odoo.exceptions import ValidationError


class tipo_periodo(models.Model):
    _name = "administracion_academica.tipo_periodo"
    _description = "tipos que puede tener un periodo"

    descripcion = fields.Char(string="Tipo de período", required=True)
    periodos = fields.One2many(
        "administracion_academica.periodo",
        inverse_name="tipo_periodo",
        string="Periodo ",
    )
    
    @api.depends("descripcion")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                f"{rec.descripcion}"
            )
    
    @api.constrains('descripcion')
    def _check_unique_descripcion(self):
        for rec in self:
            # Buscar registros con la misma descripción, ignorando mayúsculas y minúsculas
            existing = self.search([('descripcion', '=ilike', rec.descripcion)])
            if len(existing) > 1:
                raise ValidationError("El tipo de período debe ser único. Ingrese otro valor.")
