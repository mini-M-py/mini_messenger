import json
from fastapi import FastAPI, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
html = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        #input{
            position: fixed;
            top: 0;
            height: 200px;
            background-color: skyblue;
            width: 100%;
            border-color: black;
            border-radius: 9px;
        }
        #messageText{
            margin-top: 20px;
            height: 30px;
            font-size: 16px;
        }

        #message-text {
            padding: 5px;
        }

        #send-button {
            padding: 5px 10px;
            background-color: rgb(56, 175, 223);
            border: none;
            color: white;
            cursor: pointer;
            height: 30px;
        }

        .conversation-message {
            background-color: rgb(193, 201, 201);
            border-radius: 4px;
            padding: 3px;
            margin-top: 10px;
            display: inline-block;
        }

        .conversation-message.sent-message {
            background-color: rgb(56, 175, 223);
            color: white;
            float: right;
        }

        .BOX {
            background-color: rgb(193, 201, 201);
            height: auto;
            width: auto;
            border-radius: 4px;
            line-height: 1.5;
            width: auto;
            margin-top: 10px;
            padding: 10px;
            display: block;
            clear: both;

        }

        .username {
            color: crimson;
            padding: 3px;
            margin-left: 5px;
            margin-top: 5px;
        }

        .txt {
            margin-left: 6px;
        }

        .message {
            padding: 10px;
        }

        #sender {
            float: left;
        }

        #me {
            float: right;
            margin-top: 80px;
        }

        #message-input {
            position: fixed;
            width: 100%;
            background-color: aqua;
            margin-top: 0px;
            height: 30px;
        }
        .conversation-container {
            position: fixed;
            bottom: 0;
            width: 100%;
            height: 50%;
            overflow-y: scroll;
            padding: 10px;
            box-sizing: border-box;
        }

    </style>
    <title>Chat</title>
</head>

<body>
    <div id="input">
        <h1>Unique Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off" />
            <button id="send-button">Send</button>
        </form>
    </div>
    
    <div id="conversation" class="conversation-container"></div>
    <script>
        var conversationDiv = document.getElementById('conversation');

        function scrollToBottom() {
            conversationDiv.scrollTop = conversationDiv.scrollHeight - conversationDiv.clientHeight;
        }
        function handleResize() {

            isScrollAtBottom = conversationDiv.scrollHeight - conversationDiv.scrollTop === conversationDiv.clientHeight;
        }
        var client_id = Date.now()
        document.querySelector("#ws-id").textContent = client_id
        var ws = new WebSocket(`wss://${location.host}/ws/${client_id}`)
        ws.onmessage = function (event) {
            var data = JSON.parse(event.data)
            console.log(data)
            var clientId = data.client_id
            console.log(clientId)
            var message = data.message
            if (clientId === client_id) {
                clientId = "me";
                var myMessage = document.createElement('div');
                myMessage.id = 'me';
                myMessage.classList.add('BOX');
                var myID = document.createElement('div');
                myID.classList.add('username');
                myID.textContent = clientId;
                myMessage.appendChild(myID);
                var myTxt = document.createElement('div');
                myTxt.classList.add('txt');
                myTxt.textContent = message;
                myMessage.appendChild(myTxt);

                var conversationDiv = document.getElementById('conversation');
                conversationDiv.appendChild(myMessage);
            }
            else {
                var clientMessage = document.createElement('div');
                clientMessage.classList.add('BOX');
                clientMessage.id = 'sender';

                var clientIdElement = document.createElement('div');
                clientIdElement.classList.add('username');
                clientIdElement.textContent = clientId;
                clientMessage.appendChild(clientIdElement);

                var clientText = document.createElement('div');
                clientText.classList.add('txt');
                clientText.textContent = message;
                clientMessage.appendChild(clientText);

                var conversationDiv = document.getElementById('conversation');
                conversationDiv.appendChild(clientMessage);

            }
            scrollToBottom()
        }
        function sendMessage(event) {
            event.preventDefault()
            var input = document.getElementById("messageText")
            ws.send(input.value)
            input.value = ''
        }
        window.addEventListener('resize', handleResize);
    </script>
</body>

</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(html)

@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)

@app.websocket("/ws/{client_id}")
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
