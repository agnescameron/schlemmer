import serial
import threading
import pygame as pg
import math
import time
import re

ser = serial.Serial('/dev/cu.usbmodem455', 115200)

numSounds = 1

pg.mixer.init(frequency=44100, size=-16, channels=numSounds, buffer=4096)
pg.init()

drones = []
dataBuffer = [0]*20


#good is drones, drills;
for i in range(0, numSounds):
	drone = pg.mixer.Sound("../../sounds/rehearsal-test/%d.wav" %i)
	drones.append(drone)

vol = [0.0, 0.0, 0.0, 0.1, 0.1]
global lastnorm

def threshold(data):
	norm = abs(int(data[1])-600)
	if(norm<0): norm=0

	if(norm > 10000):
		volume = vol[int(data[0])]

	volume = norm/100

	return volume


def compare(data):
	global lastnorm
	norm = int(data[1])
	compNorm = abs(lastnorm - norm)
	# print(compNorm)

	if (compNorm == 0.0):
		volume = vol[int(data[0])]

	else:
		volume = compNorm/250

	lastnorm = norm
	return volume

def moving_comparative_average(data, bufSize):
	global lastnorm
	norm = int(data[1])
	compNorm = abs(lastnorm - norm)/250
	dataBuffer.append(compNorm)
	avBuffer = dataBuffer[-bufSize:]
	movingAv = sum(avBuffer)/bufSize
	# print(movingAv)
	return movingAv/250


def moving_threshold_average(data, bufSize):
	norm = abs(int(data[1])-600)
	dataBuffer.append(norm)
	avBuffer = dataBuffer[-bufSize:]
	movingAv = sum(avBuffer)/bufSize
	return movingAv/250

def getSerial():
	while True:
		line = ser.readline().decode("utf-8")
		data = line.split();
		vals = data[1:]
		idNum = data[:1]
		#print(data)
		if(len(data) == 2):
			#vol[int(data[0])] = moving_threshold_average(data, 25)
			vol[0] = moving_threshold_average(data, 25)

def channel(num):
	while True:
		drones[num].set_volume(vol[num])
		# print(vol[num])
		drones[num].play(loops=-1)

if __name__ == "__main__":
	lastnorm = 0
	thread = threading.Thread(target=getSerial)
	thread.start()

	for i in range (0, len(drones)):
		thread = threading.Thread(target=channel, args=(i, ))
		thread.start()
