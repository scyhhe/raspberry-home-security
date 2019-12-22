#!/usr/bin/env python
"""
Check to see if an process is running. If not, restart.
Run this in a cron job
"""
import os
import globals

globals.init()

process_name= "alarm.py" # change this to the name of your process
tmp2 = os.popen("ps -Af").read()

if process_name not in tmp2[:] and globals.auto_alarm:
    newprocess="nohup python %s/%s &" % (globals.install_directory, process_name)
    os.system(newprocess)

process_name= "dallas.py" # change this to the name of your process
tmp2 = os.popen("ps -Af").read()

if process_name not in tmp2[:] and globals.auto_dallas:
    newprocess="nohup python %s/%s &" % (globals.install_directory, process_name)
    os.system(newprocess)

process_name= "rfsensor.py" # change this to the name of your process
tmp2 = os.popen("ps -Af").read()

if process_name not in tmp2[:] and globals.auto_rfsensor:
    newprocess="nohup python %s/%s &" % (globals.install_directory, process_name)
    os.system(newprocess)

process_name= "dht22.py" # change this to the name of your process
tmp2 = os.popen("ps -Af").read()

if process_name not in tmp2[:]  and globals.auto_dht22:
    newprocess="nohup python %s/%s &" % (globals.install_directory, process_name)
    os.system(newprocess)

process_name= "subscribe.py" # change this to the name of your process
tmp2 = os.popen("ps -Af").read()

if process_name not in tmp2[:]  and globals.auto_lcd:
    newprocess="nohup python %s/%s &" % (globals.install_directory, process_name)
    os.system(newprocess)

process_name= "control.py" # change this to the name of your process
tmp2 = os.popen("ps -Af").read()

if process_name not in tmp2[:]  and globals.auto_control:
    newprocess="nohup python %s/%s &" % (globals.install_directory, process_name)
    os.system(newprocess)

