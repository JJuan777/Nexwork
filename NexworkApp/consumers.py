# NexworkApp/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Conversacion, Mensaje
from django.conf import settings
from NexworkApp.models import Usuario

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.conversacion_id = self.scope['url_route']['kwargs']['conversacion_id']
        self.room_group_name = f'chat_{self.conversacion_id}'

        # print(f"[DEBUG] Conexión establecida - Conversación ID: {self.conversacion_id}, Grupo: {self.room_group_name}")

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # print(f"[DEBUG] Desconexión - Código: {close_code}, Grupo: {self.room_group_name}")

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # print(f"[DEBUG] Mensaje recibido: {text_data}")

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = self.scope['user'].id
        # print(f"[DEBUG] Usuario ID: {user_id}")

        try:
            conversacion = Conversacion.objects.get(id=self.conversacion_id)
            remitente = Usuario.objects.get(id=user_id)
            print(f"[DEBUG] Conversación encontrada: {conversacion}, Remitente: {remitente}")
        except Conversacion.DoesNotExist:
            print("[ERROR] Conversación no encontrada")
            return
        except Usuario.DoesNotExist:
            print("[ERROR] Usuario no encontrado")
            return

        # Guardar el mensaje
        Mensaje.objects.create(
            conversacion=conversacion,
            remitente=remitente,
            texto=message
        )
        # print(f"[DEBUG] Mensaje guardado en la base de datos: {message}")

        # Enviar el mensaje a todos en el grupo de la conversación
        es_mio = remitente.id == self.scope['user'].id
        # print(f"[DEBUG] es_mio: {es_mio}")

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'remitente_id': remitente.id,  # ✅ Enviar ID del remitente
                'es_mio': es_mio
            }
        )

    def chat_message(self, event):
        # print(f"[DEBUG] Mensaje enviado al grupo: {event}")

        message = event['message']
        remitente_id = event['remitente_id']
        usuario_id = self.scope['user'].id  # ✅ Usuario conectado
        es_mio = (remitente_id == usuario_id)  # ✅ Verificar si el remitente es el usuario conectado

        # print(f"[DEBUG] Calculando es_mio: remitente_id={remitente_id}, usuario_id={usuario_id}, es_mio={es_mio}")

        # Enviar el mensaje al frontend
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'es_mio': es_mio,
            'remitente_id': remitente_id
        }))
        # print(f"[DEBUG] Mensaje enviado al frontend: {message} | es_mio: {es_mio} | remitente_id: {remitente_id}")