import serial
import threading
import pygame as pg
import math
import time
import re

numSounds = 3
drums = []


ser = serial.Serial('/dev/cu.usbmodem1421', 115200)

pg.mixer.init(frequency=44100, size=-16, channels=numSounds, buffer=512)
pg.init()


#good is drones, drills;
for i in range(0, numSounds):
	drum = pg.mixer.Sound("../../sounds/percussion/%d.wav" %i)
	drums.append(drum)

event = [1] * numSounds
global lastnorm

def threshold(data):
	norm = abs(math.sqrt( int(data[1])**2 + int(data[2])**2 + int(data[3])**2 )-16000)
	return norm

def compare(data):
	global lastnorm
	norm = abs(math.sqrt( int(data[1])**2 + int(data[2])**2 + int(data[3])**2 )-16000)
	compNorm = abs(lastnorm - norm)
	return compNorm


def getSerial(arg):
	while True:
		ser.flushInput()
		line = ser.readline().decode("utf-8")
		data = line.split();
		print(data)
		if(len(data) == 4):
			event[int(data[0])] = threshold(data)
			#event[0] = threshold(data)
			print(event)

def channel(num, pause):
	while True:
		if(event[num]>1000):
			print(num)
			drums[num].play()
			time.sleep(1)

if __name__ == "__main__":
	lastnorm = 0
	thread = threading.Thread(target=getSerial, args=(0, ))
	thread.start()

	for i in range (0, len(drums)):
		thread = threading.Thread(target=channel, args=(i, i))
		thread.start()
