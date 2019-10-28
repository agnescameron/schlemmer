import serial
import re
from time import sleep

ser = serial.Serial('/dev/cu.usbmodem1421', 115200)#, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)

while True:
	line = ser.readline().decode("utf-8")
	data = line.split();
	vals = data[1:]
	idNum = data[:1]
	print(vals)
	print(idNum)
	# sleep(0.1)