# UAV Summer/Fall 2022 Team
# Ground Station Controls Code
# Peter Hoang and Chasen Gaither

# This code runs a basic transmitter connected to a raspberry pi.
# The raspberry pi takes input from a joystick controller (Logitech Extreme 3D Pro)
# and sends that data as integers to the receiver.

"""
CONTROLS NOTES (VERY IMPORTANT)

run this code and fully cycle the throttle and joystick controls, then reset the throttle
to its lowest setting. If this does not 
"""

# Imports: adafruit radio complex
import adafruit_rfm9x
import board
import RPi.GPIO as GPIO
import busio
import digitalio
import flight_controls # Found in AntTest folder, it is responsible for controls configuration
GPIO.setwarnings(False)

# Initialize radio
RADIO_FREQ_MHZ = 915.0
CS = digitalio.DigitalInOut(board.CE1)
RESET = digitalio.DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
rfm9x.tx_power = 23 # maximum power

# Initial values for controls, ranged between 2 and 98
# These run with pulse width modulation, so 2 is min and 98 is max positions

UpDuty = 50         # Servo position for rear elevator
RightDuty = 50      # Servo position for left and right ailerons
RudderDuty = 50     # Servo position for rear rudder

MotorDuty = 2       # runs just like a servo motor, but is a BLDC motor
                    # 2 is lowest speed

# Initialize controller
controller = flight_controls.UserController()

while True:
    
    # Access controller coordinates 
    RightDuty = controller.getAileronValue()
    RudderDuty = controller.getRudderValue()
    UpDuty = controller.getElevatorValue()
    MotorDuty = controller.getThrottleValue()
        
    # bound each motor position between 0 and 100
    if (MotorDuty > 100):
        MotorDuty = 100
    elif (MotorDuty < 0):
        MotorDuty = 0
    MotorDuty = 100-MotorDuty


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
 
    # Combine all values into an integer (easiest for us, but if you can configure it as a string go ahead)
    duty = int(MotorDuty * 1000000 + UpDuty * 10000 + RightDuty * 100 + RudderDuty)
    
    # Convert to bytes and send through the radio
    packet = duty.to_bytes(32, byteorder = "big")
    rfm9x.send(packet)
    
    """
    We recommend inserting code here to receive data from the plane.
    The transceiver on the other side transmits exactly the same way as configured above.
    Use the transceiver on the other side, coupled with I2C or SPI devices, to send data like:
        GPS Coordinates
        Altitude

    Add a receive line like this:
        
        packet = rfm9x.receive()
        packet_int = int.from_bytes(packet, byteorder = "big")
        
    And you should be able to manipulate the received data as you please.
    
    
    
    The transmitter sends data as an integer, formulated this way:
    
    Byte                        7 6             5 4             3 2             1 0
    Associated Motor        Propulsion        Elevator        Ailerons        Rudder
    
    You can add more motor controls (camera gimbal, wheel steering, extra flaps, etc.) 
    by creating a two-digit decimal number and putting it at bytes 8 and 9, but just make sure 
    you change the code to handle everything as a string instead of as an integer. Integers are
    capped at 10 places, but strings can be up to 32 characters.

    Good Luck!
    """
   
    
    
    
