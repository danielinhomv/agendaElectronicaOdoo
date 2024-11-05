import json
import jwt
from odoo.http import request
from odoo.tools import config
import logging

CORS = config.get("cors_domain", "*")

_logger = logging.getLogger(__name__)
secret_key = "your_secret_key"


def token_required(f):
    def wrapper(*args, **kwargs):
        try:
            token = request.httprequest.headers.get("Authorization")

            if not token:
                response_data = json.dumps(
                    {
                        "error": "Token faltante",
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
            elif token.startswith("Bearer "):
                token = token.split(" ")[
                    1
                ]  # Obtener solo el token, sin el prefijo 'Bearer '

            try:
                # Decodificar el token JWT
                payload = jwt.decode(token, secret_key, algorithms=["HS256"])

                user_id = payload["user_id"]
                user = request.env["res.users"].sudo().browse(user_id)
                if not user:
                    response_data = json.dumps(
                        {
                            "error": "Token inválido",
                            "message": "Usuario no encontrado",
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
            except jwt.ExpiredSignatureError:
                response_data = json.dumps(
                    {
                        "error": "Token expirado",
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
            except jwt.InvalidTokenError:
                response_data = json.dumps(
                    {
                        "error": "Token inválido",
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

            return f(*args, **kwargs)
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

    return wrapper


def token_required_post(f):
    def wrapper(*args, **kwargs):
        try:
            token = request.httprequest.headers.get("Authorization")

            if not token:
                return {
                    "error": "Token faltante",
                    "success": False,
                }
            elif token.startswith("Bearer "):
                token = token.split(" ")[
                    1
                ]  # Obtener solo el token, sin el prefijo 'Bearer '

            try:
                # Decodificar el token JWT
                payload = jwt.decode(token, secret_key, algorithms=["HS256"])

                user_id = payload["user_id"]
                user = request.env["res.users"].sudo().browse(user_id)
                if not user:
                    # _logger.error("Token inválido para el usuario ID %s", user_id)
                    return {
                        "error": "Token inválido",
                        "message": "Usuario no encontrado",
                        "success": False,
                    }
            except jwt.ExpiredSignatureError:
                return {
                    "error": "Token expirado",
                    "success": False,
                }
            except jwt.InvalidTokenError:
                return {
                    "error": "Token inválido",
                    "success": False,
                }

            return f(*args, **kwargs)
        except Exception as e:
            return {
                "error": "Error Interno del Servidor",
                "message": str(e),
                "success": False,
            }

    return wrapper
