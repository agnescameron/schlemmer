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
drums = [drum0] #, drum1, drum2, drum3, drum4]
sleep = [1, 1, 1, 1, 1]

def printFile(arg):
	while True:
		file = open("../accelo-live1.txt", 'r')
		for line in file:
			data = line.split()
			if(len(data) == 4):
				print(data)
				print(len(data))
				sleep[int(data[3])] = math.sqrt( int(data[0])**2 + int(data[1])**2 + int(data[2])**2 )
			time.sleep(0.05)
		file.close()

def channel(num, pause):
	while True:
		drums[num].play()
		print(num)
		if(sleep[num]<4000000000):
			sleepTime = 0.2

		elif(sleep[num] < 5000000000):
			sleepTime = 0.8

		elif(sleep[num] < 6000000000):
			sleepTime=1.2
		
		elif(sleep[num] < 7000000000):
			sleepTime=1.8

		else:
			sleepTime=2.8

		time.sleep(sleepTime)

if __name__ == "__main__":

	thread = threading.Thread(target=printFile, args=(0, ))
	thread.start()

	for i in range (0, len(drums)):
		thread = threading.Thread(target=channel, args=(i, i))
		thread.start()
