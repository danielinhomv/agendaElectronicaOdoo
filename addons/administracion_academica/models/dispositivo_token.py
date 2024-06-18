from odoo import models, fields, api


class DispositivoToken(models.Model):
    _name = "administracion_academica.dispositivo_token"
    _description = "Tokens de dispositivos"

    token = fields.Char(string="Token", required=True)
    apoderado_id = fields.Many2one(
        "administracion_academica.apoderado", string="Apoderado"
    )

    # @api.model_create_single
    # def create(self, vals):
    #     record = super(DispositivoToken, self).create(vals)
    #     return record
