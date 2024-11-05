from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    # administrativo_id = fields.Many2one(
    #     'administracion_academica.administrativo', 
    #     string='Administrativo')
