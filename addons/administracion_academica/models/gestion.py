from odoo import models, fields, api


class gestion(models.Model):
    _name = "administracion_academica.gestion"
    _description = "año de gestión académica"

    year = fields.Char(string="Año de gestión", required=True)
    # una gestion puede tener varios periodos (uno a muchos)
    periodos = fields.One2many(
        "administracion_academica.periodo", inverse_name="gestion", string="Periodo"
    )
    # una gestion puede tener varias inscripciones ( uno a muchos)
    inscripciones = fields.One2many(
        "administracion_academica.inscripcion",
        inverse_name="gestion",
        string="Inscripciones",
    )
    # una gestion tiene muchas mensualidades ( uno a muchos)
    mensualidades = fields.One2many(
        "administracion_academica.mensualidad",
        inverse_name="gestion",
        string="Mensualidades",
    )


    @api.depends("year")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                f"{rec.year}".strip()
            )
            
    _sql_constraints = [
        (
            "year_unique",
            "unique(year)",
            "El año de gestión debe ser único.",
        )
    ]
   
