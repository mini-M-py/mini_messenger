from typing import Annotated
from .. import websocket, oauth2, model, utils
from ..database import get_db
from sqlalchemy.orm import Session
import json
from fastapi import Query, WebSocket, WebSocketDisconnect, APIRouter, Depends, status, WebSocketException, HTTPException

router = APIRouter()

manager = websocket.ConnectionManager()

async def get_token(
          websocket: WebSocket,
          token: Annotated[str | None, Query()] = None
):
    if token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    
    return token

@router.websocket("/ws/{receiver}")
async def websocket_endpoint(websocket: WebSocket,  receiver: str, token: str = Depends(get_token), db: Session = Depends(get_db) ):
        
        receiver_id = utils.decrypt(receiver)
                        
        user_id = oauth2.get_current_user_websocket(token)
        if user_id == None:
              
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason = "Inavlaid Token")

        
        current_id = int(user_id.id)  # Assuming user_id is an integer

        sender_name = db.query(model.User.user_name).filter(model.User.id == current_id).scalar()
        receiver_id = db.query(model.User.id).filter(model.User.id == receiver_id).scalar()
        if receiver_id == None:
         
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason = "Inavalid receiver")

        await manager.connect(websocket, current_id)

        try:
            receiver = None
            while True:
                message = await websocket.receive_text()
                data = json.loads(message)
                sender = current_id
            
                receiver = receiver_id
                message_text = data
                await manager.send_personal_message(message_text, receiver, sender, sender_name)
                new_chat = model.Chat(sender_id= current_id, receiver_id= receiver_id, chat = message_text)
                db.add(new_chat)
                db.commit()
        except WebSocketDisconnect:
            manager.disconnect(current_id)
            
@router.get("/message/{receiver_id}")
def get_message( db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), reveiver_id: int )

    messages = db.query(model.Chat, case([(model.Chat.sender_id == user_id.id, "You")], else_=model.User.user_name).label("sender_name"))
        .join(model.User, model.User.id == model.Chat.receiver_id)
        .filter((model.Chat.sender_id == user_id.id) & (model.Chat.receiver_id == receiver_id)).all()

    return  messages
