var socket

var messaged = function(data) {
  switch (data.action) {
    case 'in-use':
    alert('Name is in use, please choose another');
    break;
    case 'started':
    started = true;
    $('#submit').val('Send');
    $('#users').slideDown();
    $.each(data.users, function(i, name) {
      addUser({name: name});
    });
    break;
    case 'join':
    addUser(data, true);
    break;
    case 'leave':
    removeUser(data);
    break;
    case 'message':
    addMessage(data);
    break;
    case 'system':
    data['name'] = 'SYSTEM';
    addMessage(data);
    break;
  }
};

var connected = function(){
  socket.send({ action : start })
};

var disconnect = function(){
  socket.send({ action : stop })
};

var receiveData = function(){
	socket.send({ action : send })
}

var start = function(){
  socket = new io.Socket();
  socket.connect();
  socket.on('connect', connected);
  socket.on('disconnect', disconnected);
  socket.on('message', receiveData);
};

start();
