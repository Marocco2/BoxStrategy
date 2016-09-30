# Made with BOX
#
#
#
#
#
import ac
import acsys
import sys
import os
import platform
import datetime
import codecs
import configparser
import shutil


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

# Check My Documents location
from ctypes import wintypes

CSIDL_PERSONAL = 5  # My Documents
SHGFP_TYPE_CURRENT = 0  # Get default value
buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
ac.log('BoxStrategy: Log path: ' + buf.value)



#Global variables section
AppInitialised = False
debug = 1

try:
    from BOX import box, win32con
except:
    ac.log('BoxStrategy: error loading BOX modules: ' + traceback.format_exc())
    importError = True
try:
    from box.sim_info import info
except:
    ac.log('BoxStrategy: error loading sim_info module: ' + traceback.format_exc())
    importError = True



def acMain(ac_version):
    global debuglabel

    appWindow = ac.newApp("Box Strategy")
    ac.setSize(appWindow, 180, 220)
    ac.setTitle(appWindow, "Box Strategy")
    ac.setBackgroundOpacity(appWindow, 0.5)
    ac.drawBorder(appWindow, 0)
    #
    # DEBUG INFO
    #
    debuglabel = ac.addLabel(appWindow, "")
    ac.setPosition(debuglabel, 10, 30)
    ac.setSize(debuglabel, 160, 170)
    #
    #
    # STATUS LABELS
    #
    #StatusLabel = ac.addLabel(appWindow, Status)
    #ac.setPosition(StatusLabel, 10, 275)
    #ac.setFontColor(StatusLabel, 1, 1, 1, 1)
    #ac.setFontSize(StatusLabel, 15)
    #
    NotificationLabel = ac.addLabel(appWindow, Notify)
    ac.setPosition(NotificationLabel, 10, 200)
    ac.setFontColor(NotificationLabel, 1, 1, 1, 1)
    ac.setFontSize(NotificationLabel, 12)
    #
    return "Box Strategy"


def getNotification():
    global Notify, NotificationLabel, StatusLabel
    try:
        Notify = box.notification('232835145:AAHWX3eiGPfBRgOmLvrC293PMHGorC8D7KM')
        ac.setText(NotificationLabel, Notify)
    except:
        ac.log('BoxStrategy: No internet connection')
        Status = "No internet connection"
        ac.setText(StatusLabel, Status)


def acUpdate(deltaT):
    global AppInitialised, status, session, numberOfLaps, InPit, FuelMax, FuelRate, TireRate, car_model, track
    global TireCompund, sector

    status = info.graphics.status
    session = info.graphics.session
    numberOfLaps = info.graphics.numberOfLaps
    InPit = info.graphics.isInPit
    TireCompund = info.graphics.tyreCompund
    sector = info.graphics.currentSectorIndex

    if session != 2:
        # Initialize record code
        laptime = 0
        counter = 0
        # Start record
        

    if session == 2:


    # DEBUG INFOS
    if debug:
        ac.setText(debuglabel, "Session: " + repr(session) +
                    "\nNumber of laps: " + repr(numberOfLaps) +
                    "\nCar: " + str(car_model) +
                    "\nTrack: " + str(track) +
                    "\nSector: " + str(sector) +
                    #"\nCompleted Laps: " + repr(completedLaps) +
                    #"\nOvertakes: " + repr(count_overtake) +
                    #"\nSession Time: " + repr(sessionTime) +
                    #"\nPosition: " + repr(ac.getCarRealTimeLeaderboardPosition(0)) +
                    "\nCompound: " + str(TireCompund) +
                    "\nMax Fuel: " + str(FuelMax) +
                    "\nFuel rate aid: " + str(FuelRate) +
                    "\nTire rate aid: " + str(TireRate) +
                    "\nStatus: " + str(status) +
                    "\nIn Pit: " + str(InPit))


    try:
        if not AppInitialised:  # First call to app, set variables
            getNotification()
            #if AutoUpdate:
            #    CheckNewUpdate()
            FuelMax = int(info.static.maxFuel)
            #ac.setRange(FuelSelection, 0, FuelMax)
            #ReadPreset()
            #ac.setValue(Preset1, 1)
            FuelRate = info.static.aidFuelRate
            TireRate = info.static.aidTireRate
            car_model = info.static.carModel
            track = info.static.ttack
            AppInitialised = True


    except Exception as e:
        ac.log("BoxStrategy: Error in acUpdate: %s" % e)


def WritePreset():
    global track, car_model, TireCompound

    PresetConfig = configparser.ConfigParser()
    PresetConfig.read('apps\python\BoxStrategy\BoxStrategy.ini')
    if Tires != 'NoChange' or Gas != 0 or FixBody != 'no' or FixEngine != 'no' or FixSuspen != 'no' or Car != ac.getCarName(
            0):
        PresetConfig.set(str(track)  + '_' + str(car_model) + '_' + str(TireCompund) , 'car', ac.getCarName(0))
        PresetConfig.set(str(track)  + '_' + str(car_model) + '_' + str(TireCompund) , 'tyre', Tires)
        PresetConfig.set(str(track)  + '_' + str(car_model) + '_' + str(TireCompund) , 'fuel', str(Gas))
        PresetConfig.set(str(track)  + '_' + str(car_model) + '_' + str(TireCompund) , 'body', FixBody)
        PresetConfig.set(str(track)  + '_' + str(car_model) + '_' + str(TireCompund) , 'engine', FixEngine)
        PresetConfig.set(str(track)  + '_' + str(car_model) + '_' + str(TireCompund) , 'suspen', FixSuspen)
        with open('apps\python\BoxStrategy\BoxStrategy.ini', 'w') as configfile:
            configfile.write(
                ';Set "FUEL / add" to "1" to ADD the fuel to the amount already in the tank or set to "0" to fill the tank up to the amount selected on the app.' + '\n')
            configfile.write(
                ';UI Size example: Set "UI / sizemultiplier" to "1.2" in order to increase UI size in 20% (min: 1.0, max: 3.0)' + '\n' + '\n')
            PresetConfig.write(configfile)

def ReadPreset():
    global track, car_model, TireCompund

    PresetConfig = configparser.ConfigParser()
    PresetConfig.read('apps\python\BoxStrategy\BoxStrategy.ini')

    if not str(track)  + '_' + ac.getCarName(0) in PresetConfig:
        WriteSection()

    Car = PresetConfig[str(track)  + '_' + ac.getCarName(0)]['car']

    if Car == ac.getCarName(0):
        ac.setValue(FuelSelection, int(PresetConfig[str(track)  + '_' + str(car_model) + '_' + str(TireCompund) ]['fuel']))
        if PresetConfig[str(track)  + '_' + str(car_model) + '_' + str(TireCompund) ]['body'] == 'no':
            FixBody = 'yes'
        else:
            FixBody = 'no'
        if PresetConfig[str(track)  + '_' + str(car_model) + '_' + str(TireCompund) ]['engine'] == 'no':
            FixEngine = 'yes'
        else:
            FixEngine = 'no'
        if PresetConfig[str(track)  + '_' + str(car_model) + '_' + str(TireCompund) ]['suspen'] == 'no':
            FixSuspen = 'yes'
        else:
            FixSuspen = 'no'
        if PresetConfig[str(track)  + '_' + str(car_model) + '_' + str(TireCompund) ]['tyre'] == 'NoChange':
            NoChangeEvent('name', 0)
        elif PresetConfig[str(track)  + '_' + str(car_model) + '_' + str(TireCompund) ]['tyre'] == 'Option1':
            Option1Event('name', 0)
        elif PresetConfig[str(track)  + '_' + str(car_model) + '_' + str(TireCompund) ]['tyre'] == 'Option2':
            Option2Event('name', 0)
        elif PresetConfig[str(track)  + '_' + str(car_model) + '_' + str(TireCompund) ]['tyre'] == 'Option3':
            Option3Event('name', 0)
        elif PresetConfig[str(track)  + '_' + str(car_model) + '_' + str(TireCompund) ]['tyre'] == 'Option4':
            Option4Event('name', 0)
        elif PresetConfig[str(track)  + '_' + str(car_model) + '_' + str(TireCompund) ]['tyre'] == 'Option5':
            Option5Event('name', 0)
    else:
        ac.setValue(FuelSelection, 0)
        NoChangeEvent('name', 0)
        FixBody = 'yes'
        FixEngine = 'yes'
        FixSuspen = 'yes'

    BodyEvent('name', 0)
    EngineEvent('name', 0)
    SuspensionEvent('name', 0)
    FuelEvent(0)
