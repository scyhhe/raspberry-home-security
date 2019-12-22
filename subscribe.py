#!/usr/bin/env python
"""
subscribe.py 2.00 Home Alarm System Message Queue Broker
---------------------------------------------------------------------------------
 Works conjunction with host at www.privateeyepi.com                              
 Visit projects.privateeyepi.com for full details                                 
                                                                                  
 J. Evans March 2015       
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                                                       
                                                                                  
 Revision History                                                                  
 V1.00 - Created
 V2.00 - Support for multiple LCD makes
       - Ability to scroll through a log of events
       - Ability to display alarms
       - Display Armed/Disarmed using a tactile switch 
 ----------------------------------------------------------------------------------
"""

import sys
import time
import RPi.GPIO as GPIO
import paho.mqtt.client as paho
import thread
import globals
global broker_ip
global cycle_temperature
global temp_counter
global GPIOList
global UOMList
global LocationList
global HumidityList
global TempList
global TypeList
global start_time
global PrintToScreen
global armed
global SaveScreen
global activity_cnt
global activity_log
global log_cnt
global display_alarms
global alarm
global mqttc
global threadstart

GPIOList = []
LocationList = []
Humidity = []
UOMList = []
TempList = []
TypeList = []
SaveScreen = [0,0,0,0,0,0,0,0]
activity_log = []
armed=2
activity_cnt=0
log_cnt=0
alarm=False
threadstart=False

#Configure these settings to customize you LCD
broker_ip="127.0.0.1"
cycle_temperature = True
display_alarms = True
PrintToScreen = True
button_gpio=0 #This is BCM format not Rpi pin number!
num_saved_logs = 10 #the number of logs you wanted to be able to scroll through
lcd_type=1 # 1=HD44780, 2=Nokia

if lcd_type==1:
        from lcd_hd44780 import DisplayLCD
        
elif lcd_type==2:
        from lcd_nokia import DisplayLCD
        import Adafruit_Nokia_LCD as LCD
        import Adafruit_GPIO.SPI as SPI
        
def on_message(mosq, obj, msg):
    global cycle_tempeature
    global start_time
    global armed
    global SaveScreen
    global alarm
    
    tempmsg=str(msg.payload)
    RecordSet = tempmsg.split(',')
    if armed==1 and int(RecordSet[3])<>6: 
            RecordSet[7]=1
    if PrintToScreen==True: 
            print RecordSet
    if int(RecordSet[7])==1: armed=1
    if int(RecordSet[7])==2: armed=2
    if int(RecordSet[3])==6:  
            RecordSet=SaveScreen
            RecordSet[7]=armed
            if int(RecordSet[3])==0: 
                    RecordSet[3]=6
    if msg.topic=="alarm_activity":
            if alarm==False:
                    DisplayLCD(RecordSet)
            temp = tempmsg.split(',')
            SaveActivity(temp)
            start_time = time.time()
    if msg.topic=="temperature":
            if cycle_temperature:
                    add_to_temp_list(RecordSet[0],RecordSet[1],RecordSet[4],RecordSet[6],RecordSet[5],RecordSet[3])
            else:
                    if alarm==False:
                            DisplayLCD(RecordSet)
    SaveScreen=RecordSet
        
def SaveActivity(RecordSet):
        global activity_cnt
        global activity_log
        global alarm

        now = time.strftime("%d/%m %X") 
        if int(RecordSet[7])==1:
                RecordSet[1]="Armed"
        elif int(RecordSet[7])==2:
                RecordSet[1]="Disarmed"
        elif int(RecordSet[3])==8:
                RecordSet[2]="Alarm!!!"
                alarm=True
        elif int(RecordSet[3])==5 or int(RecordSet[3])==3 or int(RecordSet[3])==4: 
                return
        if activity_cnt >= num_saved_logs:
                del activity_log[0]
        else:
                activity_cnt=activity_cnt+1
        activity_log.append(str(now)+","+str(RecordSet[1])+","+str(RecordSet[2])+","+str(RecordSet[3]))
        if PrintToScreen: print activity_log[activity_cnt-1]
                
                
def add_to_temp_list(number, location, temperature, uom, humidity, type):
        global TempList
        global TypeList
        global LocationList
        global GPIOList
        global Humidity
        global UOMList
                
        found = False
        for i in range(len(GPIOList)):
                if GPIOList[i]==number:
                        found=True
                        break
        if found==False:
                GPIOList.append(number)
                LocationList.append(location)
                TempList.append(temperature)
                TypeList.append(type)
                UOMList.append(uom)
                Humidity.append(humidity)
        else:
                TempList[i] = temperature
                UOMList[i] = uom
                Humidity[i] = humidity
                TypeList[i] = type
                LocationList[i] = location

def DisplayNextTemperature():
      global TempList
      global TypeList
      global LocationList
      global temp_counter
      global cycle_tempeature
      global Humidity
      global UOMList
      global armed
      
      if cycle_temperature == True and len(TempList) > 0:
                if temp_counter+1 > len(TempList):
                        temp_counter=0
                rt=[GPIOList[temp_counter], LocationList[temp_counter],0, TypeList[temp_counter] ,TempList[temp_counter],Humidity[temp_counter],UOMList[temp_counter],armed]
                if alarm==False:
                        DisplayLCD(rt)
                temp_counter=temp_counter+1

def PollGPIO():
# Routine to continuously poll the IO ports on the Raspberry Pi
        global button_gpio
        global log_cnt
        global activity_log
        global start_time
        global activity_cnt
        global alarm
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(button_gpio, GPIO.IN)
        circuit = GPIO.input(button_gpio)
        if circuit==False:
                alarm=False
                if PrintToScreen==True: print "Button pushed "+str(activity_cnt) 
                if activity_cnt>0:
                        start_time = time.time()
                        log_cnt=log_cnt-1
                        if log_cnt<=0:
                                log_cnt=activity_cnt     
                        temp = activity_log[log_cnt-1].split(',')
                        if PrintToScreen==True: print temp
                        DisplayLCD([0,temp[1],temp[2],7,log_cnt,temp[3],0,0,temp[0]])

def ProcessMessage(rt):
        global mqttc
        global threadstart
        
        threadstart=True
        rc = mqttc.loop()
        threadstart=False

def ProcessMessageThread(rt):
        global threadstart
        
        try:
                if threadstart==False:
                        thread.start_new_thread(ProcessMessage, (rt, ) )
        except:
                print "Error: unable to start thread"
                exit

def main():
    global broker_ip
    global cycle_temperature
    global temp_counter
    global start_time
    global log_cnt
    global activity_cnt
    global mqttc

    globals.init()

    if lcd_type==2:
        globals.disp = LCD.PCD8544(23, 24, spi=SPI.SpiDev(0, 0, max_speed_hz=4000000))
    
    RecordSet = [0,0,"Welcome to**PrivateEyePi",5,0,0,0,0]
    DisplayLCD(RecordSet)
        
    temp_counter=0
    mqttc = paho.Client()
    mqttc.on_message = on_message
    mqttc.connect(broker_ip, 1883, 60)
    mqttc.subscribe("alarm_activity", 0)
    mqttc.subscribe("temperature", 0)
    start_time = time.time()
    
    rc = 0
    while rc == 0:
        ProcessMessageThread(rc)
        elapsed_time = time.time() - start_time
        if (elapsed_time > 10):
                log_cnt=activity_cnt
                if cycle_temperature:
                        DisplayNextTemperature()
                        start_time = time.time()
        if button_gpio>0:        
                PollGPIO()
                 
        time.sleep(.2)

    return 0

if __name__ == "__main__":
    sys.exit(main())




