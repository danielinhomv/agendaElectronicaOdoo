import os
import firebase_admin
from firebase_admin import credentials, messaging
import logging

_logger = logging.getLogger(__name__)

# Obtener la ruta al directorio actual
current_dir = os.path.dirname(__file__)

# Construir la ruta al archivo firebase-admin.json
json_path = os.path.join(current_dir, '../data/firebase-admin.json')

# Inicializar la app de Firebase con las credenciales del archivo
cred = credentials.Certificate(json_path)
firebase_admin.initialize_app(cred)


# Enviar notificaciones a un dispositivo
def send_push_notification(token, title, body):
    _logger.info("Enviando notificación push a %s", token)
    # Crear el mensaje
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )

    # Enviar el mensaje
    try:
        response = messaging.send(message)
        return {
            "success": True,
            "data": response
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
  
# Enviar notificaciones a varios dispositivos
def send_push_notifications(tokens, title, body, data):
    _logger.info("Enviando notificación push a %s", tokens)
    _logger.info("Data: %s", data)
    # Crear el mensaje
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data,
        tokens=tokens,
    )

    # Enviar el mensaje
    try:
        # response = messaging.send_multicast(message)
        response = messaging.send_each_for_multicast(message)
        return {
            "success": True,
            "data": response
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }