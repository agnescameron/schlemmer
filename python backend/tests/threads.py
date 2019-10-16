import logging
import threading
import pygame as pg
import math
import time
import re

pg.mixer.init()
pg.init()
pg.mixer.set_num_channels(50)


drum1 = pg.mixer.Sound("../../sounds/japanese-percussion/biz.wav")
drum4 = pg.mixer.Sound("../../sounds/japanese-percussion/taiko.wav")
drum2 = pg.mixer.Sound("../../sounds/japanese-percussion/hyoshigi.wav")
drum3 = pg.mixer.Sound("../../sounds/japanese-percussion/kagura.wav")
drum0 = pg.mixer.Sound("../../sounds/japanese-percussion/tsuzumi.wav")
drums = [drum0]#, drum0, drum0, drum0, drum0] #[drum0, drum1, drum2, drum3, drum4]
sleep = [1, 1, 1, 1, 1]
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
		file = open("../accelo-live1.txt", 'r')
		for line in file:
			data = line.split()
			if(len(data) == 4):
				sleep[int(data[3])] = compare(data)
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
