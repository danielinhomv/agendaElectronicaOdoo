from odoo import models, fields, api
from ..utils.firebase import send_push_notification, send_push_notifications
from datetime import date, datetime, timedelta
import time
import pytz
import logging

_logger = logging.getLogger(__name__)


class ComunicadoPrueba(models.Model):
    _name = "administracion_academica.comunicado_prueba"
    _description = "Comunicados de la institución"

    tipo = fields.Selection(
        [
            ("Citación", "Citación"),
            ("Invitación", "Invitación"),
            ("Entrega de notas", "Entrega de notas"),
            ("Tarea", "Tarea"),
            ("Examen", "Examen"),
            ("Salida", "Salida"),
            ("General", "General"),
        ],
        string="Tipo de comunicado",
        required=True,
        default="General",
    )
    titulo = fields.Char(string="Título", required=True)
    mensaje = fields.Text(string="Mensaje", required=True)
    tipo_destinatario = fields.Selection(
        [
            ("todos", "Todos los Apoderados"),
            ("grupo", "Grupo de Curso"),
            ("especifico", "Apoderado Específico"),
        ],
        string="Tipo de Destinatario",
        required=True,
        default="todos",
    )
    fecha = fields.Datetime(string="Fecha", default=fields.Datetime.now())
    # un comunicado es enviado a varios apoderados(uno a muchos)
    apoderado_ids = fields.Many2many(
        "administracion_academica.apoderado",
        string="Apoderados",
        relation="comunicado_prueba_apoderado_rel",
        column1="comunicado_prueba_id",
        column2="apoderado_id",
    )
    # un comunicado es enviado a varios cursos(uno a muchos)
    curso_ids = fields.Many2many(
        "administracion_academica.curso",
        string="Cursos",
        relation="comunicado_prueba_curso_rel",
        column1="comunicado_prueba_id",
        column2="curso_id",
    )
    profesor_id = fields.Many2one(
        "administracion_academica.profesor", string="Profesor que emite"
    )
    
    @api.depends("tipo")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (f"{rec.tipo}")

    # @api.model
    # def create(self, vals):
    #     record = super(ComunicadoPrueba, self).create(vals)

    #     # Obtener los apoderados asociados al comunicado
    #     apoderados = record.apoderado_ids
    #     _logger.info("Apoderados asociados: %s", apoderados)

    #     # Obtener los tokens de los dispositivos de los apoderados
    #     tokens = apoderados.mapped('dispositivos_ids.token')
    #     _logger.info("Tokens obtenidos: %s", tokens)

    #     # Datos adicionales a enviar en la notificación
    #     data = {
    #         'id': str(record.id),
    #         'fecha': record.fecha.strftime("%d/%m/%Y %H:%M %p"),
    #         'titulo': record.titulo,
    #         'mensaje': record.mensaje,
    #     }

    #     # Enviar notificación a cada token
    #     # for token in tokens:
    #     #     send_push_notification(token, record.titulo, record.mensaje)

    #     send_push_notifications(tokens, record.titulo, record.mensaje, data)

    #     return record

    @api.model
    def create(self, vals):
        # Obtener la zona horaria de Bolivia
        bolivia_tz = pytz.timezone('America/La_Paz')
        
        # Convertir la hora actual a la zona horaria de Bolivia
        now_utc = datetime.now(pytz.utc)
        now_bolivia = now_utc.astimezone(bolivia_tz)
        
        # Convertir la hora "aware" a "naive"
        now_bolivia_naive = now_bolivia.replace(tzinfo=None)
        
        # Asignar la hora convertida a la fecha del comunicado
        vals['fecha'] = now_bolivia_naive
        
        comunicado = super(ComunicadoPrueba, self).create(vals)
        if comunicado.tipo_destinatario == "todos":
            _logger.info("ENVIANDO A TODOS LOS APODERADOS")
            apoderados = self.env["administracion_academica.apoderado"].search([])
            comunicado.apoderado_ids = [(6, 0, apoderados.ids)]
            # comunicado.write({'apoderado_ids': [(6, 0, apoderados.ids)]})

        elif comunicado.tipo_destinatario == "grupo":
            _logger.info("ENVIANDO A GRUPO DE CURSO")
            inscripciones = comunicado.curso_ids.mapped("inscripciones")
            alumnos = inscripciones.mapped("alumno_id")
            apoderados = alumnos.mapped("apoderado")
            _logger.info("Apoderados obtenidos grupo: %s", apoderados)
            comunicado.apoderado_ids = [(6, 0, apoderados.ids)]
        else:  # tipo_destinatario == 'especifico'
            _logger.info("ENVIANDO A APODERADO ESPECIFICO")
            apoderados = comunicado.apoderado_ids
            _logger.info("Apoderados obtenidos especifico: %s", apoderados)

        tokens = apoderados.mapped("dispositivos_ids.token")
        data = {
            "id": str(comunicado.id),
            "fecha": comunicado.fecha.strftime("%d/%m/%Y %H:%M %p"),
            "titulo": comunicado.titulo,
            "mensaje": comunicado.mensaje,
            "tipo": comunicado.tipo,
            "remitente": (
                f"{comunicado.profesor_id.nombre} {comunicado.profesor_id.apellidos}"
                if comunicado.profesor_id
                else "Administración Académica"
            ),
        }
        send_push_notifications(tokens, comunicado.titulo, comunicado.mensaje, data)
        return comunicado

    