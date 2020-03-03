namespace = '/test';
const socket = io(namespace);
let player;


function startStream() {
	socket.emit('broadcast');
}

socket.on('stream', function(event) {
	console.log('starting stream.... volume is', event.data)
});


//attach a click listener to a play button
$('#button').click( async function () {
	await Tone.start();
	document.getElementById('button').innerHTML = 'audio ready'
	player.start();
})

$(document).ready(function(){
	//connect websocket
	socket.on('connect', function() {
		console.log('client connected')
	    socket.emit('hello', {data: 'I\'m connected!'});
	});

	//connect web player
	player = new Tone.Player('static/0.wav').toMaster();
});