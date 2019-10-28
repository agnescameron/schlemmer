import threading
import pygame as pg
import math
import time
import serial
import re

numSounds = 1

ser = serial.Serial('/dev/cu.usbmodem1421', 115200)

pg.mixer.init(frequency=44100, size=-16, channels=numSounds, buffer=4096)
pg.init()

drones = []
channels = []
buffer = [0]*20


#good is drones, drills;
for i in range(0, numSounds):
	channel = pg.mixer.Channel(i)
	channels.append(channel)
	drone = pg.mixer.Sound("../../../sounds/rehearsal-test/1.wav")
	drones.append(drone)

norm = [1]*numSounds
global lastnorm

def threshold(data):
	norm = abs(math.sqrt( int(data[1])**2 + int(data[2])**2 + int(data[3])**2 )-16000)
	# print (norm)

	if(norm > 100000):
		volume = vol[int(data[3])]

	return norm


def printFile():
	while True:
		line = ser.readline().decode("utf-8")
		data = line.split();
		print(data)
		if(len(data) == 4):
			norm[int(data[0])] = threshold(data)

def channel(num):
	channels[num].play(drones[num], loops=-1)
	playing = True
	while True:
		#if no sound playing on the channel and 
		#movement above threshold
		if(norm[num] > 4000 and not playing):
			channels[num].unpause()
			playing = True

		#if sound playing on the channel and
		#movement below threshold		
		if(norm[num] < 4000 and playing):
			channels[num].pause()
			playing = False
		
		time.sleep(0.05)

if __name__ == "__main__":
	lastnorm = 0
	thread = threading.Thread(target=printFile)
	thread.start()

	for i in range (0, numSounds):
		thread = threading.Thread(target=channel, args=(i, ))
		thread.start()
