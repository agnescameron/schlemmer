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
drums = [drum4]#, drum0, drum0, drum0, drum0] #[drum0, drum1, drum2, drum3, drum4]
event = [1, 1, 1, 1, 1]
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
		file = open("../accelo-live1.txt", 'r')
		for line in file:
			data = line.split()
			if(len(data) == 4):
				event[int(data[3])] = compare(data)
			time.sleep(0.1)
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
