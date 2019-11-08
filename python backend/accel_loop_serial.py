import threading
import pygame as pg
import numpy.linalg
import math
import time
import re
import serial

ser = serial.Serial('/dev/cu.usbmodem528', 115200)

pg.mixer.init(frequency=44100, size=-16, channels=1, buffer=4096)
pg.init()

buffer = [0]*20

#change stuff here!
soundfile = "../sounds/rehearsal-test/0.wav"
sensors = [0, 1, 2, 3, 4, 5]  #put the number of sensors used
norms = [0]*len(sensors)

drone = pg.mixer.Sound("../sounds/rehearsal-test/0.wav")
vol=[0]
global lastnorm

def moving_weighted_average(data, bufSize):
	norms[int(data[0])] = abs(math.sqrt( int(data[1])**2 + int(data[2])**2 + int(data[3])**2 )-16000)
	avNorm = sum(norms)/len(norms)
	buffer.append(avNorm)
	avBuffer = buffer[-bufSize:]
	movingAv = sum(avBuffer)/bufSize
	print(movingAv, norms)
	return movingAv/12000

def moving_average(data, bufSize):
	norms[int(data[0])] = abs(math.sqrt( int(data[1])**2 + int(data[2])**2 + int(data[3])**2 )-16000)
	avNorm = sum(norms)/len(norms)
	buffer.append(avNorm)
	avBuffer = buffer[-bufSize:]
	movingAv = sum(avBuffer)/bufSize
	print(movingAv, norms)
	return movingAv/12000

def getSerial():
	while True:
		ser.flushInput()
		borked = False
		line = ser.readline().decode("utf-8")
		data = line.split();
		vals = data[1:]
		idNum = data[:1]
		if (vals == ['1', '1', '1']) or (vals == ['0', '0', '0']):
			borked = True
			print(idNum, 'borked')
		if (len(data) == 4):
			if (int(data[0]) in sensors) and not borked:		
				vol[0] = moving_average(data, 20)
				# vol = 1
				# vol = moving_weighted_average(data, 20)
				print(data)
				# print(vol)

def channel():
	while True:
		drone.set_volume(vol[0])
		drone.play(loops=-1)

if __name__ == "__main__":
	print("listening for sensors", sensors, "playing sound file", soundfile)
	lastnorm = 0
	thread1 = threading.Thread(target=getSerial)
	thread1.start()

	thread2 = threading.Thread(target=channel, args=( ))
	thread2.start()
