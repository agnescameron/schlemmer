import serial
import re
from time import sleep
import math

ser = serial.Serial('/dev/cu.usbmodem527', 115200)#, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)

while True:
	ser.flushInput()
	line = ser.readline().decode("utf-8")
	data = line.split();
	print(data)
	# sleep(0.1)