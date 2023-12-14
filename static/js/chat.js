var conversationDiv = document.getElementById('conversation');

function scrollToBottom() {
    conversationDiv.scrollTop = conversationDiv.scrollHeight - conversationDiv.clientHeight;
}
function handleResize() {
    isScrollAtBottom = conversationDiv.scrollHeight - conversationDiv.scrollTop === conversationDiv.clientHeight;
}
var client_id = Date.now()
function home(token){
    fetch(`http://127.0.0.1:8000/`,{
        headers: {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }
    }).then(res => {
        if (res.status === 401) {
            window.location.href = 'login.html'
        } else {
            return res.json();
        }
    })
}
var token = localStorage.getItem('token')
var sendBtn = document.getElementById('send-button')

sendBtn.onclick = sendMessage
console.log('token ' + token)
home(token)
document.querySelector("#ws-id").textContent = client_id
var ws = new WebSocket(`ws://${location.host}/ws/${client_id}`,{
})
ws.onmessage = function (event) {
    var token = localStorage.getItem('token')
    ws.setRequestHeader('Authorization', 'Bearer ' + token)
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
    var receiver = document.getElementById('receiver').value
    var message = {
        'message': input.value,
        'sender':client_id,
        'receiver': receiver
    }
    data = JSON.parse(message)
    ws.send(data)
    input.value = ''
}

window.addEventListener('resize', handleResize);