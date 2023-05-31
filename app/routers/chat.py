from jinja2 import Template
from .. import websocket
import json
from fastapi import FastAPI, Request, Response, WebSocket, WebSocketDisconnect, APIRouter

router = APIRouter()

manager = websocket.ConnectionManager()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            data = {
                "client_id": client_id,
                "message": message
            }
            data = json.dumps(data)
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        data = {
            'client_id': client_id,
            'message': "left the chat"
            }
        data = json.dumps(data)
        await manager.broadcast(data)