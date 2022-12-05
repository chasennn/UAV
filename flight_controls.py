from inputs import get_gamepad
import math
import threading
import json
import io
import os


class UserController(object):

    # Max values
    # MAX TRIGGER VALUE = 256.0
    # MAX JOYSTICK VALUE = 1024 <- number for logitech extreme 3d pro

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

        # Controls
        self.aileronCont = ""
        self.rudderCont = ""
        self.elevatorCont = ""
        self.throttleCont = ""

        self.openConfig()

        self.controlsThread = threading.Thread(
            target=self.inputListener, args=())
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

    # Trigger and joystick values normalized between 0 - 100

    def getInput(self, value, type):
        if type == 0:  # joystick
            return round(0.0976 * (value) + 3.84 * pow(10,-3))
        else:  # trigger
            return round(0.391 * (value) - 3.64 * pow(10, -14))

    def getAileronValue(self):
        return self.getInput(self.ailerons, self.aileronsType)

    def getRudderValue(self):
        return self.getInput(self.rudder, self.rudderType)

    def getElevatorValue(self):
        return self.getInput(self.elevator, self.elevatorType)

    def getThrottleValue(self):
        return self.getInput(self.throttle, self.throttleType)


def userQuery(controlName, controlType, controlCode, data):
    # Ailerons
    while (1):
        msg = "{" + controlName + "} Is this a Stick or a Trigger? [s/t]: "
        inputType = input(msg)
        if (inputType == "t"):
            inputType = input(
                "You selected Trigger. Is this correct? [y/n]: ")
            if (inputType == "y"):
                print("Selected Trigger")
                data[controlType] = 1
                deadzone = 100
                break
        elif (inputType == "s"):
            inputType = input(
                "You selected Stick. Is this correct? [y/n]: ")
            if (inputType == "y"):
                print("Selected Stick")
                data[controlType] = 0
                deadzone = 800
                break

    print("\nMove the ", controlName, " controls: ")
    while (1):
        control = get_gamepad()
        event = control[0]
        if (event.code != "SYN_REPORT" and event.code != "SYN_CONFIG" and event.code != "SYN_MT_REPORT" and event.code != "SYN_DROPPED" and event.code != "SYN_MAX" and event.code != "SYN_CNT" and event.code != "SYN_REPORT" and event.code != "MSC_SCAN"):
            if (event.state >= deadzone):
                print("\nIs this the correct input: ", event.code,)
                userInput = input("Please type [y/n]: ")
                if (userInput == "y"):
                    data[controlCode] = event.code
                    break
                print("\nMove the ", controlName, " controls: ")


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

    while (1):
        # Ailerons
        userQuery("Ailerons", "aileronType", "aileronCont", data)

        # Rudder
        userQuery("Rudder", "rudderType", "rudderCont", data)

        # elevator
        userQuery("Elevator", "elevatorType", "elevatorCont", data)

        # Throttle
        userQuery("Throttle", "throttleType", "throttleCont", data)

        print("Double check the following controls. Note that for control type, 0 is joystick and 1 is a trigger\n")
        print(data)
        userInput = input("Type [y/n] to confirm the controls: ")
        if userInput == "y":
            break

    # writing to file

    with open('Controls_Configuration.json', 'w') as outfile:
        json.dump(data, outfile)
