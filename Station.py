from ast import IsNot
from email import message
from time import time
import datetime

import digitalio
import board
import busio
import adafruit_rfm9x

RADIO_FREQ_MHZ = 925.0
CS = digitalio.DigitalInOut(board.CE1)
RESET = digitalio.DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialze RFM radio with a more conservative baudrate
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

rfm9x.tx_power = 23




prev_packet = None
packetLossCount = 0
packetCount = 0
x = datetime.datetime.now()
fileName = "test_" + str(x) + ".txt"
file1 = open(fileName, 'w')

lastTime = int(time() * 1000)
key = bytes("TESTUW", "utf-8")

while True:
	packet = None
	rfm9x.send(key)
	
	packet = rfm9x.receive()
	if packet is None:
		print("Waiting...")
		if packetCount != 0:
			packetLossCount = packetLossCount + 1
		
	else:
		x2 = datetime.datetime.now
		packetCount = packetCount + 1
		currentTime = int(time()*1000)
		pingTime = currentTime - lastTime
		lastTime = currentTime
		rssi = rfm9x.last_rssi
		snr = rfm9x.last_snr
		logMessage = "Ping: " + str(pingTime) + " Packet Loss: " + str(packetLossCount) + " RSSI: " + str(rssi) + " SNR: " + str(snr) + " " + str(x2) + "\n "
		print(logMessage)
		file1.write(logMessage)
		
 
