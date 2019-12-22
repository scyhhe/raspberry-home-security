#!/usr/bin/env python
"""
lcdtest.py 2.00 Home LCD Test Message Utility
---------------------------------------------------------------------------------                            
 Visit projects.privateeyepi.com for full details                                 
                                                                                  
 J. Evans March 2015       
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                                                       
                                                                                  
 Revision History                                                                  
 V2.00 - Created
 ----------------------------------------------------------------------------------
"""

lcd_type=1 # 1=HD44780, 2=Nokia

if lcd_type==1:
        from lcd_hd44780 import DisplayLCD
elif lcd_type==2:
        from lcd_nokia import DisplayLCD

#The DisplayLCD() function takes 9 parameters:
#1. GPIO_Pin_Number
#2. Location       
#3. Display Message
#4. Type 1=Switch Open, 2=Switch Closed, 3=Temperature, 4=Temperature & Humidity, 5=Free format String, 6=Arm/Disarm, 7=Log, 8 = Alarm
#5. Tempeature Value
#6. Humidity Value
#7. Unit of measure, 0=Centigrade, 1=Fahrenheit
#8. Armed/Disarmed 1=Armed, 2=Disarmed
#9. Date/Time

DisplayLCD([0,0,"Hello World!!**Hello World!!",5,0,0,0,0]) 

