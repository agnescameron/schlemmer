import serial
import re
from time import sleep

ser = serial.Serial('/dev/cu.usbmodem1421', 115200)#, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)

while True:
	line = ser.readline().decode("utf-8")
	line.strip()
	val = line[-6:-2]
	idNum = line[:1]
	print(line)
	# sleep(0.1)