from inputs import get_gamepad
import math
import threading
import json

class UserController(object):

    #Max value
    MAX_TRIG_VAL = 256.0
    MAX_JOY_VAL = 32768.0


    def __init__(self):
        #Note: 2-98
        self.ailerons = 0
        self.rudder = 0
        self.elevator = 0
        self.throttle = 0

        # 0 = Joystick; 1 = Trigger
        self.aileronsType = 0
        self.rudderType = 0
        self.elevatorType = 0
        self.throttleType = 0

        #Controls
        self.aileronCont = ""
        self.rudderCont = ""
        self.elevatorCont = ""
        self.throttleCont = ""

        self.controlsThread = threading.Thread(target=self.inputListener, args=())
        self.controlsThread.daemon = True
        self.controlsThread.start()
        print("Controls Configuration started Successfully\n")
    
        



    #Input values are normalized between -1 and 1 for joysticks.
    #Input values are normalized between 0 and 1 for triggers
    def inputListener(self):
         while True:
            events = get_gamepad()
            for event in events:
                if event.code == self.aileronCont:
                    if aileronsType == 1:
                        self.ailerons = event.state / UserController.MAX_TRIG_VAL
                    else:
                        self.aileron = event.state / UserController.MAX_JOY_VAL
                elif event.code == self.rudderCont:
                    if rudderType == 1:
                        self.rudder = event.state / UserController.MAX_TRIG_VAL
                    else:
                        self.rudder = event.state / UserController.MAX_JOY_VAL
                elif event.code == self.elevatorCont:
                    if elevatorType == 1:
                        self.elevator = event.state / UserController.MAX_TRIG_VAL
                    else:
                        self.elevator = event.state / UserController.MAX_JOY_VAL
                elif event.code == self.throttleCont:
                    if throttleType == 1:
                        self.throttle = event.state / UserController.MAX_TRIG_VAL
                    else:
                        self.throttle = event.state / UserController.MAX_JOY_VAL
                







