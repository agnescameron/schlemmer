import logging
import threading
import pygame as pg
import math
import time
import re

pg.mixer.init()
pg.init()
pg.mixer.set_num_channels(50)
lastnorm = 0


drum1 = pg.mixer.Sound("../../sounds/japanese-percussion/biz.wav")
drum4 = pg.mixer.Sound("../../sounds/japanese-percussion/taiko.wav")
drum2 = pg.mixer.Sound("../../sounds/japanese-percussion/hyoshigi.wav")
drum3 = pg.mixer.Sound("../../sounds/japanese-percussion/kagura.wav")
drum0 = pg.mixer.Sound("../../sounds/japanese-percussion/tsuzumi.wav")
drums = [drum0]#, drum0, drum0, drum0, drum0] #[drum0, drum1, drum2, drum3, drum4]
sleep = [1, 1, 1, 1, 1]

def thresholdAll(data):
	norm = abs(math.sqrt( int(data[0])**2 + int(data[1])**2 + int(data[2])**2 )-15000)
	print (norm)

	if(norm > 100000):
		sleepTime = sleep[int(data[3])]

	else:
		if(norm < 1000):
			sleepTime = 2

		elif(norm < 2500):
			sleepTime = 1.2

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
	norm = abs(math.sqrt( int(data[0])**2 + int(data[1])**2 + int(data[2])**2 )-9.8)
	print (norm)

	if(norm > 100000):
		sleepTime = sleep[int(data[3])]

	else:
		if(norm < 1000):
			sleepTime = 2

		elif(norm < 2500):
			sleepTime = 1.2

		elif(norm < 5000):
			sleepTime= 1
		
		elif(norm < 1000):
			sleepTime=0.8
			
		elif(norm < 15000):
			sleepTime=0.4

		else:
			sleepTime=0.2

	return sleepTime


def movingAv(data):
	norm = abs(math.sqrt( int(data[0])**2 + int(data[1])**2 + int(data[2])**2 )-6073989301)
	print (norm)

	if(norm > 100000):
		sleepTime = sleep[int(data[3])]

	else:
		if(norm < 1000):
			sleepTime = 2

		elif(norm < 5000):
			sleepTime = 1.2

		elif(norm < 12000):
			sleepTime= 1
		
		elif(norm < 25000):
			sleepTime=0.8
			
		elif(norm < 50000):
			sleepTime=0.4

		else:
			sleepTime=0.2

	return sleepTime


def printFile(arg):
	while True:
		file = open("../accelo-live1.txt", 'r')
		for line in file:
			data = line.split()
			if(len(data) == 4):
				sleep[int(data[3])] = thresholdAll(data)
			time.sleep(0.05)
		file.close()

def channel(num, pause):
	while True:
		drums[num].play()
		time.sleep(sleep[num])

if __name__ == "__main__":

	thread = threading.Thread(target=printFile, args=(0, ))
	thread.start()

	for i in range (0, len(drums)):
		thread = threading.Thread(target=channel, args=(i, i))
		thread.start()
