from inputs import get_gamepad
import math
import threading
import json
import io
import os

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

        self.openConfig()

        self.controlsThread = threading.Thread(target=self.inputListener, args=())
        self.controlsThread.daemon = True
        self.controlsThread.start()
        print("Controls Configuration started Successfully\n")
    
        

    def openConfig(self):

        with open('Controls_Configuration.json', 'r') as outfile:
            data = json.load(outfile)

        self.aileronCont = data["aileronCont"]
        self.rudderCont = data["rudderCont"]
        self.elevatorCont = data["elevatorCont"]
        self.throttleCont = data["throttleCont"]

        self.aileronsType = data["aileronType"]
        self.rudderType = data["rudderType"]
        self.elevatorType = data["elevatorType"]
        self.throttleType = data["throttleType"]

        print("Control configuration loaded successfully")


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
        if type == 0: #joystick
            return round(1.53 * pow(10,-3) * (value) - 3.18 * pow(10, -14))
        else:         #trigger
            return round(0.391 * (value) - 3.64 * pow(10,-14))

    def getAileronValue(self):
        return self.getInput(self.ailerons, self.aileronsType)
    def getRudderValue(self):
        return self.getInput(self.rudder, self.rudderType)
    def getElevatorValue(self):
        return self.getInput(self.elevator, self.elevatorType)
    def getThrottleValue(self):
        return self.getInput(self.throttle, self.throttleType)


                


if __name__ == '__main__':



    deadzone = 0
    

    data = {
        "aileronCont": "",
        "aileronType": 0,
        "rudderCont": "",
        "rudderType": 0,
        "elevatorCont": "",
        "elevatorType": 0,
        "throttleCont": "",
        "throttleType": 0
    }


    while(1):
        #Ailerons
        while(1):
            inputType = input("{Ailerons} Is this a Stick or a Trigger? [s/t]: ")
            if(inputType == "t"):
                inputType = input("You selected Trigger. Is this correct? [y/n]: ")
                if (inputType == "y"):
                    print("Selected Trigger")
                    data["aileronType"] = 1
                    deadzone = 100
                    break
            elif (inputType == "s"):
                inputType = input("You selected Stick. Is this correct? [y/n]: ")
                if (inputType == "y"):
                    print("Selected Stick")
                    data["aileronType"] = 0
                    deadzone = 16384
                    break

        print("\nMove the aileron controls: ") 
        while(1):
            control = get_gamepad()
            event = control[0]
            if (event.code != "SYN_REPORT" and event.code != "SYN_CONFIG" and event.code != "SYN_MT_REPORT" and event.code != "SYN_DROPPED" and event.code != "SYN_MAX" and event.code != "SYN_CNT"):
                if (event.state >= deadzone):
                    print("\nIs this the correct input: ", event.code,)
                    userInput = input("Please type [y/n]: ")
                    if(userInput == "y"):
                        data["aileronCont"] = event.code
                        break
                    print("\nMove the aileron controls: ")

        #Rudder
        while(1):
            inputType = input("{Rudder} Is this a Stick or a Trigger? [s/t]: ")
            if(inputType == "t"):
                inputType = input("You selected Trigger. Is this correct? [y/n]: ")
                if (inputType == "y"):
                    print("Selected Trigger")
                    data["rudderType"] = 1
                    deadzone = 100
                    break
            elif (inputType == "s"):
                inputType = input("You selected Stick. Is this correct? [y/n]: ")
                if (inputType == "y"):
                    print("Selected Stick")
                    data["rudderType"] = 0
                    deadzone = 16384
                    break

        print("\nMove the Rudder controls: ") 
        while(1):
            control = get_gamepad()
            event = control[0]
            if (event.code != "SYN_REPORT" and event.code != "SYN_CONFIG" and event.code != "SYN_MT_REPORT" and event.code != "SYN_DROPPED" and event.code != "SYN_MAX" and event.code != "SYN_CNT"):
                if (event.state >= deadzone):
                    print("\nIs this the correct input: ", event.code,)
                    userInput = input("Please type [y/n]: ")
                    if(userInput == "y"):
                        data["rudderCont"] = event.code
                        break
                    print("\nMove the Rudder controls: ")

        #elevator
        while(1):
            inputType = input("{Elevator} Is this a Stick or a Trigger? [s/t]: ")
            if(inputType == "t"):
                inputType = input("You selected Trigger. Is this correct? [y/n]: ")
                if (inputType == "y"):
                    print("Selected Trigger")
                    data["elevatorType"] = 1
                    deadzone = 100
                    break
            elif (inputType == "s"):
                inputType = input("You selected Stick. Is this correct? [y/n]: ")
                if (inputType == "y"):
                    print("Selected Stick")
                    data["elevatorType"] = 0
                    deadzone = 16384
                    break

        print("\nMove the elevator controls: ") 
        while(1):
            control = get_gamepad()
            event = control[0]
            if (event.code != "SYN_REPORT" and event.code != "SYN_CONFIG" and event.code != "SYN_MT_REPORT" and event.code != "SYN_DROPPED" and event.code != "SYN_MAX" and event.code != "SYN_CNT"):
                if (event.state >= deadzone):
                    print("\nIs this the correct input: ", event.code,)
                    userInput = input("Please type [y/n]: ")
                    if(userInput == "y"):
                        data["elevatorCont"] = event.code
                        break
                    print("\nMove the elevator controls: ")

        #Throttle
        while(1):
            inputType = input("{Throttle} Is this a Stick or a Trigger? [s/t]: ")
            if(inputType == "t"):
                inputType = input("You selected Trigger. Is this correct? [y/n]: ")
                if (inputType == "y"):
                    print("Selected Trigger")
                    data["throttleType"] = 1
                    deadzone = 100
                    break
            elif (inputType == "s"):
                inputType = input("You selected Stick. Is this correct? [y/n]: ")
                if (inputType == "y"):
                    print("Selected Stick")
                    data["throttleType"]= 0
                    deadzone = 16384
                    break

        print("\nMove the throttle controls: ") 
        while(1):
            control = get_gamepad()
            event = control[0]
            if (event.code != "SYN_REPORT" and event.code != "SYN_CONFIG" and event.code != "SYN_MT_REPORT" and event.code != "SYN_DROPPED" and event.code != "SYN_MAX" and event.code != "SYN_CNT"):
                if (event.state >= deadzone):
                    print("\nIs this the correct input: ", event.code,)
                    userInput = input("Please type [y/n]: ")
                    if(userInput == "y"):
                        data["throttleCont"] = event.code
                        break
                    print("\nMove the throttle controls: ")



        print("Double check the following controls. Note that for control type, 0 is joystick and 1 is a trigger\n")
        print(data)
        userInput = input("Type [y/n] to confirm the controls: ")
        if userInput == "y":
            break
    

    #writing to file

    with open('Controls_Configuration.json', 'w') as outfile:
        json.dump(data, outfile)






