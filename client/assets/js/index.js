var context = new AudioContext()
var freqarray = [2880, 2544, 5296, 544, 1008, 4448, 11216, 8368, 2144, 4016, 11040, 5664, 11312, 7568, 11696];

var o = context.createOscillator()
var  g = context.createGain()
var frequency = freqarray[0];
o.connect(g)
g.connect(context.destination)
o.start(0)
var i=0

var body = document.getElementById('body')
console.log(body)

function changeSound() {
	o.frequency.value = freqarray[i%15];
	i++;
	// colour = '#' +freqarray[i%15].toString(16);
	// console.log(colour);
	// body.style.backgroundColor = colour;
}

setInterval(changeSound, 1000);

// One-liner to resume playback when user interacted with the page.
document.addEventListener('click', function() {
  context.resume().then(() => {
    console.log('Playback resumed successfully');
  });
});