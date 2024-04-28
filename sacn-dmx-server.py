#!/usr/bin/python
# -*- coding: utf-8 -*-
import serial
import time
import sacn
#import datetime

dmxconnection = False
while not dmxconnection:
	try:
		dmx = serial.Serial('/dev/ttyAMA1', baudrate=250000, bytesize=8, stopbits=2)
		dmxconnection = True
	except:
		print("Serial not available.")
		exit()

data = []
for i in range(513):
	data.append(0x00)

def sendDMXdirect(dataIN):
	dmx.break_condition = True
	time.sleep(120/1000000.0)
	dmx.break_condition = False
	time.sleep(12/1000000.0)
	dmx.write(bytearray(dataIN))

receiver = sacn.sACNreceiver()
receiver.start()

@receiver.listen_on('universe', universe=1)
def callback(packet):
#	print("ok")
	for i in range(512):
		data[i+1] = packet.dmxData[i]

receiver.join_multicast(1)

while True:
	sendDMXdirect(data)

