#!/usr/bin/env python
"""
rfthermtest.py 1.00 PrivateEyePi RF Temperature Test Program
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
 -----------------------------------------------------------------------------------
"""

import serial
import time
import sys
from time import sleep

def main():
        # declare to variables, holding the com port we wish to talk to and the speed
        port = '/dev/ttyAMA0'
        baud = 9600
        
        # open a serial connection using the variables above
        ser = serial.Serial(port=port, baudrate=baud)
        
        # wait for a moment before doing anything else
        sleep(0.2)    
    
        print "Please wait max 5 mins for the temperature transmitter to transmit..."
    
        while True:
                while ser.inWaiting():
                        # read a single character
                        char = ser.read()
                        # check we have the start of a LLAP message
                        if char == 'a':
                                # start building the full llap message by adding the 'a' we have
                                llapMsg = 'a'
                                
                                # read in the next 11 characters form the serial buffer
                                # into the llap message
                                llapMsg += ser.read(11)
                                
                                # now we split the llap message apart into devID and data
                                devID = llapMsg[1:3]
                                data = llapMsg[3:]
                                
                                print "Device Number : " + devID
                                print "Temperature data : " + data
                                
                        sleep(0.2)
   
if __name__ == "__main__":
        main()



   
   

