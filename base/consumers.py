import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat, User, ChatRoom
from django.contrib.humanize.templatetags.humanize import naturaltime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = self.scope["url_route"]["kwargs"]["chat_room"]
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        sender_username = data['senderUsername']
        reciever_username = data['recieverUsername']
        chat_room = data['chatRoom']
        message = data['chat']
        sender = await self.get_sender(sender_username)
        reciever = await self.get_reciever(reciever_username)
        room = await self.get_chat_room(chat_room)
        chat = await self.save_chat(sender, reciever, room, message)
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'chat_message', 'chat': message,
                'senderUsername': sender_username, 
                'recieverUsername': reciever_username, 
                'fullName': sender.first_name, 'created': chat.created,
            }
        )
    
    async def chat_message(self, event):
        created = str(naturaltime(event['created'])).title()
        await self.send(text_data=json.dumps({
            'chat': event['chat'],
            'senderUsername': event['senderUsername'], 
            'recieverUsername': event['recieverUsername'],
            'fullName': event['fullName'].title(), 'created': created,
        }))
    
    @database_sync_to_async
    def get_sender(self, sender_username):
        return User.objects.get(username=sender_username)
    
    @database_sync_to_async
    def get_reciever(self, reciever_username):
        return User.objects.get(username=reciever_username)

    @database_sync_to_async
    def get_chat_room(self, name):
        return ChatRoom.objects.get(name=name)

    @database_sync_to_async
    def save_chat(self, sender, reciever, room, message):
        return Chat.objects.create(
            sender=sender, reciever=reciever, room=room, message=message
        )
