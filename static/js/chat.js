var ws;
currentConnection = 'none'
const token = localStorage.getItem('token');
var chatMessages = document.getElementById('chat-messages');
var newMessage 
function toggleDropdown() {
     document.getElementById('dropdown-content').style.display === 'block' ;
     document.getElementById('dropdown-content').style.display = 'none' ;
     document.getElementById('dropdown-content').style.display = 'block';
}

function changePerson(person, id, uniqueId) {
    document.getElementById('current-person').textContent = `Chatting with: ${person}`;
    document.getElementById('selected-person').textContent = person;
    document.getElementById('dropdown-content').style.display = 'none';
    document.getElementById('chat-messages').innerHTML = '';
    currentConnection = uniqueId
    get_messages(id)

    //ws.close();
    connectReceiver(id)
}
function getPerson(){
    var url = 'http://localhost:8000/users/'
    fetch(url, {
        headers: {
            'Authorization' : 'Bearer ' + token,
            'Content-Type' : 'application/json'
        },
         }).then(res => {
        if(res.status === 200){
            if(url === res.url){
                return res.json()
            }
            else{
                window.location.href = res.url
            }
            
        }else{
           window.location.href = res.url 
  
         }
    }).then(data => {
        data.forEach(person => {
            markup = `<span class = "dropdown-item" onclick = "changePerson('${person.user_name}', '${person.id}', '${person.uniqueId}')"
            >${person.user_name}</span>`

            document.querySelector('#dropdown-content').insertAdjacentHTML('beforeend', markup)
        })
        })
}

function get_messages(receiver){
    fetch(`http://localhost:8000/message/${receiver}`, {
        headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + token
        }
        }).then(res => {
            if(res.status === 200){
                return res.json()
            }else{
                window.location.href = 'http://localhost:8000/Login'
            }
        }).then(data => {
            data.forEach(text => {
                var messages = document.createElement('p')
                messages.textContent = `${text.sender_name}: ${text.message}`
                if(text.sender_name === "You"){
                    messages.style.color = '#4CAF50'
                }else{
                    messages.style.color = '#92C7CF'
                }
                chatMessages.appendChild(messages)
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
    
    messageInput.value = '';
}

function connectReceiver(id) {
    ws = new WebSocket(`ws://localhost:8000/ws/${id}?token=${token}`);
    ws.onmessage = function(event) {
        newMessage = document.createElement('p')
        var data = JSON.parse(event.data)
        if(data.id != currentConnection){
            alert(`${data.sender_name} send a message`)
        }else{
            newMessage.textContent =`${data.sender_name}: ${data.message}`;
            newMessage.style.color = "#063970"
            chatMessages.appendChild(newMessage);
        }
    }
    ws.onerror = function(event){
       window.location.href = 'http://localhost:8000/Login'
    }
}
getPerson()        
