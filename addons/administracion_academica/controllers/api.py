# academic_management/controllers/auth_api.py
from odoo import http 
from odoo.http import request, Response
from odoo.tools import config
from collections import defaultdict
import json
import jwt
import datetime
import logging
from .decorators import token_required, token_required_post
from ..utils.firebase import send_push_notification

_logger = logging.getLogger(__name__)

CORS = config.get("cors_domain", "*")


class AuthAPI(http.Controller):

    secret_key = "your_secret_key"

    @http.route("/api/auth/login", auth="public", type="json", methods=["POST"])
    def authenticate(self, **kwargs):
        try:
            params = json.loads(request.httprequest.data)
            username = params.get("username")
            password = params.get("password")

            # Autenticar el usuario con el nombre de la base de datos actual
            uid = request.session.authenticate(
                request.env.cr.dbname, username, password
            )
            if uid is not False:  # Verificar si la autenticación fue exitosa
                user = request.env["res.users"].browse(uid)

                # Verificar si el usuario es un apoderado
                apoderado = (
                    request.env["administracion_academica.apoderado"]
                    .sudo()
                    .search([("user_id", "=", user.id)], limit=1)
                )
                if not apoderado:
                    return {"error": "Acceso no autorizado", "success": False}

                payload = {
                    "user_id": user.id,
                    "exp": datetime.datetime.now()
                    + datetime.timedelta(hours=24),  # Token expira en 24 horas
                }
                token = jwt.encode(payload, self.secret_key, algorithm="HS256")
                # _logger.info("Token creado correctamente para el usuario %s", username)

                response_data = {
                    "success": True,
                    "message": "Usuario autenticado con éxito.",
                    "data": {
                        "user_id": user.id,
                        "user_name": user.name,
                        "user_email": user.email,
                        "token": token,
                    },
                }
                return response_data

            # _logger.error("Credenciales inválidas para el usuario %s", username)
            return {"error": "Credenciales no válidas", "success": False}
        except Exception as e:
            # _logger.exception("Error en el proceso de autenticación: %s", str(e))
            return {
                "error": "Error Interno del Servidor",
                "message": str(e),
                "success": False,
            }

    @http.route("/api/students", auth="public", methods=["GET"])
    @token_required
    def get_students(self):
        try:
            # Obtener la lista de estudiantes
            students = request.env["administracion_academica.alumno"].sudo().search([])
            student_data = []
            for student in students:
                apoderado = student.apoderado
                student_data.append(
                    {
                        "id": student.id,
                        "nombre": student.nombre,
                        "apellido_paterno": student.apellido_paterno,
                        "apellido_materno": student.apellido_materno,
                        "fecha_nacimiento": (
                            student.fecha_nacimiento.strftime("%Y-%m-%d")
                            if student.fecha_nacimiento
                            else None
                        ),
                        "direccion": student.direccion if student.direccion else None,
                        "foto": student.foto_url if student.foto_url else None,
                        "apoderado": (
                            {
                                "id": apoderado.id,
                                "nombre": apoderado.nombre,
                                "apellidos": apoderado.apellidos,
                                "carnet_identidad": apoderado.carnet_identidad,
                                "correo_electronico": apoderado.correo_electronico,
                                "telefono": (
                                    apoderado.telefono if apoderado.telefono else None
                                ),
                                "direccion": (
                                    apoderado.direccion if apoderado.direccion else None
                                ),
                            }
                            if apoderado
                            else None
                        ),
                    }
                )

            _logger.info("Datos de estudiantes obtenidos correctamente")
            response_data = {
                "success": True,
                "data": student_data,
            }
            response_data = json.dumps(response_data)
            return request.make_response(
                response_data,
                headers=[
                    ("Content-Type", "application/json"),
                    ("Access-Control-Allow-Origin", CORS),
                ],
            )
        except Exception as e:
            _logger.exception(
                "Error al obtener los datos de los estudiantes: %s", str(e)
            )
            response_data = json.dumps(
                {
                    "error": "Error Interno del Servidor",
                    "message": str(e),
                    "success": False,
                }
            )
            return request.make_response(
                response_data,
                headers=[
                    ("Content-Type", "application/json"),
                    ("Access-Control-Allow-Origin", CORS),
                ],
            )

    @http.route(
        "/api/apoderado/<int:user_id>/estudiantes", auth="public", methods=["GET"]
    )
    @token_required
    def get_estudiantes_apoderado(self, user_id, **kwargs):
        try:
            # Buscar el apoderado asociado al user_id
            apoderado = (
                request.env["administracion_academica.apoderado"]
                .sudo()
                .search([("user_id", "=", user_id)], limit=1)
            )
            if not apoderado:
                response_data = json.dumps(
                    {
                        "error": "Usuario no encontrado",
                        "success": False,
                    }
                )
                return request.make_response(
                    response_data,
                    headers=[
                        ("Content-Type", "application/json"),
                        ("Access-Control-Allow-Origin", CORS),
                    ],
                )

            # Obtener los estudiantes asociados al apoderado
            estudiantes = (
                request.env["administracion_academica.alumno"]
                .sudo()
                .search([("apoderado", "=", apoderado.id)])
            )

            # Construir la respuesta con los datos de los estudiantes
            data = []
            for estudiante in estudiantes:
                data.append(
                    {
                        "id": estudiante.id,
                        "nombre": estudiante.nombre,
                        "apellido_paterno": estudiante.apellido_paterno,
                        "apellido_materno": estudiante.apellido_materno,
                        "fecha_nacimiento": (
                            estudiante.fecha_nacimiento.strftime("%Y-%m-%d")
                            if estudiante.fecha_nacimiento
                            else None
                        ),
                        "direccion": (
                            estudiante.direccion if estudiante.direccion else None
                        ),
                        "foto": estudiante.foto_url if estudiante.foto_url else None,
                    }
                )

            response_data = json.dumps(
                {
                    "success": True,
                    "data": data,
                }
            )
            return request.make_response(
                response_data,
                headers=[
                    ("Content-Type", "application/json"),
                    ("Access-Control-Allow-Origin", CORS),
                ],
            )
        except Exception as e:
            response_data = json.dumps(
                {
                    "error": "Error Interno del Servidor",
                    "message": str(e),
                    "success": False,
                }
            )
            return request.make_response(
                response_data,
                headers=[
                    ("Content-Type", "application/json"),
                    ("Access-Control-Allow-Origin", CORS),
                ],
            )

    @http.route("/api/comunicados/<int:user_id>", auth="public", methods=["GET"])
    @token_required
    def get_comunicados(self, user_id, **kwargs):
        try:
            # Buscar el apoderado asociado al user_id
            apoderado = (
                request.env["administracion_academica.apoderado"]
                .sudo()
                .search([("user_id", "=", user_id)], limit=1)
            )
            if not apoderado:
                response_data = json.dumps(
                    {
                        "error": "Usuario no encontrado",
                        "success": False,
                    }
                )
                return request.make_response(
                    response_data,
                    headers=[
                        ("Content-Type", "application/json"),
                        ("Access-Control-Allow-Origin", CORS),
                    ],
                )

            # Buscar los comunicados asociados al apoderado
            comunicados = (
                request.env["administracion_academica.comunicado_prueba"]
                .sudo()
                .search(
                    [("apoderado_ids", "in", apoderado.id)],
                    order="create_date desc",
                )
            )

            # comunicados = request.env['administracion_academica.comunicado'].sudo().search([
            #     ('apoderado_ids', '=', apoderado.id)
            # ])

            comunicados_data = []
            for comunicado in comunicados:
                comunicados_data.append(
                    {
                        "id": comunicado.id,
                        "titulo": comunicado.titulo,
                        "mensaje": comunicado.mensaje,
                        "fecha": comunicado.fecha.strftime("%d/%m/%Y %H:%M %p"),
                        "tipo": comunicado.tipo,
                        "remitente": f"{comunicado.profesor_id.nombre} {comunicado.profesor_id.apellidos}"
                        or "Administración Académica",
                    }
                )

            response_data = json.dumps(
                {
                    "success": True,
                    "data": comunicados_data,
                }
            )
            return request.make_response(
                response_data,
                headers=[
                    ("Content-Type", "application/json"),
                    ("Access-Control-Allow-Origin", CORS),
                ],
            )
        except Exception as e:
            response_data = json.dumps(
                {
                    "error": "Error Interno del Servidor",
                    "message": str(e),
                    "success": False,
                }
            )
            return request.make_response(
                response_data,
                headers=[
                    ("Content-Type", "application/json"),
                    ("Access-Control-Allow-Origin", CORS),
                ],
            )

    @http.route(
        "/api/send_push_notification", type="json", auth="public", methods=["POST"]
    )
    def send_push_notification_endpoint(self, **kwargs):

        params = json.loads(request.httprequest.data)
        token = params.get("token")
        title = params.get("title")
        body = params.get("body")

        response = send_push_notification(token, title, body)
        return response

    @http.route("/api/registrar_token", auth="public", type="json", methods=["POST"])
    @token_required_post
    def registrar_token(self, **kwargs):
        try:
            # Obtener los datos del POST request
            params = json.loads(request.httprequest.data)
            user_id = params.get("user_id")
            token = params.get("token")

            # Validar que los datos requeridos estén presentes
            if not user_id or not token:
                return {
                    "error": "Falta el id del usuario o token",
                    "success": False,
                }

            # Buscar el apoderado asociado al user_id
            apoderado = (
                request.env["administracion_academica.apoderado"]
                .sudo()
                .search([("user_id", "=", user_id)], limit=1)
            )

            if not apoderado:
                _logger.warning("Apoderado no encontrado para user_id: %s", user_id)
                return {
                    "error": "Usuario no encontrado",
                    "success": False,
                }

            _logger.info("Apoderado encontrado: %s", apoderado.nombre)

            # Verificar si el token ya está registrado para evitar duplicados
            dispositivo_existente = (
                request.env["administracion_academica.dispositivo_token"]
                .sudo()
                .search([("token", "=", token)], limit=1)
            )

            if dispositivo_existente:
                return {
                    "error": "El token ya está registrado",
                    "success": False,
                }

            # Crear el dispositivo asociado al apoderado
            request.env["administracion_academica.dispositivo_token"].sudo().create(
                {
                    "token": token,
                    "apoderado_id": apoderado.id,
                }
            )

            return {
                "success": True,
                "message": "Token registrado correctamente",
            }
        except Exception as e:
            return {
                "error": "Error Interno del Servidor",
                "message": str(e),
                "success": False,
            }

    @http.route(
        "/api/calificaciones/<int:alumno_id>/<int:gestion_id>/<int:periodo_id>",
        auth="public",
        methods=["GET"],
    )
    @token_required
    def get_calificaciones(self, alumno_id, gestion_id, periodo_id, **kwargs):
        try:
            # Verificar si el alumno existe
            alumno = request.env["administracion_academica.alumno"].sudo().browse(alumno_id)
            if not alumno.exists():
                response_data = json.dumps(
                    {"error": "Alumno no encontrado", "success": False}
                )
                return request.make_response(
                    response_data,
                    headers=[
                        ("Content-Type", "application/json"),
                        ("Access-Control-Allow-Origin", CORS),
                    ],
                )

            # Verificar si el periodo existe
            periodo = request.env["administracion_academica.tipo_periodo"].sudo().browse(
                periodo_id
            )
            if not periodo.exists():
                response_data = json.dumps(
                    {"error": "Periodo no encontrado", "success": False}
                )
                return request.make_response(
                    response_data,
                    headers=[
                        ("Content-Type", "application/json"),
                        ("Access-Control-Allow-Origin", CORS),
                    ],
                )

            # Verificar si la gestion existe
            gestion = request.env["administracion_academica.gestion"].sudo().browse(gestion_id)
            if not gestion.exists():
                response_data = json.dumps(
                    {"error": "Gestión no encontrada", "success": False}
                )
                return request.make_response(
                    response_data,
                    headers=[
                        ("Content-Type", "application/json"),
                        ("Access-Control-Allow-Origin", CORS),
                    ],
                )

            # Construir el dominio para la busqueda
            domain = [("alumno_id", "=", alumno_id)]

            if gestion_id:
                domain.append(("periodo_id.gestion", "=", gestion_id))
            if periodo_id:
                domain.append(("periodo_id.tipo_periodo", "=", periodo_id))

            # Buscar las calificaciones basadas en el dominio
            calificaciones = (
                request.env["administracion_academica.calificacion"]
                .sudo()
                .search(domain)
            )

            calificaciones_data = []
            for calificacion in calificaciones:
                calificaciones_data.append(
                    {
                        "id": calificacion.id,
                        "materia": calificacion.materia_id.nombre,
                        "curso": calificacion.curso_id.nombre,
                        "nota": calificacion.nota,
                        "gestion": calificacion.periodo_id.gestion.year,
                        "periodo": f"{calificacion.periodo_id.tipo_periodo.descripcion} - {calificacion.periodo_id.gestion.year}",
                        "descripcion": calificacion.descripcion,
                        "profesor": f"{calificacion.profesor_id.nombre} {calificacion.profesor_id.apellidos}",
                    }
                )

            response_data = json.dumps(
                {
                    "success": True,
                    "data": calificaciones_data,
                }
            )
            return request.make_response(
                response_data,
                headers=[
                    ("Content-Type", "application/json"),
                    ("Access-Control-Allow-Origin", CORS),
                ],
            )
        except Exception as e:
            response_data = json.dumps(
                {
                    "error": "Error Interno del Servidor",
                    "message": str(e),
                    "success": False,
                }
            )
            return request.make_response(
                response_data,
                headers=[
                    ("Content-Type", "application/json"),
                    ("Access-Control-Allow-Origin", CORS),
                ],
            )

    @http.route(
        "/api/calificaciones_materia/<int:alumno_id>/<int:gestion_id>/<int:periodo_id>",
        auth="public",
        methods=["GET"],
    )
    @token_required
    def get_calificaciones_materia(self, alumno_id, gestion_id, periodo_id, **kwargs):
        try:
            # Verificar si el alumno existe
            alumno = request.env["administracion_academica.alumno"].sudo().browse(alumno_id)
            if not alumno.exists():
                response_data = json.dumps(
                    {"error": "Alumno no encontrado", "success": False}
                )
                return request.make_response(
                    response_data,
                    headers=[
                        ("Content-Type", "application/json"),
                        ("Access-Control-Allow-Origin", CORS),
                    ],
                )

            # Verificar si el periodo existe
            periodo = request.env["administracion_academica.tipo_periodo"].sudo().browse(
                periodo_id
            )
            if not periodo.exists():
                response_data = json.dumps(
                    {"error": "Periodo no encontrado", "success": False}
                )
                return request.make_response(
                    response_data,
                    headers=[
                        ("Content-Type", "application/json"),
                        ("Access-Control-Allow-Origin", CORS),
                    ],
                )

            # Verificar si la gestion existe
            gestion = request.env["administracion_academica.gestion"].sudo().browse(gestion_id)
            if not gestion.exists():
                response_data = json.dumps(
                    {"error": "Gestión no encontrada", "success": False}
                )
                return request.make_response(
                    response_data,
                    headers=[
                        ("Content-Type", "application/json"),
                        ("Access-Control-Allow-Origin", CORS),
                    ],
                )

            # Construir el dominio para la busqueda
            domain = [
                ("alumno_id", "=", alumno_id),
                ("periodo_id.tipo_periodo", "=", periodo_id),
                ("periodo_id.gestion", "=", gestion_id),
            ]

            # Buscar las calificaciones basadas en el dominio
            calificaciones = (
                request.env["administracion_academica.calificacion"]
                .sudo()
                .search(domain)
            )

            # Agrupar calificaciones por materia
            grouped_calificaciones = defaultdict(list)
            for calificacion in calificaciones:
                grouped_calificaciones[calificacion.materia_id.nombre].append(
                    {
                        "id": calificacion.id,
                        "curso": calificacion.curso_id.nombre,
                        "nota": calificacion.nota,
                        "gestion": calificacion.periodo_id.gestion.year,
                        "periodo": f"{calificacion.periodo_id.tipo_periodo.descripcion} - {calificacion.periodo_id.gestion.year}",
                        "descripcion": calificacion.descripcion,
                        "profesor": f"{calificacion.profesor_id.nombre} {calificacion.profesor_id.apellidos}",
                    }
                )

            # Convertir el resultado a una lista para la respuesta JSON y calcular el promedio por materia
            result = []
            suma_promedios = 0
            count_materias = len(grouped_calificaciones)
            for materia, details in grouped_calificaciones.items():
                promedio_materia = sum(d["nota"] for d in details) / len(details)
                suma_promedios += promedio_materia
                result.append(
                    {
                        "materia": materia,
                        "promedio_materia": promedio_materia,
                        "details": details,
                    }
                )

            # Calcular el promedio general
            promedio_general = (
                suma_promedios / count_materias if count_materias > 0 else 0
            )
            response_data = json.dumps(
                {
                    "success": True,
                    "data": result,
                    "data": {
                        "promedio_general": promedio_general,
                        "materias": result,
                    },
                }
            )
            return request.make_response(
                response_data,
                headers=[
                    ("Content-Type", "application/json"),
                    ("Access-Control-Allow-Origin", CORS),
                ],
            )
        except Exception as e:
            response_data = json.dumps(
                {
                    "error": "Error Interno del Servidor",
                    "message": str(e),
                    "success": False,
                }
            )
            return request.make_response(
                response_data,
                headers=[
                    ("Content-Type", "application/json"),
                    ("Access-Control-Allow-Origin", CORS),
                ],
            )

    
    @http.route(
        "/api/promedio_materias/<int:alumno_id>/<int:gestion_id>/<int:periodo_id>",
        auth="public",
        methods=["GET"],
    )
    @token_required
    def get_promedio_materias(self, alumno_id, gestion_id, periodo_id, **kwargs):
        try:
            # Verificar si el alumno existe
            alumno = request.env["administracion_academica.alumno"].sudo().browse(alumno_id)
            if not alumno.exists():
                response_data = json.dumps(
                    {"error": "Alumno no encontrado", "success": False}
                )
                return request.make_response(
                    response_data,
                    headers=[
                        ("Content-Type", "application/json"),
                        ("Access-Control-Allow-Origin", CORS),
                    ],
                )

            # Verificar si la gestion existe
            gestion = request.env["administracion_academica.gestion"].sudo().browse(gestion_id)
            if not gestion.exists():
                response_data = json.dumps(
                    {"error": "Gestión no encontrada", "success": False}
                )
                return request.make_response(
                    response_data,
                    headers=[
                        ("Content-Type", "application/json"),
                        ("Access-Control-Allow-Origin", CORS),
                    ],
                )
                
            # Verificar si el periodo existe
            periodo = request.env["administracion_academica.tipo_periodo"].sudo().browse(
                periodo_id
            )
            if not periodo.exists():
                response_data = json.dumps(
                    {"error": "Periodo no encontrado", "success": False}
                )
                return request.make_response(
                    response_data,
                    headers=[
                        ("Content-Type", "application/json"),
                        ("Access-Control-Allow-Origin", CORS),
                    ],
                )

            # Obtener la inscripción más reciente del alumno en la gestión especificada
            inscripcion = (
                request.env["administracion_academica.inscripcion"]
                .sudo()
                .search(
                    [("alumno_id", "=", alumno_id), ("gestion", "=", gestion_id)],
                    order="id desc",
                    limit=1,
                )
            )

            if not inscripcion:
                response_data = json.dumps(
                    {
                        "error": "No se encontró una inscripción para el alumno en la gestión especificada",
                        "success": False,
                    }
                )
                return request.make_response(
                    response_data,
                    headers=[
                        ("Content-Type", "application/json"),
                        ("Access-Control-Allow-Origin", CORS),
                    ],
                )

            # Obtener el curso asociado a la inscripción
            curso = inscripcion.curso_id

            if not curso:
                response_data = json.dumps(
                    {
                        "error": "No se encontró un curso asociado a la inscripción",
                        "success": False,
                    }
                )
                return request.make_response(
                    response_data,
                    headers=[
                        ("Content-Type", "application/json"),
                        ("Access-Control-Allow-Origin", CORS),
                    ],
                )

            # Construir el dominio para la busqueda
            domain = [
                ("alumno_id", "=", alumno_id),
                ("curso_id", "=", curso.id),
                ("periodo_id.gestion", "=", gestion_id),
                ("periodo_id.tipo_periodo", "=", periodo_id),
            ]

            # Buscar las calificaciones basadas en el dominio
            calificaciones = (
                request.env["administracion_academica.calificacion"]
                .sudo()
                .search(domain)
            )
            _logger.info("Calificaciones encontradas: %s", calificaciones)

            # Agrupar calificaciones por materia y calcular promedio por materia
            grouped_calificaciones = defaultdict(list)
            for calificacion in calificaciones:
                grouped_calificaciones[calificacion.materia_id.nombre].append(
                    calificacion.nota
                )

            # Calcular promedio por materia
            materias_promedio = []
            suma_promedios = 0
            count_materias = len(grouped_calificaciones)
            for materia, notas in grouped_calificaciones.items():
                promedio_materia = sum(notas) / len(notas)
                suma_promedios += promedio_materia
                materias_promedio.append(
                    {
                        "materia": materia,
                        "promedio_materia": promedio_materia,
                    }
                )
                
            # Calcular el promedio general
            promedio_general = (
                suma_promedios / count_materias if count_materias > 0 else 0
            )

            response_data = json.dumps(
                {
                    "success": True,
                    "data": {
                        "alumno": f"{alumno.apellido_paterno} {alumno.apellido_materno} {alumno.nombre}",
                        "gestion": gestion.year,
                        "periodo": periodo.descripcion,
                        "curso": curso.nombre,
                        "promedio_general": promedio_general,
                        "materias_promedio": materias_promedio,
                    },
                }
            )
            return request.make_response(
                response_data,
                headers=[
                    ("Content-Type", "application/json"),
                    ("Access-Control-Allow-Origin", CORS),
                ],
            )
        except Exception as e:
            response_data = json.dumps(
                {
                    "error": "Error Interno del Servidor",
                    "message": str(e),
                    "success": False,
                }
            )
            return request.make_response(
                response_data,
                headers=[
                    ("Content-Type", "application/json"),
                    ("Access-Control-Allow-Origin", CORS),
                ],
            )

    @http.route("/api/gestiones", auth="public", methods=["GET"])
    def get_gestiones(self):
        try:
            # Obtener las gestiones
            gestiones = (
                request.env["administracion_academica.gestion"].sudo().search([])
            )

            gestiones_data = []
            for gestion in gestiones:
                gestiones_data.append({"id": gestion.id, "year": gestion.year})

            response_data = json.dumps({"success": True, "data": gestiones_data})
            return request.make_response(
                response_data,
                headers=[
                    ("Content-Type", "application/json"),
                    ("Access-Control-Allow-Origin", CORS),
                ],
            )
        except Exception as e:
            response_data = json.dumps(
                {
                    "error": "Error Interno del Servidor",
                    "message": str(e),
                    "success": False,
                }
            )
            return request.make_response(
                response_data,
                headers=[
                    ("Content-Type", "application/json"),
                    ("Access-Control-Allow-Origin", CORS),
                ],
            )

    @http.route("/api/periodos", auth="public", methods=["GET"])
    def get_periodos(self):
        try:
            # Obtener los periodos
            periodos = (
                request.env["administracion_academica.tipo_periodo"]
                .sudo()
                .search([], order="descripcion")
            )

            periodos_data = []
            for periodo in periodos:
                periodos_data.append(
                    {
                        "id": periodo.id,
                        "descripcion": periodo.descripcion,
                    }
                )

            response_data = json.dumps({"success": True, "data": periodos_data})
            return request.make_response(
                response_data,
                headers=[
                    ("Content-Type", "application/json"),
                    ("Access-Control-Allow-Origin", CORS),
                ],
            )
        except Exception as e:
            response_data = json.dumps(
                {
                    "error": "Error Interno del Servidor",
                    "message": str(e),
                    "success": False,
                }
            )
            return request.make_response(
                response_data,
                headers=[
                    ("Content-Type", "application/json"),
                    ("Access-Control-Allow-Origin", CORS),
                ],
            )

    @http.route("/api/comunicados_hijos/<int:user_id>", auth="public", methods=["GET"])
    @token_required
    def get_comunicados_hijos(self, user_id, **kwargs):
        try:
            # Buscar el apoderado asociado al user_id
            apoderado = (
                request.env["administracion_academica.apoderado"]
                .sudo()
                .search([("user_id", "=", user_id)], limit=1)
            )
            if not apoderado:
                response_data = json.dumps(
                    {
                        "error": "Usuario no encontrado",
                        "success": False,
                    }
                )
                return request.make_response(
                    response_data,
                    headers=[
                        ("Content-Type", "application/json"),
                        ("Access-Control-Allow-Origin", CORS),
                    ],
                )

            # Obtener la cantidad de comunicados asociados al apoderado
            comunicados = (
                request.env["administracion_academica.comunicado_prueba"]
                .sudo()
                .search_count(
                    [("apoderado_ids", "in", apoderado.id)]
                )
            )
            
            # Obtener la cantidad de hijos asociados al apoderado
            hijos = (
                request.env["administracion_academica.alumno"]
                .sudo()
                .search_count(
                    [("apoderado", "=", apoderado.id)]
                )
            )
            
            data = {
                "comunicados": comunicados,
                "hijos": hijos
            }

            response_data = json.dumps({"success": True, "data": data})
            return request.make_response(
                response_data,
                headers=[
                    ("Content-Type", "application/json"),
                    ("Access-Control-Allow-Origin", CORS),
                ],
            )
        except Exception as e:
            response_data = json.dumps(
                {
                    "error": "Error Interno del Servidor",
                    "message": str(e),
                    "success": False,
                }
            )
            return request.make_response(
                response_data,
                headers=[
                    ("Content-Type", "application/json"),
                    ("Access-Control-Allow-Origin", CORS),
                ],
            )
    

