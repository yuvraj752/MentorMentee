from channels.generic.websocket import WebsocketConsumer
import json

class Chat(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'type': 'connection successful',
            'message': 'you are now connected'
        }))

    def receive(self, text_data):
        json_data = json.loads(text_data)
        message = json_data['message']
        print(message)
