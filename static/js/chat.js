var ws;
const token = localStorage.getItem('token');
var chatMessages = document.getElementById('chat-messages');
var newMessage 
function toggleDropdown() {
     document.getElementById('dropdown-content').style.display === 'block' ;
     document.getElementById('dropdown-content').style.display = 'none' ;
     document.getElementById('dropdown-content').style.display = 'block';
}

function changePerson(person, id) {
    document.getElementById('current-person').textContent = `Chatting with: ${person}`;
    document.getElementById('selected-person').textContent = person;
    document.getElementById('dropdown-content').style.display = 'none';
    document.getElementById('chat-messages').innerHTML = '';

    //ws.close();
    connectReceiver(id)
}
function getPerson(){
    fetch('http://localhost:8000/users', {
        headers: {
            'Authorization' : 'Bearer ' + token,
            'Content-Type' : 'application/json'
        }
    }).then(res => {
        if(res.status === 401){
            window.location.href = 'http://localhost:8000/Login'
        }else{
            return res.json()
        }
    }).then(data => {
        data.forEach(person => {
            markup = `<span class = "dropdown-item" onclick = "changePerson('${person.user_name}', '${person.id}')"
            >${person.user_name}</span>`

            document.querySelector('#dropdown-content').insertAdjacentHTML('beforeend', markup)
        })
        })
}

function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value;
    if (message.trim() === '') {
        return;
    }

    chatMessages = document.getElementById('chat-messages');
    newMessage = document.createElement('p');
    newMessage.textContent = `You: ${message}`;
    newMessage.style.color = '#4CAF50';
    chatMessages.appendChild(newMessage);
    ws.send(JSON.stringify(message));
    
    document.getElementById("messageText").value = '';
    event.preventDefault();
    messageInput.value = '';
}

function connectReceiver(id) {
    ws = new WebSocket(`ws://localhost:8000/ws/${id}?token=${token}`);
    ws.onmessage = function(event) {
        newMessage = document.createElement('p')
        var data = JSON.parse(event.data)
        newMessage.textContent =`${data.sender_name}: ${data.message}`;
        newMessage.style.color = "#063970"
        chatMessages.appendChild(newMessage);
    }
    ws.onerror = function(event){
       window.location.href = 'http://localhost:8000/Login'
    }
}
getPerson()        
