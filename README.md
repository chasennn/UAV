# UAV
This repository contains code for our UAV Capstone Project at the University of Washington Bothell. It uses the LoRa 915 MHz modules to communicate between the two Raspberry Pis.

Step 1 - SSH into two Raspberry Pis and clone this repository into each one. Make sure your Raspberry Pis are wired correctly with the LoRa radios using rfm9x_check.py.

Step 2 - Run 'Station.py' on one pi and 'repeater.py' on the other.

UPDATE:

New code in files named "sender.py" and "receive.py" - contain code for 4 servo motors and one brushless DC motor on the receiver side. Control these motors from the sender side using AWSD, Z, C, and K, M

AWSD - ailerons and elevator
ZC - rudder controls (emulates pedals)
KM - throttle
