import logging
import threading
import pygame as pg
import math
import time
import re

numSounds = 1

pg.mixer.init(frequency=44100, size=-16, channels=numSounds, buffer=4096)
pg.init()

drones = []
dataBuffer = [0]*20


#good is drones, drills;
for i in range(0, numSounds):
	drone = pg.mixer.Sound("../../sounds/drills/%d.wav" %i)
	drones.append(drone)

vol = [0.1, 0.1, 0.1, 0.1, 0.1]
global lastnorm

def thresholdAll(data):
	norm = int(data[0])-2250
	if(norm<0): norm=0

	if(norm > 10000):
		volume = vol[int(data[1])]

	volume = norm/100

	return volume


def compare(data):
	global lastnorm
	norm = int(data[0])
	compNorm = abs(lastnorm - norm)
	print(compNorm)

	if (compNorm == 0.0):
		volume = vol[int(data[1])]

	else:
		volume = compNorm/100

	lastnorm = norm
	return volume

def moving_comparative_average(data, bufSize):
	global lastnorm
	norm = int(data[0])
	compNorm = abs(lastnorm - norm)/100
	dataBuffer.append(compNorm)
	avBuffer = dataBuffer[-bufSize:]
	movingAv = sum(avBuffer)/bufSize
	print(movingAv)
	return movingAv/100


def moving_threshold_average(data, bufSize):
	norm = abs(int(data[0])-2250)
	dataBuffer.append(norm)
	avBuffer = dataBuffer[-bufSize:]
	movingAv = sum(avBuffer)/bufSize
	print(movingAv)
	return movingAv/200

def printFile():
	while True:
		file = open("../flex-live.txt", 'r')
		for line in file:
			data = line.split()
			if(len(data) == 2):
				vol[int(data[1])] = moving_threshold_average(data, 30)
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
