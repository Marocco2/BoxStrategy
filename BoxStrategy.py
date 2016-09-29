import ac
import acsys
import sys
import os
import platform

if platform.architecture()[0] == "64bit":
    sysdir = "stdlib64"
else:
    sysdir = "stdlib"

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "box", sysdir))
os.environ['PATH'] = os.environ['PATH'] + ";."

import traceback
import ctypes
import threading

importError = False

#Global variables section
AppInitialised = False

try:
    from BOX import box, win32con
except:
    ac.log('BoxRadio: error loading BOX modules: ' + traceback.format_exc())
    importError = True
try:
    from box.sim_info import info
except:
    ac.log('BoxStrategy: error loading sim_info module: ' + traceback.format_exc())
    importError = True

def acMain(ac_version):

    return "Box Strategy"


def getNotification():
    global Notify, NotificationLabel, StatusLabel
    try:
        Notify = box.notification('232835145:AAHWX3eiGPfBRgOmLvrC293PMHGorC8D7KM')
        ac.setText(NotificationLabel, Notify)
    except:
        ac.log('BoxRadio: No internet connection')
        Status = "No internet connection"
        ac.setText(StatusLabel, Status)


def acUpdate(deltaT):
    global

    try:
        if not AppInitialised:  # First call to app, set variables
            getNotification()
            #if AutoUpdate:
            #    CheckNewUpdate()
            InPit = info.graphics.isInPit
            FuelMax = int(info.static.maxFuel)
            ac.setRange(FuelSelection, 0, FuelMax)
            ReadPreset()
            ac.setValue(Preset1, 1)
            AppInitialised = True

    except Exception as e:
        ac.log("BoxRadio: Error in acUpdate: %s" % e)


