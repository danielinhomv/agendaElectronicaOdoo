# import os
# from odoo import models, fields, api
# from firebase_admin import credentials, initialize_app, messaging

# # Inicializa la app con tus credenciales de servicio
# cred = credentials.Certificate('./data/firebase-admin.json')
# firebase_admin.initialize_app(cred)

# def send_push_notification(token, title, body):
#     # Crear el mensaje
#     message = messaging.Message(
#         notification=messaging.Notification(
#             title=title,
#             body=body,
#         ),
#         token=token,
#     )

#     # Enviar el mensaje
#     try:
#         response = messaging.send(message)
#         print('Successfully sent message:', response)
#     except Exception as e:
#         print('Error sending message:', e)


# class FirebaseService(models.AbstractModel):
#     _name = "firebase.service"
#     _description = "Firebase Service"

#     _firebase_initialized = False

#     def _initialize_firebase(self):
#         if not self._firebase_initialized:
#             firebase_cred_path = os.path.join(
#                 os.path.dirname(os.path.abspath(__file__)),
#                 "../data/firebase-admin.json",
#             )
#             if os.path.isfile(firebase_cred_path):
#                 cred = credentials.Certificate(firebase_cred_path)
#                 initialize_app(cred)
#                 self._firebase_initialized = True
#             else:
#                 raise ValueError(
#                     "Firebase credentials file not found at {}".format(
#                         firebase_cred_path
#                     )
#                 )

#     def send_notification(self, title, body, tokens):
#         self._initialize_firebase()
#         messages = [
#             messaging.Message(
#                 notification=messaging.Notification(
#                     title=title,
#                     body=body,
#                 ),
#                 token=token,
#             )
#             for token in tokens
#         ]
#         response = messaging.send_all(messages)
#         return response.success_count, response.failure_count

    
