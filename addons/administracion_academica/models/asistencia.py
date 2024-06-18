from odoo import models, fields, api
import datetime


class asistencia(models.Model):
    _name = "administracion_academica.asistencia"
    _description = "Asistencia del alumno"

    fecha = fields.Date(string ="Fecha", default= datetime.datetime.now())
    estado = fields.Selection(
        [
            ('Presente', 'Presente'),
            ('Ausente', 'Ausente'),
            ('Atrasado', 'Atrasado'),
            ('Licencia', 'Licencia'),
        ],
        string = "Estado",
        required = True,
        default = 'Presente'
    )

    clase_id = fields.Many2one(
        "administracion_academica.clase",
        string = "Clase",
        ondelete='cascade')
    
    alumno_id = fields.Many2one(
        "administracion_academica.alumno",
        string = "Alumno",
        ondelete='cascade')
        
    def enviar_notificaciones(self):
        # Recuperar la lista de asistencias
        asistencias = self.search([])  # Puedes agregar un dominio para filtrar las asistencias si es necesario
        #añadir lo de enviar las notificaciones
        
