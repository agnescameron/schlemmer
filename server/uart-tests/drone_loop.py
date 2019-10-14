import logging
import threading
import pygame as pg
import math
import time
import re

pg.mixer.init()
pg.init()
pg.mixer.set_num_channels(1)

drones = []
buffer = [0]*20

for i in range(2, 3):
	drone = pg.mixer.Sound("../../sounds/drones/drone%d.wav" %i)
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
		volume = compNorm/2000

	lastnorm = norm
	return volume

def moving_average(data):
	norm = abs(math.sqrt( int(data[0])**2 + int(data[1])**2 + int(data[2])**2 )-16000)
	buffer.append(norm)
	avBuffer = buffer[-20:]
	movingAv = sum(avBuffer)/20
	print(movingAv)
	return movingAv/2000


def printFile(arg):
	while True:
		file = open("../accelo-live1.txt", 'r')
		for line in file:
			data = line.split()
			if(len(data) == 4):
				vol[int(data[3])] = moving_average(data)
			time.sleep(0.05)
		file.close()

def channel(num, pause):
	while True:
		drones[num].set_volume(vol[num])
		drones[num].play(loops=-1)

if __name__ == "__main__":
	lastnorm = 0
	thread = threading.Thread(target=printFile, args=(0, ))
	thread.start()

	for i in range (0, len(drones)):
		thread = threading.Thread(target=channel, args=(i, i))
		thread.start()
