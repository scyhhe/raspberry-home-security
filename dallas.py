#!/usr/bin/env python
"""
dallas.py 14.00 Dallas 1 wire interface to PrivateEyePi
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
 V1.00 - Created       
 V2.00 - Incorporation of rules functionality
 V9.00 - Rules Release    
 V10.00 - Fixed a bug with retries after bad reads of the DS18B20 sensor    
 V13.00 - Added LCD Functionality                                                                                               
 V14.00 - Simplified code and sensor automatically configured on PrivateEyePi
-----------------------------------------------------------------------------------
"""

import time
import RPi.GPIO as GPIO
import urllib2
import subprocess
import globals
from alarmfunctionsr import UpdateHost
from alarmfunctionsr import GetDataFromHost
from alarmfunctionsr import SendEmailAlert
from alarmfunctionsr import SendToLCD

#...

def fileexists(filename):
        try:
                with open(filename): pass
        except IOError:
                return False 
        return True

def GetTemperature(no):
        #Routine to read the temperature
        #Read the sensor 10 times checking the CRC until we have a good read 
        for retries in range(0, 10):        
                subprocess.call(['modprobe', 'w1-gpio'])
                subprocess.call(['modprobe', 'w1-therm'])
                
                # Open the file that we viewed earlier so that python can see what is in it. Replace the serial number as before.
                filename = "/sys/bus/w1/devices/"+globals.DallasSensorDirectory[no]+"/w1_slave"
                if (fileexists(filename)):
                        tfile = open(filename)
                else:
                        return 0
                # Read all of the text in the file.
                text = tfile.read()
                # Close the file now that the text has been read.
                tfile.close()
                #Perform a CRC Check
                firstline  = text.split("\n")[0]
                crc_check = text.split("crc=")[1]
                crc_check = crc_check.split(" ")[1]
                if crc_check.find("YES")>=0:
                        break
        #If after 10 tries we were unable to get a good read return 0
        if retries==9:
                return(0)
        # Split the text with new lines (\n) and select the second line.
        secondline = text.split("\n")[1]
        # Split the line into words, referring to the spaces, and select the 10th word (counting from 0).
        temperaturedata = secondline.split(" ")[9]
        # The first two characters are "t=", so get rid of those and convert the temperature from a string to a number.
        temperature = float(temperaturedata[2:])
        # Put the decimal point in the right place and display it.
        temperature = temperature / 1000
        temp = float(temperature)
        # Do the Farenheit conversion if required
        if globals.Farenheit:
                temp=temp*1.8+32
        temp = round(temp,2)
        return(temp)

                                  
def NotifyHostTemperature():
        numtemp = len(globals.DallasSensorNumbers)
        rt2=False
        for z in range(0,numtemp,1):
                TempBuffer = []
                TempBuffer.append(GetTemperature(z))
                if globals.Farenheit:
                        TempBuffer.append(1)
                else:
                        TempBuffer.append(0)
                TempBuffer.append(globals.DallasSensorNumbers[z])
                UpdateHost(14, TempBuffer)
        
        return (0)
                   
def main():
        global start_temperature_time
        global elapsed_temperature_time
        
        globals.init()
        start_temperature_time = time.time()
        elapsed_temperature_time=9999
        
        #Main Loop
        while True:
                        
            if (elapsed_temperature_time > 300):
                    start_temperature_time = time.time()
                    # Get the latest temperature
                    NotifyHostTemperature()
                    
            elapsed_temperature_time = time.time() - start_temperature_time
                
            time.sleep(.2)

if __name__ == "__main__":
        main()