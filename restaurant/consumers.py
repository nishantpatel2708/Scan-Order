from channels.generic.websocket import WebsocketConsumer
import json
from .models import *
from asgiref.sync import async_to_sync, sync_to_async

class WaiterCall(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['rest_id']
        self.room_group_name = 'waiter_call_%s' % self.room_name
        print('connect')
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    
    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
             self.room_group_name,
             {
                 'type': text_data
             }
        )
    
    def call_wait(self, event):
        print(event)
        data = json.loads(event['value'])
        print(data)
        self.send(text_data=json.dumps({
            'payload': data
        }))