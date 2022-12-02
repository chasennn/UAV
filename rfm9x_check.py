import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the RFM9x radio module.
import adafruit_rfm9x

# Configure RFM9x LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

while True:
	
	try:
		rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
		print('RFM9x: Detected')
	except RuntimeError as error:
		# Thrown on version mismatch
		print('RFM9x Error: ', error)
        
	time.sleep(1)
