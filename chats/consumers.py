import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chats.models import ChatModel, UserProfileModel, ChatNotification
from django.contrib.auth.models import User


class ChatPersonalConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        other_user_id = self.scope["url_route"]['kwargs']['id']
        chat_id = self.scope['url_route']['kwargs']['chat_id']

        if not chat_id or not user.is_authenticated:
            await self.close()

        self.room_group_name = f"chat_{chat_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        receiver = data['receiver']

        await self.save_message(username, self.room_group_name, message, receiver)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
                "receiver": receiver
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username
                 }

            )
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def save_message(self, username, thread_name, message, receiver):
        chat_obj = ChatModel.objects.create(
            sender=username,
            thread_name=thread_name,
            message=message
        )

        other_user_id = self.scope["url_route"]['kwargs']['id']
        get_user = User.objects.get(id=other_user_id)

        if receiver == get_user.username:
            ChatNotification.objects.create(chat=chat_obj, user=get_user)

