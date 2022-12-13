from inputs import get_gamepad
import math
import threading
import json
import io
import os

while(1):
    controller = get_gamepad()
    events = get_gamepad()
    for event in events:
        #if (event.code != "SYN_REPORT" and event.code != "SYN_CONFIG" and event.code != "SYN_MT_REPORT" and event.code != "SYN_DROPPED" and event.code != "SYN_MAX" and event.code != "SYN_CNT" and event.code != "SYN_REPORT" and event.code != "MSC_SCAN"):
            #if (event.code == "ABS_X"):
        print(event.code, " ", event.state, "\n")