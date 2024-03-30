import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat, User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = self.scope["url_route"]["kwargs"]["room"]
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        username = data['username']
        user = await self.get_user(username)
        room = data['room']
        message = data['chat']
        chat = await self.save_chat(user, room, message)
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'chat_message', 'chat': chat.message,
                'created': chat.created, 'fullName': user.first_name,
            }
        )
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat', 'chat': event['chat'],
            'created': event['created'].strftime("%B %d, %Y, %I:%M %p"),
            'fullName': event['fullName'].title()
        }))
    
    @database_sync_to_async
    def save_chat(self, user, room, message):
        return Chat.objects.create(user=user, room=room, message=message)

    @database_sync_to_async
    def get_user(self, username):
        return User.objects.get(username=username)
