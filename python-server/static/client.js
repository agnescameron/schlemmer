	namespace = '/test';
	var socket = io(namespace);

	function startStream() {
		socket.emit('broadcast');
	}

	socket.on('stream', function(event) {
		console.log('starting stream.... volume is', event.data)
	});

	$(document).ready(function(){
		socket.on('connect', function() {
			console.log('client connected')
		    socket.emit('hello', {data: 'I\'m connected!'});
		});
	});

	const osc = new Tone.Oscillator(440, "sine").toMaster();

//attach a click listener to a play button
document.getElementById('button').addEventListener('click', async () => {
	await Tone.start();
	document.getElementById('button').innerHTML = 'audio ready'
	osc.start();
})
