namespace = '/test';
const socket = io(namespace);
let player;


function startStream() {
	socket.emit('broadcast');
}

socket.on('stream', function(event) {
	console.log('starting stream.... volume is', event.data)
});

socket.on('vol', function(event) {
	// player.volume.value = event.data.volume;
	console.log("volume now", event.data);
	setTimeout(() => { socket.emit('volRequest'); }, 1000);
});

//attach a click listener to a play button
$('#button').click( async function () {
	await Tone.start();
	player.start();
	socket.emit('volRequest');
});

$('#volDown').click(function () {
	player.volume.value = player.volume.value-1;
	console.log("volume now", player.volume.value);
});

$('#volUp').click(function () {
	player.volume.value = player.volume.value+1;
	console.log("volume now", player.volume.value);
});


$(document).ready(function(){
	//connect websocket
	socket.on('connect', function() {
		console.log('client connected')
	    socket.emit('hello', {data: 'I\'m connected!'});
	});

	//connect web player
	player = new Tone.Player({
		'url': 'static/0.wav',
		'loop': 'true',
		'volume': 10
	}).toMaster();
});