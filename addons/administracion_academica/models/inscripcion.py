from odoo import models, fields, api
from datetime import datetime
from datetime import date
from odoo.exceptions import ValidationError

# tabla intermedia entre curso y alumno
class Inscripcion(models.Model):
    _name = "administracion_academica.inscripcion"
    _description = "Inscripciones de los estudiantes"

    curso_id = fields.Many2one(
        "administracion_academica.curso", string="Curso", required=True
    )
    alumno_id = fields.Many2one(
        "administracion_academica.alumno", string="Alumno", required=True
    )
    fecha = fields.Datetime(string="Fecha Actual", default=datetime.now())

    cantidad_mensualidad = fields.Integer(string ="Cantidad de mensualidades", default =0)
    # muchas inscripciones pueden darse en una gestion (muchos a uno)
    gestion = fields.Many2one("administracion_academica.gestion", string="Gestión")
    
    sucursal_id = fields.Many2one("administracion_academica.sucursal", string ="Sucursal")
    
    @api.depends("fecha")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                f"Inscripción {self.id} - {rec.fecha}"
            )

    @api.model
    def _get_mes_actual(self):
        mes_actual = date.today().month
        return mes_actual

    @api.depends('cantidad_mensualidad')
    def _compute_estado_pago(self):
        meses = {
            1: 'febrero', 2: 'marzo', 3: 'abril',
            4: 'mayo', 5: 'junio', 6: 'julio', 7: 'agosto',
            8: 'septiembre', 9: 'octubre', 10: 'noviembre'
        }

        for inscripcion in self:
            mes_actual = self._get_mes_actual()
            mes_actual_nombre = meses.get(mes_actual, False)

            if not mes_actual_nombre:
                inscripcion.estado_pago = 'desconocido'
                continue

            numero_mes_actual = mes_actual
            mes_pago_minimo = meses[mes_actual]

            if inscripcion.cantidad_mensualidad >= numero_mes_actual:
                inscripcion.estado_pago = 'al día'
            else:
                inscripcion.estado_pago = 'deudor'

    estado_pago = fields.Selection([
        ('al día', 'Al día'),
        ('deudor', 'Deudor'),
        ('desconocido', 'Desconocido')
    ], string="Estado de pago", compute="_compute_estado_pago", store=True)

    def create(self, vals):
        inscripcion = super(Inscripcion, self).create(vals)
        user_id = self.env.uid
        if user_id :
            administrador_logueado = self.env['administracion_academica.administrativo'].search([
                    ('user_id', '=',  user_id)],limit=1)
            
            if administrador_logueado:
                inscripcion.write({
                    'sucursal_id': administrador_logueado.sucursal_id.id
                })
        
        return inscripcion

         
    @api.constrains('curso_id', 'alumno_id', 'gestion')
    def _check_unique_inscripcion(self):
        for inscripcion in self:
            existing_inscripcion = self.search([
                ('curso_id', '=', inscripcion.curso_id.id),
                ('alumno_id', '=', inscripcion.alumno_id.id),
                ('gestion', '=', inscripcion.gestion.id),
                ('id', '!=', inscripcion.id)
            ])
            if existing_inscripcion:
                raise ValidationError('El alumno ya está inscrito en este curso y gestión.')

