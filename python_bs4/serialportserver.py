import serial
import time

ser = serial.Serial('/dev/pts/17')

val = ''
while True:
	
	val = ser.read(1)
	#print ord(val)
	
	if ord(val) == 20:
		ser.write(bytearray([0x22]))

ser.close()
