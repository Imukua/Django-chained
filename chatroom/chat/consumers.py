import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        #Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        #Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    
    #receive message from websocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        #send message eto room group

        await self.channel_layer.group_send(self.room_group_name, {"type": "chat_message", "message":message})


    #receive mesage from room group
    async def chat_message(self, event):
        message = event["message"]


        #send message to websocket
        await self.send(text_data=json.dumps({"message":message}))

        
