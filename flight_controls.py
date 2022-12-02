from inputs import get_gamepad
import math
import threading
import json

class UserController(object):

    #Max values
    #MAX TRIGGER VALUE = 256.0
    #MAX JOYSTICK VALUE = 32768.0


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
    
        




    def inputListener(self):
         while True:
            events = get_gamepad()
            for event in events:
                if event.code == self.aileronCont:
                    self.ailerons = event.state
                elif event.code == self.rudderCont:
                    self.rudder = event.state 
                elif event.code == self.elevatorCont:
                    self.elevator = event.state 
                elif event.code == self.throttleCont:
                    self.throttle = event.state 

    #Trigger and joystick values normalized between 0 - 100

    def getInput(self, value, type):
        if type == 0:
            return round(pow(3.05,-3) * (value) - pow(-3.64,-14))
        else:
            return round(0.391 * (value) - pow(3.64,-14))

    def getAileronValue(self):
        return getInput(ailerons, aileronsType)
    def getRudderValue(self):
        return getInput(rudder, rudderType)
    def getElevatorValue(self):
        return getInput(elevator, elevatorType)
    def getThrottleValue(self):
        return getInput(throttle, getThrottleValue)


                


""" if __name__ == '__main__':
    while(1):
        inputType = input("Is this a Stick or a Trigger? [s/t]: ")
        if(inputType == "t"):
            print("Selected Trigger")
            self.aileronCont = 1
        else if(inputType == "s")
            print("Selected Stick")
            self.aileronCont = 0

        print("\nMove the aileron stick: ")
        control = get_gamepad()
        event = control[0]
        if (event.code != "SYN_REPORT"):
            stickName = event.code
            print("\nIs this the correct input: ", event.code,)
            userInput = input("Please type [y/n]: ")
            if(userInput == "y"):
                aileronCont = stickName

                break
         """





