# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        print("Connection established.")
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        message_sender_id = text_data_json['message_sender_id']
        message_receiver_id = text_data_json['message_receiver_id']

        # Message.objects.create(sender_id=message_sender_id, message=message, message_receiver_id=message_receiver_id)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'message_sender_id': message_sender_id,
            }
        )
        print('socket receive')

    # Receive message from room/ group
    def chat_message(self, event):
        message = event['message']
        message_sender_id = event['message_sender_id']
        # room_name = event['roomName']
        print("message_sender_id:", message_sender_id)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'message_sender_id': message_sender_id,
        }))
        print('socket chat_receive')
