from odoo import models, fields, api


class Mensualidad(models.Model):
    _name = "administracion_academica.mensualidad"
    _description = "Relacion de los mensualidades de los alumnos"

    monto = fields.Float(string="Monto Bs.")
    cantidad_meses = fields.Integer(string="Cantidad de meses")
 
    # muchas mensualidades le pertencen a un alumno( muchos a uno)
    alumno = fields.Many2one(
        "administracion_academica.alumno", string="Nombre del alumno",domain="[('inscripciones.curso_id', '=', curso_id)]"
    )
    # muchas mensualidades puede tener una gestion ( muchos a uno)
    gestion = fields.Many2one("administracion_academica.gestion", string="Gestión")
    costo_mensualidad = fields.Many2one(
        "administracion_academica.costo_mensualidad", 
        string="Costo de la mensualidad")

    curso_id = fields.Many2one(
        "administracion_academica.curso",
        string ="Curso")

    sucursal_id = fields.Many2one(
        "administracion_academica.sucursal",
        string = "Sucursal")

    # calcula la cantidad total a pagar segun los meses que paga
    @api.onchange("cantidad_meses", "costo_mensualidad")
    def _onchange_cantidad_meses(self):
        if self.cantidad_meses and self.costo_mensualidad:
            self.monto = float(self.cantidad_meses) * float( self.costo_mensualidad.costo)

    @api.onchange("cantidad_meses")
    def action_confirmar_pago_mensualidad(self):
         for mensualidad in self:
            # Se obtiene la inscripción del alumno y curso asociados a esta mensualidad
            inscripcion = self.env['administracion_academica.inscripcion'].search([
                ('alumno_id', '=', mensualidad.alumno.id),
                ('curso_id', '=', mensualidad.curso_id.id)
            ], limit=1)
            
            if inscripcion:
                # Incrementar el contador de mensualidades pagadas
                inscripcion.write({
                    'cantidad_mensualidad': inscripcion.cantidad_mensualidad + mensualidad.cantidad_meses
                })

    def create(self, vals):
        mensualidad = super(Mensualidad, self).create(vals)
        user_id = self.env.uid
        if user_id :
            administrador_logueado = self.env['administracion_academica.administrativo'].search([
                    ('user_id', '=',  user_id)],limit=1)
            
            if administrador_logueado:
                mensualidad.write({
                    'sucursal_id': administrador_logueado.sucursal_id.id
                })
        return mensualidad

    @api.depends()
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (f"Mensualidad {rec.id}")
    
  