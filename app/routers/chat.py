from typing import Annotated
from .. import websocket, oauth2
import json
from fastapi import Query, WebSocket, WebSocketDisconnect, APIRouter, Depends, status, WebSocketException

router = APIRouter()

manager = websocket.ConnectionManager()

async def get_token(
        websocket: WebSocket,
        token: Annotated[str | None, Query()] = None
):
    if token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    else:
        user_id = await oauth2.get_current_user(token)

        return user_id

@router.websocket("/ws/{receiver_id}")
async def websocket_endpoint(websocket: WebSocket,  receiver_id: int ,user_id: Annotated[str, Depends(get_token)],):


    if user_id:
        current_id = int(user_id.id)  # Assuming user_id is an integer
        await manager.connect(websocket, current_id)

        try:
            receiver = None
            while True:
                message = await websocket.receive_text()
                data = json.loads(message)
                sender = current_id
            
                receiver = receiver_id

                message_text = data.get("message", "")
                await manager.send_personal_message(message_text, receiver, sender)
        except WebSocketDisconnect:
            manager.disconnect(current_id)
            # data = {
            #     'sender': "server",
            #     'message': "left the chat"
            #     }
            # data = json.dumps(data)
            # await manager.broadcast(data)


