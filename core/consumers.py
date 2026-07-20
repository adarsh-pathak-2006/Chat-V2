import json

from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer

from django.db.models import Q

from core.models import Chat, Conversation


class ChatConsumer(WebsocketConsumer):

    def connect(self):

        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]

        self.room_group_name = f"chat_{self.chat_id}"

        user = self.scope["user"]

        if not user.is_authenticated:
            self.close()
            return

        self.chat = Chat.objects.filter(id=self.chat_id).first()

        if not self.chat or (user != self.chat.user and user != self.chat.user2):
            self.close()
            return

        async_to_sync(
            self.channel_layer.group_add
        )(
            self.room_group_name,
            self.channel_name,
        )

        self.accept()

    def disconnect(self, close_code):

        async_to_sync(
            self.channel_layer.group_discard
        )(
            self.room_group_name,
            self.channel_name,
        )

    def receive(self, text_data):

        data = json.loads(text_data)

        message = data["message"]

        conversation = Conversation.objects.create(
            chat=self.chat,
            user=self.scope["user"],
            message=message,
        )

        async_to_sync(
            self.channel_layer.group_send
        )(
            self.room_group_name,
            {
                "type": "chat_message",

                "message": conversation.message,

                "username": conversation.user.username,

                "time": conversation.time.strftime("%H:%M:%S"),
            },
        )

    def chat_message(self, event):

        self.send(
            text_data=json.dumps(
                {
                    "username": event["username"],

                    "message": event["message"],

                    "time": event["time"],
                }
            )
        )