#!/usr/bin/env python
"""
globals.py 11.00 PrivateEyePi Globals Parameters
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
 V1.00 - Release
 V2.00 - Added generic poll interval
 V3.00 - Incorporated rules functionality
 V4.00 - Added siren rule action, chime, siren beep delay
 v9.00 - Rules release     
 v10.00 - Added support for flexible sensor voltages
 V11.00 -  Added support for token auth
 V12.00 - Added support for multiple sensor per RF Module
 -----------------------------------------------------------------------------------
"""

def init():
	global PrintToScreen
	global token
	global RFPollInterval
	global smtp_server
	global smtp_user
	global smtp_pass
	global Farenheit
	global DallasSensorNumbers
	global DallasSensorDirectory
	global TemperaturePollInterval
	global GenericPollInterval
	global GPIOPollInterval
	global UseSiren
	global SirenGPIOPin
	global SirenTimeout
	global SirenStartTime
	global Armed
	global RemoteZoneDescription
	global ArmPin
	global DisarmPin
	global ArmDisarm
	global GPIO 
	global ChimeDuration
	global SirenPollInterval
	global SirenDelay
	global BeepDuringDelay
	global ButtonBList
	global ButtonBId
	global dht22_gpio
	global auto_dht22
	global auto_alarm
	global auto_rfsensor
	global auto_dallas
	global auto_lcd
	global auto_control
	global install_directory
	global email_type
	global ChimeGPIOPin
	global photopath
	global RelayPin
	global WRelayPin
	global VoltageList
	global MaxVoltage
	global LCDName
	global LCDTemperature
	global LCDAlarmActivity
	global lcd_ip
	global LCDChime
	global disp
	global AllowExternalControl
	global TMPBPrefix
	global TMPCPrefix
	global HUMPrefix
	global ANABPrefix
	global BUTTONPrefix

	#Token that has been registered on www.privateeyepi.com website
	token="acc8c3c811914ee354679919b8d4754c"

	# Set this to True if you want to send outputs to the screen
	# This is useful for debugging
	PrintToScreen=False

	# If you want to receive email alerts define SMTP email server details
	# This is the SMTP server, username and password trequired to send email through your internet service provider
	smtp_server="" # usually something like smtp.yourisp.com
	smtp_user=""   # usually the main email address of the account holder
	smtp_pass=""   # usually your email address password
	email_type=1   # 1 for No Encryption, 
				   # 2 for SSL and 
				   # 3 and TLS

	# Set the path to the photos that get attached to emails when
	# a rule is triggered to send photos
	photopath = "/home"

	#Indicator to record temperature in Farenheit
	Farenheit=False
			
	#Temperature settings
	#if you are using the dht22 temperature and humidity sensor set the gpio number and the pin number here
	# note!! the GPIO number and the pin number are not the same e.g GPIO4=RPIPin7
	dht22_gpio=4

	DallasSensorNumbers = []
	DallasSensorDirectory = []

	#Set the directory and sensor numbers for the Dallas temperature gauge
	DallasSensorNumbers.append(7) #sensor number defined in the number field in the GPIO settings
	#DallasSensorNumbers.append(80) #add more sensors..
	#DallasSensorNumbers.append() #add more sensors..

	DallasSensorDirectory.append("28-0000055d57dd") #directory name on RPI in the /sys/bus/w1/devices directory  
	#DallasSensorDirectory.append("28-000005020815") #add another directory 
	#DallasSensorDirectory.append("") #add another directory

	#Auto restart settings
	auto_dallas = False
	auto_alarm = False
	auto_dht22 = False
	auto_rfsensor = False
	auto_lcd = False
	auto_control = False
	install_directory = "/home/pi/pep" #The PrivateEyePi software directory

	# Set this to true if you want to connect an external siren. Put siren activation and deactivation code in the Siren function.
	UseSiren = False
	SirenGPIOPin = 18
	SirenDelay=30 #The amount of time the siren will delay before it sounds
	BeepDuringDelay = True #if your want the siren to beep during the SirenDelay period
	SirenTimeout = 30 #siren will timeout after 30 seconds
	ChimeGPIOPin = 18
	ChimeDuration = 5

	#Arm/Disarm zone from a switch
	ArmDisarm=False # set this to True if you want to arm/disarm using switches
	RemoteZoneDescription="" #The description of the zone you want to arm/disarm
	ArmPin=13
	DisarmPin=15
	Armed = True

	#Configure alternate voltages here. This is for wireless sensors that have a voltage
	#that is not the standard 3V. This voltage setting is used for the battery display
	#on the dashboard so the system knows what the maximum voltage is for the display
	#The below example will set the maximum voltage for Device ID 81 to 9V
	VoltageList = []
	MaxVoltage = []
	#VoltageList.append(92)
	#MaxVoltage.append(1.5)
	#VoltageList.append(81)
	#MaxVoltage.append(9)
	#...add more max voltages by copying the above two lines and updating the numbers in brackets....

	#Configure an LCD panel here
	LCDTemperature=False
	LCDAlarmActivity=False
	LCDChime=False
	lcd_ip="127.0.0.1"

	#Set this setting to True if you want to be able to send control commands from the web to your Raspberry Pi
	#The default to not allow external control
	#Applies to switch GPIO, send photos, or switch relay
	AllowExternalControl=False
	
	#An RF Mofule (like the FLEX) can support multiple sensors at the same time, 
	#but each RF module has one ID. The following prefixes are appended to the front 
	#of the ID to give each sensor a unique ID for PrivateEyePi
	#E.g. for a sensor with ID=25, TMPA will have and ID of 25, TMPB an ID of 125, TMPC an ID of 225
	TMPBPrefix="1"
	TMPCPrefix="2"
	HUMPrefix="3"
	ANABPrefix="4"
	BUTTONPrefix="" #not configured by default but add a prefix if you want to combine a BUTTON swicth with temperature
	
	
	

