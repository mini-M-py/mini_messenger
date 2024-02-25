from fastapi import WebSocket
import json
from . import utils

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, user_id:str):
        try:
            await websocket.accept()
            self.active_connections[user_id] = websocket
        except:
            print('couldnot connect')

    def disconnect(self, user_id:str):
        try:
            del self.active_connections[user_id]
        except:
            print('closing anyway')
     

    async def send_personal_message(self, message: str, receiver_id:int, sender:str ,sender_name:str):
        websocket = self.active_connections.get(int(receiver_id))
        enc_sender = str(utils.encrypt(sender))
        if websocket:
            data = {
                'sender':enc_sender,
                'message': message,
                'sender_name': sender_name
            }
            data = json.dumps(data)
            await websocket.send_text(data)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)
