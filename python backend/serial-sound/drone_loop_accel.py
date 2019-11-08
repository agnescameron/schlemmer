import threading
import pygame as pg
import math
import time
import re
import serial

numSounds = 6
ser = serial.Serial('/dev/cu.usbmodem528', 115200)


pg.mixer.init(frequency=44100, size=-16, channels=numSounds, buffer=4096)
pg.init()

drones = []
buffer = [0]*20


#good is drones, drills;
for i in range(0, numSounds):
	drone = pg.mixer.Sound("../../sounds/rehearsal-test/0.wav")
	drones.append(drone)

vol = [0, 0, 0, 0, 0, 0]
global lastnorm

def thresholdAll(data):
	norm = abs(math.sqrt( int(data[0])**2 + int(data[1])**2 + int(data[2])**2 )-16000)
	print (norm)

	if(norm > 100000):
		volume = vol[int(data[0])]
		# volume = vol[0]

	volume = norm/2000

	return volume


def compare(data):
	global lastnorm
	norm = abs(math.sqrt( int(data[0])**2 + int(data[1])**2 + int(data[2])**2 ))
	compNorm = abs(lastnorm - norm)
	print(compNorm)

	if (compNorm == 0.0):
		volume = vol[int(data[0])]
		# volume = vol[0]

	else:
		volume = compNorm/3000

	lastnorm = norm
	return volume

def moving_weighted_average(data, bufSize):
	# print(movingAv)
	if data[1:] == ['1', '1', '1']:
		norm=0
	elif data[1:] == ['0', '0', '0']:
		norm=0
	else:
		norm = abs(math.sqrt( int(data[1])**2 + int(data[2])**2 + int(data[3])**2 )-16000)
	buffer.append(norm)
	avBuffer = buffer[-bufSize:]
	movingAv = sum(avBuffer)/bufSize
	print(movingAv)
	#12000 is good!
	return movingAv/12000

def moving_average(data, bufSize):
	if data[1:] == ['1', '1', '1']:
		norm=0
	elif data[1:] == ['0', '0', '0']:
		norm=0
	else:
		norm = abs(math.sqrt( int(data[1])**2 + int(data[2])**2 + int(data[3])**2 )-16000)
	buffer.append(norm)
	avBuffer = buffer[-bufSize:]
	movingAv = sum(avBuffer)/bufSize
	print(movingAv)
	#12000 is good!
	return movingAv/12000

# def weighted_average(data, bufSize):
# 	# print(movingAv)
# 	norm = abs(math.sqrt( int(data[0])**2 + int(data[1])**2 + int(data[2])**2 )-16000)
# 	buffer.append(norm)
# 	nearBuffer = buffer[-bufSize/2:]
# 	farBuffer = buffer[-bufSize:-bufSize/2]
# 	movingAv = (nearBuffer*2 + farBuffer*0.5)/bufSize
# 	# if(data[3] == 1):
# 	print(movingAv)
# 	return movingAv/6000


def getSerial():
	while True:
		ser.flushInput()
		line = ser.readline().decode("utf-8")
		data = line.split();
		vals = data[1:]
		idNum = data[:1]
		if vals == ['1', '1', '1']:
			print(idNum, 'borked')
		if vals == ['0', '0', '0']:
			print(idNum, 'borked')
		if(len(data) == 4):
			if(int(data[0]) == 0):				
				vol[int(data[0])] = moving_average(data, 20)
				# vol[int(data[0])] = moving_average(data, 20)
				print(data)			
			if(int(data[0]) == 1):				
				vol[int(data[0])] = moving_average(data, 20)
				print(data)	
			if(int(data[0]) == 2):				
				vol[int(data[0])] = moving_average(data, 20)
				print(data)
			# if(int(data[0]) == 3):				
			# 	vol[int(data[0])] = moving_average(data, 20)
			# 	print(data)			
			# if(int(data[0]) == 4):				
			# 	vol[int(data[0])] = moving_average(data, 20)
			# 	print(data)	
			# if(int(data[0]) == 5):				
			# 	vol[int(data[0])] = moving_average(data, 20)
			# 	print(data)
			
			# vol[0] = 0
			# vol[1] = 0
			# vol[2] = 0
			vol[3] = 0
			vol[4] = 0
			vol[5] = 0

def channel(num):
	while True:
		drones[num].set_volume(vol[num])
		drones[num].play(loops=-1)

if __name__ == "__main__":
	lastnorm = 0
	thread = threading.Thread(target=getSerial)
	thread.start()

	for i in range (0, numSounds):
		thread = threading.Thread(target=channel, args=(i, ))
		thread.start()
