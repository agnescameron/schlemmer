
$(document).ready(function(){

	namespace = '/test';
	var socket = io(namespace);

	socket.on('connect', function() {
		console.log('client connected')
	    socket.emit('hello', {data: 'I\'m connected!'});
	});
});