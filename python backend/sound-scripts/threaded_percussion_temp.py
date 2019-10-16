import logging
import threading
import pygame as pg
import math
import time
import re


numSounds = 5
drums = []

pg.mixer.init(frequency=88200, size=-16, channels=numSounds, buffer=4096)
# pg.mixer.init()
pg.init()

#good is drones, drills;
for i in range(0, numSounds):
	drum = pg.mixer.Sound("../../sounds/japanese-percussion/%d.wav" %i)
	drums.append(drum)

sleep = [1]*numSounds
global lastnorm

def threshold(data):
	norm = int(data[0])-2500
	if(norm<0): norm=0
	print(norm)

	if(norm > 1000):
		sleepTime = sleep[int(data[1])]

	else:
		if(norm < 50):
			sleepTime = 3

		elif(norm < 100):
			sleepTime = 1.4

		elif(norm < 150):
			sleepTime= 1
		
		elif(norm < 350):
			sleepTime=0.8
			
		elif(norm < 500):
			sleepTime=0.4

		else:
			sleepTime=0.2

	return sleepTime


def compare(data):
	global lastnorm
	norm = abs(int(data[0])-2700)
	compNorm = abs(lastnorm - norm)
	print(compNorm)

	if (compNorm == 0):
		sleepTime = sleep[int(data[1])]

	else:
		if(compNorm < 10):
			sleepTime = 3

		elif(compNorm < 25):
			sleepTime = 1.4

		elif(compNorm < 50):
			sleepTime= 1
		
		elif(compNorm < 100):
			sleepTime=0.8
			
		elif(compNorm < 150):
			sleepTime=0.4

		else:
			sleepTime=0.2

	lastnorm = norm
	return sleepTime


def printFile(arg):
	while True:
		file = open("../temp-live.txt", 'r')
		for line in file:
			data = line.split()
			if(len(data) == 2):
				sleep[int(data[1])] = threshold(data)  #compare(data)
			time.sleep(0.05)
		file.close()

def channel(num, pause):
	while True:
		drums[num].play()
		time.sleep(sleep[num])

if __name__ == "__main__":
	lastnorm = 0
	thread = threading.Thread(target=printFile, args=(0, ))
	thread.start()

	for i in range (0, len(drums)):
		thread = threading.Thread(target=channel, args=(i, i))
		thread.start()
