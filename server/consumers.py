import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import ChatModel
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']

        if int(my_id) > int(other_user_id):
            self.room_name = f"{my_id}-{other_user_id}"
        else:
            self.room_name = f"{other_user_id}-{my_id}"
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, code):
        # await self.channel_layer.group_discard(
        #     self.room_group_name,
        #     self.channel_layer
        # )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username= text_data_json['username']
        time = text_data_json['time']  

        print(f"Time: {time}")

        await self.save_message(username, self.room_name, message, time)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'time': time
            }
        ) 

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        time = event['time']
        

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'time': time
        }))  

    @database_sync_to_async
    def save_message(self, username, thread_name, message, time):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(username=username)
        ChatModel.objects.create(sender=user, thread_name=thread_name, message=message, timestamp=time)
        