
$(document).ready(function() {
    //var socket = io.connect('http://' + document.domain + ':' + location.port); //replace with the legit ip later
    var socket = io.connect('http://127.0.0.1:5000'); //replace with the legit ip later

    socket.on('connect', function() { //send a message to the server when connection is initiated
        socket.send('Hi, user here! I am connected!');
    });

    socket.on('echo', function(data){ //the server will send back anything sent using socket.send as an echo
        document.getElementById("log").innerHTML += data.data+"<br>";
    });
    
    $('#boopbutton').on('click', function() { //press the button to test connection
        socket.send('Boop');
    });

    $('#carconnect').on('click', function() { //press the button to connect server to cars
        socket.emit("carconnect", {});
    });
    
    $(document).keydown(function(e) { //transmit all keypress data to the server for it to deal with
        var code = e.keyCode || e.which;
	socket.emit("keydown", {id:code});
    });
    
    $(document).keyup(function(e) {
        var code = e.keyCode || e.which;
	socket.emit("keyup", {id:code});
    });
});

