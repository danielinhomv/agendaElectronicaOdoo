from odoo import models, fields, api

class costoMensualidad(models.Model):
    _name = 'administracion_academica.costo_mensualidad'
    _description = 'Costo de las mensualidades por nivel ( incial, primaria, secundaria)'

    costo = fields.Float(string= "Monto")
    grado = fields.Selection(
        [
             ("inicial", "Inicial"),
             ("primaria", "Primaria"),
             ("secundaria", "Secundaria"),

        ],
        string ="Nivel",
        default="inicial",
        required= True,
    )
    
    # un costo de mensualidad pertenece a una mensualidad ( uno a muchos)    
    mensualidades = fields.One2many('administracion_academica.mensualidad', inverse_name="costo_mensualidad",string="Mensualidad")

    @api.depends("grado","costo")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                f"{rec.grado}: {rec.costo}Bs"
            )
            
