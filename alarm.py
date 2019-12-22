#!/usr/bin/env python
"""
alarm.py 14.00 Home Alarm System
---------------------------------------------------------------------------------
 Works conjunction with host at www.privateeyepi.com                              
 Visit projects.privateeyepi.com for full details                                 
                                                                                  
 R. Brown 2018
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                                                       
                                                                                  
 Revision History                                                                  
 V8.00 - Alarm system that utilizes the rules function for actions/triggers
 V8.10 - Added siren rule action, chime, siren beep delay
 V9    - Rules release     
 V13   - Added LCD Functionality   
 V14   - Moved to token authentication method 
 ----------------------------------------------------------------------------------
"""

import time
import RPi.GPIO as GPIO
import urllib2
import subprocess
import globals
from alarmfunctionsr import UpdateHost
from alarmfunctionsr import GetDataFromHost
from alarmfunctionsr import SendEmailAlert
from alarmfunctionsr import SendEmailAlertFromRule
from alarmfunctionsr import SendEmailAlertThread
from alarmfunctionsr import SendToLCD

def BuildGPIOList():
	# Build a list of zones and store in memory
	global GPIOList
	global numgpio
	global AlarmActioned
	global Locations

	AlarmActioned = []    
	Locations = []
	numgpio=0

	RecordSet = GetDataFromHost(2,[0])
	if RecordSet==False:
			return
	numgpio = len(RecordSet)

	GPIOList = []
	for i in range(numgpio):
			if isNumber(RecordSet[i][0]):
					GPIOList.append(RecordSet[i][0])
			Locations.append(RecordSet[i][1])

	numgpio = len(GPIOList)    
	# Initialize the Raspberry Pi board pin numbers to the armed zones
	GPIO.setmode(GPIO.BOARD)        
	if globals.ArmDisarm == True:
			GPIO.setup(globals.ArmPin, GPIO.IN) #Arm pin setup
			GPIO.setup(globals.DisarmPin, GPIO.IN) #Disarm pin setup

	for i in range(0,numgpio,1):
			GPIO.setup(GPIOList[i], GPIO.IN)
			circuit = GPIO.input(GPIOList[i])
			AlarmActioned.append(circuit)

def CheckArmDisarm():    
	if globals.ArmDisarm==True:
		globals.ArmKeyPressed=GPIO.input(globals.ArmPin)
		globals.DisarmKeyPressed=GPIO.input(globals.DisarmPin)
		
		if not globals.Armed and globals.ArmKeyPressed:
			globals.Armed=True
			ArmZone()
			
		if globals.Armed and globals.DisarmKeyPressed:
			globals.Armed=False
			DisarmZone()

def ArmZone():
	# Routine to arm a zone  
	TempBuffer = []
	TempBuffer.append(globals.RemoteZoneDescription)
	rt=UpdateHost(18, TempBuffer)
	if globals.LCDAlarmActivity==True:
			#SendToLcd receives an array of 7 values
			#RecordSet[7] : Armed/Disarmed 1=Armed, 2=Disarmed
			SendToLCD([0,0,0,0,0,0,0,1])
	return (0)

def DisarmZone():
	# Routine to arm a zone  
	TempBuffer = []
	TempBuffer.append(globals.RemoteZoneDescription)
	rt=UpdateHost(19, TempBuffer)
	if globals.LCDAlarmActivity==True:
			#SendToLcd receives an array of 7 values
			#RecordSet[7] : Armed/Disarmed 1=Armed, 2=Disarmed
			SendToLCD([0,0,0,0,0,0,0,2])
	return (0)

               
def InitializeHostGPIO():
	global GPIOList

	SensorList = []
	SensorList.append(0)
	y=0
	for x in AlarmActioned:
			SensorList.append(GPIOList[y])
			SensorList.append(AlarmActioned[y])
			y=y+1
	SensorList[0]=y
	# Send the status of the pins to the server
	rt=UpdateHost(23,SensorList)
                    
def PollGPIO():
# Routine to continuously poll the IO ports on the Raspberry Pi
	global ciruit
	global GPIOList
	global numgpio
	global GPIO
	global AlarmActioned

	circuit=False
			
	for z in range(0,numgpio,1):
			circuit = GPIO.input(GPIOList[z])
			if circuit==True:
					if not AlarmActioned[z]: 
							NotifyHostEvent(z, 1)
							AlarmActioned[z]=True
							
			else: #resetting the IO after the switch is reset (e.g. door closed)
					if AlarmActioned[z]==True:
							AlarmActioned[z]=False
							NotifyHostEvent(z, 0)
					AlarmActioned[z]=False
	CheckArmDisarm()       
                
def NotifyHostEvent(z, status):
	global GPIOList
	global Locations

	# Notify the host that an IO was switched (e.g. door open)
	HostEvent=[]
	HostEvent.append(GPIOList[z])
	HostEvent.append(status)
	if globals.LCDAlarmActivity==True:
			#SendToLcd receives an array of 7 values
			#RecordSet[0] : GPIO_Pin_Number
			#RecordSet[1] : Location       
			#RecordSet[2] : Display Message
			#RecordSet[3] : type 1=Switch Open, 2=Switch Closed, 3=Temperature, 4=Temperature & Humidity, 5=Free format String, 6=Arm/Disarm, 7=Log
			#RecordSet[4] : Tempeature Value
			#RecordSet[5] : Humidity Value
			#RecordSet[6] : Unit of measure, 0=Centigrade, 1=Fahrenheit
			#RecordSet[7] : Armed/Disarmed 1=Armed, 2=Disarmed
			#RecordSet[8] : DateTime
			
			if status==0: switch=2
			else: switch=1
			SendToLCD([GPIOList[z],Locations[z],0,switch,0,0,0,0,0])
	rt=UpdateHost(26,HostEvent)
	if rt==3:
			if globals.LCDAlarmActivity==True:
					SendToLCD([GPIOList[z],Locations[z],0,8,0,0,0,0,0])
			return(True)
	else:
			return(False)      

def PollRoutine():
	global start_time
	global elapsed_time

	#Poll for changes to GPIO settings
	if (elapsed_time > 600):
			start_time = time.time()
			BuildGPIOList()
			InitializeHostGPIO()

def isNumber(x):
	# Test whether the contents of a string is a number
	try:
			val = int(x)
	except ValueError:
			return False
	return True

def main():
	global start_time
	global elapsed_time
	global AlarmActioned

	globals.init()

	#Start Main Program Loop

	AlarmActioned = []
	BuildGPIOList()
	InitializeHostGPIO()
	 
	#Main Loop
	# loop to monitor armed zones and create an alarm
	start_time = time.time()

	while True:
		
			PollGPIO()
			 
			elapsed_time = time.time() - start_time
			
			PollRoutine()
				
			time.sleep(.2)

if __name__ == "__main__":
        main()