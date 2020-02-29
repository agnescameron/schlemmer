import * as Tone from "tone";
import $ from "jquery";
import * as io from "socket.io-client";
import pickle from 'pickle';

console.log('wahey!')

const namespace = '/test';
const socket = io(namespace);

let context = new AudioContext();

function startStream() {
	socket.emit('broadcast');
}

// Play the loaded file
function play() {
    // Create a source node from the buffer
    var source = context.createBufferSource();
    source.buffer = buf;
    // Connect to the final output node (the speakers)
    source.connect(context.destination);
    // Play immediately
    source.start(0);
}


function playByteArray(byteArray) {
    var arrayBuffer = new ArrayBuffer(byteArray.length);
    var bufferView = new Uint8Array(arrayBuffer);
    for (let i = 0; i < byteArray.length; i++) {
      bufferView[i] = byteArray[i];
    }

    context.decodeAudioData(arrayBuffer, function(buffer) {
        buf = buffer;
        play();
    });
}


socket.on('stream', function(message) {
	console.log('starting stream....', message);
	playByteArray(message.data);
});

$(document).ready(function(){
	socket.on('connect', function() {
		console.log('client connected')
	    socket.emit('hello', {data: 'I\'m connected!'});
	});
});
