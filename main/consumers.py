from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Check if the user is authenticated
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            # Join the user-specific notification group
            await self.channel_layer.group_add(
                f"notifications_{self.user.id}",
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            # Leave the notification group
            await self.channel_layer.group_discard(
                f"notifications_{self.user.id}",
                self.channel_name
            )

    async def receive(self, text_data):
        # Not handling incoming WebSocket messages in this example
        pass

    # This is the function that will send notifications to the user
    async def send_notification(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
