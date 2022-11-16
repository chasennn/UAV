import digitalio
import board
import busio
import adafruit_rfm9x
import RPi.GPIO as GPIO
from time import time
from gpiozero import Servo

from gpiozero.pins.pigpio import PiGPIOFactory

RADIO_FREQ_MHZ = 925.0
CS = digitalio.DigitalInOut(board.CE1)
RESET = digitalio.DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialze RFM radio with a more conservative baudrate
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

rfm9x.tx_power = 23

factory = PiGPIOFactory()

RightAil = Servo(12, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = factory)

LeftAil = Servo(16, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = factory)

Elevator = Servo(20, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = factory)

Rudder = Servo(21, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = factory)

Motor = Servo(26, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = factory)

while True: 
    
    packet = None
    # draw a box to clear the image

    # check for packet rx
    packet = rfm9x.receive()
    if packet is None:
        packet_int = 0
    else:
        packet_int = int.from_bytes(packet, byteorder = "big")
        
        MotorPower = packet_int/1000000 - 50        
        UpDown = (packet_int % 1000000) / 10000 - 50
        RightLeft = (packet_int / 100) % 100 - 50
        RudderPos = packet_int % 100 - 50

        Elevator.value = 0.5 + 0.01 * UpDown
        
        Rudder.value = 0.5 + 0.01 * RudderPos
        
        LeftAil.value = 0.5 + 0.01 * RightLeft
        
        RightAil.value = 0.5 + 0.01 * RightLeft
        
        Motor.value = 0.01 * MotorPower
        
        rssi = rfm9x.last_rssi
        
        print(rssi)
        
        
        
     
