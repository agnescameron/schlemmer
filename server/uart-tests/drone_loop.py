import logging
import threading
import pygame as pg
import math
import time
import re

numSounds = 6

pg.mixer.init(frequency=44100, size=-16, channels=numSounds, buffer=4096)
pg.init()
pg.mixer.set_num_channels(5)

drones = []
buffer = [0]*20


#good is drones, drills;
for i in range(0, numSounds):
	drone = pg.mixer.Sound("../../sounds/drills/%d.wav" %i)
	drones.append(drone)

vol = [0.1, 0.1, 0.1, 0.1, 0.1]
global lastnorm

def thresholdAll(data):
	norm = abs(math.sqrt( int(data[0])**2 + int(data[1])**2 + int(data[2])**2 )-16000)
	print (norm)

	if(norm > 100000):
		volume = vol[int(data[3])]

	volume = norm/2000

	return volume


def compare(data):
	global lastnorm
	norm = abs(math.sqrt( int(data[0])**2 + int(data[1])**2 + int(data[2])**2 ))
	compNorm = abs(lastnorm - norm)
	print(compNorm)

	if (compNorm == 0.0):
		volume = vol[int(data[3])]

	else:
		volume = compNorm/3000

	lastnorm = norm
	return volume

def moving_average(data, bufSize):
	norm = abs(math.sqrt( int(data[0])**2 + int(data[1])**2 + int(data[2])**2 )-16000)
	buffer.append(norm)
	avBuffer = buffer[-bufSize:]
	movingAv = sum(avBuffer)/bufSize
	print(movingAv)
	return movingAv/3000


def printFile():
	while True:
		file = open("../accelo-live.txt", 'r')
		for line in file:
			data = line.split()
			if(len(data) == 4):
				vol[int(data[3])] = moving_average(data, 60)
			time.sleep(0.05)
		file.close()

def channel(num):
	while True:
		drones[num].set_volume(vol[num])
		print(vol[num])
		drones[num].play(loops=-1)

if __name__ == "__main__":
	lastnorm = 0
	thread = threading.Thread(target=printFile)
	thread.start()

	for i in range (0, len(drones)):
		thread = threading.Thread(target=channel, args=(i, ))
		thread.start()
