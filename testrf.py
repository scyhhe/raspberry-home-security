#!/usr/bin/env python

import serial
import globals
import time
import sys
import thread
from alarmfunctionsr import SwitchRF
from time import sleep
global measure

globals.init()
#SwitchRF(onoff, sensorID, rfPort, wirelessMessage, wCommand):
SwitchRF(1,3,"A", "RELAY", "ON-")
SwitchRF(0,3,"A", "RELAY", "OFF")
