#!/usr/bin/env python
import paho.mqtt.client as paho
import globals
import time
from alarmfunctionsr import SendToLCD

globals.init()

#RecordSet is an array of 7 values
#RecordSet[0] : GPIO_Pin_Number
#RecordSet[1] : Location       
#RecordSet[2] : Display Message
#RecordSet[3] : type 1=Switch Open, 2=Switch Closed, 3=Temperature, 4=Temperature & Humidity, 5=Free format String, 6=Arm/Disarm, 7=Log, 8 = Alarm
#RecordSet[4] : Tempeature Value
#RecordSet[5] : Humidity Value
#RecordSet[6] : Unit of measure, 0=Centigrade, 1=Fahrenheit
#RecordSet[7] : Armed/Disarmed 1=Armed, 2=Disarmed
#RecordSet[8] : Date/Time

#Custom Message
RecordSet = [0,0,"Welcome to**PrivateEyePi",5,0,0,0,0,0]
SendToLCD(RecordSet)
time.sleep(2)

#Door Closed
RecordSet = [0,"Front Door",0,2,0,0,0,0,0]
SendToLCD(RecordSet)
time.sleep(2)

#Alarm Armed
RecordSet = [0,0,0,6,0,0,0,1,0]
SendToLCD(RecordSet)
time.sleep(2)

#Temperature
RecordSet = [12,"Inside",0,3,22.5,0,0,0,0]
SendToLCD(RecordSet)
time.sleep(2)

#Temperature
RecordSet = [13,"Outside",0,3,-28.7,0,0,0,0]
SendToLCD(RecordSet)
time.sleep(2)

#Temperature & Humidity
RecordSet = [13,"Green House",0,4,-28.5,43,0,0,0]
SendToLCD(RecordSet)
time.sleep(2)

#Door Open
RecordSet = [0,"Front Door",0,1,0,0,0,0,0]
SendToLCD(RecordSet)
time.sleep(2)

#Alarm
RecordSet = [0,"Front Door",0,8,0,0,0,0,0]
SendToLCD(RecordSet)

#Alarm Disarmed
RecordSet = [0,0,0,6,0,0,0,2,0]
SendToLCD(RecordSet)
time.sleep(2)
