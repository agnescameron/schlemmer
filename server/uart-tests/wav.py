import wave
import pyaudio

p = pyaudio.PyAudio()
punch = wave.open("../../sounds/kung-fu/punch1.wav")

chunk_size = 1024



stream = p.open(format=p.get_format_from_width(punch.getsampwidth()), 
	channels=punch.getnchannels(), rate=punch.getframerate(), output=True)

data = punch.readframes(1024)

while len(data) > 0:
	stream.write(data)
	data=punch.readframes(1024)
