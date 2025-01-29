const id = JSON.parse(document.getElementById('json-username').textContent);
const message_username = JSON.parse(document.getElementById('json-message-username').textContent);

const socket = new WebSocket('ws://' + window.location.host + '/ws/' + id + '/');

socket.onopen = function (e) {
    console.log('Connection established');
}

socket.onclose = function (e) {
    console.error('Connection closed');
}

socket.onerror = function (e) {
    console.error(e);
}

socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data);
    
    const formatter = new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true,
        timeZone: 'Asia/Kolkata'
    });
    
    data.time = formatter.format(new Date(data.time)).replace(',', '.').replace(' at', ',');

    //change the time in this format Jan. 27, 2025, 12:21 p.m.

    const date = new Date(data.time);
    const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    


    if(data.username === message_username){
        document.getElementById('chatMessages').innerHTML+= '<div class="message sent"><p>'+data.message+'</p><small>'+data.time+'</small></div>'; 
    }
    else{
        document.getElementById('chatMessages').innerHTML+= '<div class="message received">'+data.message+'</p><small>'+data.time+'</small></div>'; 
    }

}


document.querySelector("#sendMessage").onclick = function (e) {

    const message_input = document.querySelector('#newMessage');
    const message = message_input.value;
    

    if (message.trim()) {
        const localTime = new Date();
        const displayTime = localTime.toISOString();
        
        socket.send(JSON.stringify({
            'message': message,
            'username': message_username,
            'time': displayTime
        }));
        
        message_input.value = '';
    }

}