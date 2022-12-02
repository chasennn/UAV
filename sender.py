import time

import adafruit_rfm9x
import board
import RPi.GPIO as GPIO
import busio
import digitalio
import sys, tty, termios, time
import curses

screen = curses.initscr()
screen.nodelay(True)
curses.noecho()
curses.cbreak()
screen.keypad(True)

GPIO.setwarnings(False)

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try: 
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


RADIO_FREQ_MHZ = 925.0
CS = digitalio.DigitalInOut(board.CE1)
RESET = digitalio.DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialze RFM radio with a more conservative baudrate
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

rfm9x.tx_power = 23

UpDuty = 50

RightDuty = 50

RudderDuty = 50

MotorDuty = 50

i = 0

while i < 100:
    
   
    char = screen.getch()
    
    if char == ord('w'):
        UpDuty = UpDuty - 6
    elif char == ord('s'):
        UpDuty = UpDuty + 6
    elif char == ord('a'):
        RightDuty = RightDuty - 6
    elif char == ord('d'):
        RightDuty = RightDuty + 6
    elif char == ord('c'):
        RudderDuty = RudderDuty + 6
    elif char == ord('z'):
        RudderDuty = RudderDuty -6
    elif char == ord('k'):
        MotorDuty = MotorDuty + 6
    elif char == ord('m'):
        MotorDuty = MotorDuty - 6
        
    if (MotorDuty > 98):
        MotorDuty = 98
    elif (MotorDuty < 2):
        MotorDuty = 2
    
    if (UpDuty > 98):
        UpDuty = 98
    elif (UpDuty < 2):
        UpDuty = 2
    
    if (RightDuty > 98):
        RightDuty = 98
    elif (RightDuty < 2):
        RightDuty = 2
        
    if (RudderDuty > 98):
        RudderDuty = 98
    elif (RudderDuty < 2):
        RudderDuty = 2
        
    if (UpDuty > 50):
        UpDuty = UpDuty - 2
    if (UpDuty < 50):
        UpDuty = UpDuty + 2
        
    if (RightDuty > 50):
        RightDuty = RightDuty - 2
    if (RightDuty < 50):
        RightDuty = RightDuty + 2
        
    if (RudderDuty > 50):
        RudderDuty = RudderDuty - 2
    if (RudderDuty < 50):
        RudderDuty = RudderDuty + 2
 
    
    duty = int(MotorDuty * 1000000 + UpDuty * 10000 + RightDuty * 100 + RudderDuty)
    
    packet = duty.to_bytes(32, byteorder = "big")
    rfm9x.send(packet)
   
    
    
    
