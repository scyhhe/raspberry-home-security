#!/usr/bin/env python
"""
rfsensor.py v18 PrivateEyePi RF Sensor Interface
---------------------------------------------------------------------------------
 Works conjunction with host at www.privateeyepi.com                              
 Visit projects.privateeyepi.com for full details                                 
																				  
 J. Evans October 2013       
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                                                       
																				  
 Revision History                                                                  
 V1.00 - Release
 V2.00 - Incorporation of rules functionality  
 V3.00 - Incorporated Button B logic
 V3.01 - High CPU utilization fixed
 V9    - Rule release   
 V10   - Added support for the BETA single button power saving wireless switch   
	   - Functionality added for wireless temperature and humidity sensor  
 V11   - Fixed a bug with negative readings from a DHT22 sensor
 V13   - Publish temperature to LCD
 V14   - Added auto sensor creation on the server, dropped support for obsolete two button sensors
 V15   - Added token based authentication
 V16   - Removed delay to speed up serial polling
 V17   - 
 V18   - Fixed bug wireles switch BUTTONON and BUTTONOFF sensing same state
 V20   - Changed STATEON STATEOFF to not trigger rules or log on the server
 -----------------------------------------------------------------------------------
"""

import serial
import globals
import time
import sys
import thread
from alarmfunctionsr import UpdateHostThread
from alarmfunctionsr import GetDataFromHost
from alarmfunctionsr import SendEmailAlert
from alarmfunctionsr import SendToLCD
from time import sleep
global measure

def dprint(message):
	if (globals.PrintToScreen):
		print message

def ProcessMessage(value, DevId, PEPFunction):
# Notify the host that there is new data from a sensor (e.g. door open)
	global measure		   
	hostdata =[]
	hostdata.append(DevId)
	hostdata.append(value)
	if PEPFunction==22: #Battery
		MaxVoltage=3
		for z in range (0,len(globals.VoltageList)):
			if globals.VoltageList[z] == int(DevId):
				MaxVoltage=globals.MaxVoltage[z]
		hostdata.append(MaxVoltage) #MaxVoltage
	if PEPFunction==37: #Temperature or Analog
		hostdata.append(measure)
		
	rt=UpdateHostThread(PEPFunction,hostdata)
	return(0)

def DoFahrenheitConversion(value):
	global measure
	if globals.Farenheit:
		value = float(value)*1.8+32
		value = round(value,2)
		measure = '1'
	else:
		measure='0'
	return(value)
		
def main():
		globals.init()
		global measure
		sensordata=''
		currdevid=''

		# loop until the serial buffer is empty

		start_time = time.time()

		#try:
		while True:

				# declare to variables, holding the com port we wish to talk to and the speed
				port = '/dev/ttyAMA0'
				baud = 9600

				# open a serial connection using the variables above
				ser = serial.Serial(port=port, baudrate=baud)

				# wait for a moment before doing anything else
				sleep(0.2)        
				while ser.inWaiting():
						# read a single character
						char = ser.read()
						# check we have the start of a LLAP message
						if char == 'a':
								sleep(0.01)
								start_time = time.time()
								
								# start building the full llap message by adding the 'a' we have
								llapMsg = 'a'

								# read in the next 11 characters form the serial buffer
								# into the llap message
								llapMsg += ser.read(11)

								# now we split the llap message apart into devID and data
								devID = llapMsg[1:3]
								data = llapMsg[3:]
								
								dprint(time.strftime("%c")+ " " + llapMsg)
																
								if data.startswith('BUTTONON'):
										devID=globals.BUTTONPrefix+devID
										sensordata=0
										PEPFunction=26

								if data.startswith('STATEON'):
										devID=globals.BUTTONPrefix+devID
										sensordata=0
										PEPFunction=38

								if data.startswith('STATEOFF'):
										devID=globals.BUTTONPrefix+devID
										sensordata=1
										PEPFunction=38

								if data.startswith('BUTTONOFF'):
										sensordata=1
										PEPFunction=26

								if data.startswith('TMPA'):
										sensordata=DoFahrenheitConversion(str(data[4:].rstrip("-")))
										PEPFunction=37
								
								if data.startswith('ANAA'):
										sensordata=str(data[4:].rstrip("-"))
										sensordata=(float(sensordata)-1470)/16 #convert it to a reading between 1(light) and 48 (dark)
										sensordata=str(sensordata)
										PEPFunction=37
										measure='2'
								
								if data.startswith('ANAB'):
										devID=globals.ANABPrefix+devID
										sensordata=str(data[4:].rstrip("-"))	
										sensordata=(float(sensordata)-1470)/16 #convert it to a reading between 1(light) and 48 (dark)
										sensordata=str(sensordata)
										measure='2'
										PEPFunction=37
								
								if data.startswith('TMPC'):
										devID=globals.TMPCPrefix+devID
										sensordata=DoFahrenheitConversion(str(data[4:].rstrip("-")))
										PEPFunction=37
								
								if data.startswith('TMPB'): 
										devID=globals.TMPBPrefix+devID
										sensordata=DoFahrenheitConversion(str(data[4:].rstrip("-")))
										PEPFunction=37
																				
								if data.startswith('HUM'):
										devID=globals.HUMPrefix+devID
										sensordata=str(data[3:].rstrip("-"))								
										PEPFunction=37
										measure='2'
												
								if data.startswith('BATT'):
										sensordata=data[4:].strip('-')
										PEPFunction=22
								
								if ((currdevid==devID) and (currvalue==sensordata)) or (sensordata==""): #ignore duplicates
										dprint("Ignoring message");
								else:
										currvalue=sensordata
										currdevid=devID
										ProcessMessage(currvalue, devID, PEPFunction)
						measure=''
						sensordata=''
					
				elapsed_time = time.time() - start_time
				if (elapsed_time > 2):
						currvalue=""
						sensordata=""
						currdevid=""
		   
if __name__ == "__main__":
		main()



   
   


