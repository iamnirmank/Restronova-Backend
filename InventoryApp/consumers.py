# consumers.py
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class Consumer(WebsocketConsumer):
    def connect(self):
        try:
            self.room_group_name = 'InventoryApp'
            self.room_name = 'InventoryAlerts'
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept()
            self.send(text_data=json.dumps({'type': 'connection', 'message': 'Connected'}))
        except Exception as e:
            print(f"WebSocket connection failed: {str(e)}")

    def send_inventory_alerts(self, event):
        alert_data = event['value']
        event_type = event['type']
        self.send(text_data=json.dumps({'type': event_type, 'value': alert_data}))
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        self.send(text_data=json.dumps({'type': 'connection', 'message': 'Disconnected'}))