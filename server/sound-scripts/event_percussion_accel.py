import logging
import threading
import pygame as pg
import math
import time
import re

numSounds = 6
drums = []

pg.mixer.init(frequency=44100, size=-16, channels=numSounds, buffer=512)
pg.init()


#good is drones, drills;
for i in range(0, numSounds):
	drum = pg.mixer.Sound("../../sounds/kung-fu/%d.wav" %i)
	drums.append(drum)

event = [1] * numSounds
global lastnorm

def threshold(data):
	norm = abs(math.sqrt( int(data[0])**2 + int(data[1])**2 + int(data[2])**2 )-16000)
	return norm

def compare(data):
	global lastnorm
	norm = abs(math.sqrt( int(data[0])**2 + int(data[1])**2 + int(data[2])**2 )-16000)
	compNorm = abs(lastnorm - norm)
	return compNorm


def printFile(arg):
	while True:
		file = open("../accelo-live.txt", 'r')
		for line in file:
			data = line.split()
			if(len(data) == 4):
				event[int(data[3])] = compare(data)
			time.sleep(0.01)
		file.close()

def channel(num, pause):
	while True:
		if(event[num]>6000):
			drums[num].play()
			time.sleep(0.2)			

if __name__ == "__main__":
	lastnorm = 0
	thread = threading.Thread(target=printFile, args=(0, ))
	thread.start()

	for i in range (0, len(drums)):
		thread = threading.Thread(target=channel, args=(i, i))
		thread.start()
