
$(document).ready(function() {
    
    //var socket = io.connect('http://' + document.domain + ':' + location.port); //replace with the legit ip later
    var socket = io.connect('http://127.0.0.1:5000'); //replace with the legit ip later

    socket.on('connect', function() {
        socket.send('Hi, user here! I am connected!');
    });
    
    $('#boopbutton').on('click', function() {
        socket.send('Boop');
    });
    
    $(document).keydown(function(e) {
        var code = e.keyCode || e.which;
        socket.send(code.toString());
    });
    
    $(document).keyup(function(e) {
        var code = e.keyCode || e.which;
        socket.send((-code).toString());
    });
});

