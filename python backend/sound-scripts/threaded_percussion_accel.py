import logging
import threading
import pygame as pg
import math
import time
import re


numSounds = 2
drums = []

pg.mixer.init(frequency=88200, size=-16, channels=numSounds, buffer=4096)
# pg.mixer.init()
pg.init()


#good is drones, drills;
for i in range(0, numSounds):
	drum = pg.mixer.Sound("../../sounds/percussion/%d.wav" %i)
	drums.append(drum)

sleep = [1]*numSounds
global lastnorm

def thresholdAll(data):
	norm = abs(math.sqrt( int(data[0])**2 + int(data[1])**2 + int(data[2])**2 )-16000)
	print (norm)

	if(norm > 100000):
		sleepTime = sleep[int(data[3])]

	else:
		if(norm < 1000):
			sleepTime = 3

		elif(norm < 2500):
			sleepTime = 1.4

		elif(norm < 5000):
			sleepTime= 1
		
		elif(norm < 1000):
			sleepTime=0.8
			
		elif(norm < 15000):
			sleepTime=0.4

		else:
			sleepTime=0.2

	return sleepTime


def compare(data):
	global lastnorm
	norm = abs(math.sqrt( int(data[0])**2 + int(data[1])**2 + int(data[2])**2 )-16000)
	compNorm = abs(lastnorm - norm)
	print(compNorm)

	if (compNorm == 0.0):
		sleepTime = sleep[int(data[3])]

	else:
		if(compNorm < 300):
			sleepTime = 3

		elif(compNorm < 500):
			sleepTime = 1.4

		elif(compNorm < 1000):
			sleepTime= 1
		
		elif(compNorm < 5000):
			sleepTime=0.8
			
		elif(compNorm < 10000):
			sleepTime=0.4

		else:
			sleepTime=0.2

	lastnorm = norm
	return sleepTime


def printFile(arg):
	while True:
		file = open("../accelo-live.txt", 'r')
		for line in file:
			data = line.split()
			if(len(data) == 4):
				if (int(data[3]) == 1): sleep[1] = compare(data)
			time.sleep(0.05)
		file.close()

def channel(num, pause):
	while True:
		if(num==1): drums[num].play()
		time.sleep(sleep[num])

if __name__ == "__main__":
	lastnorm = 0
	thread = threading.Thread(target=printFile, args=(0, ))
	thread.start()

	for i in range (0, len(drums)):
		thread = threading.Thread(target=channel, args=(i, i))
		thread.start()
