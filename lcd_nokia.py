import time

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import globals

def DisplayLCD(RecordSet):
    
    #RecordSet is an array of 7 values
    #RecordSet[0] : GPIO_Pin_Number
    #RecordSet[1] : Location       
    #RecordSet[2] : Display Message
    #RecordSet[3] : type 1=Switch Open, 2=Switch Closed, 3=Temperature, 4=Temperature & Humidity, 5=Free format String, 6=Arm/Disarm, 7=Log, 8 = Alarm
    #RecordSet[4] : Tempeature Value
    #RecordSet[5] : Humidity Value
    #RecordSet[6] : Unit of measure
    #RecordSet[7] : Arm/Disarm
    #RecordSet[8] : DateTime
                    
    con=60
    #disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))30..+
    
    globals.disp.begin(contrast=con)
    globals.disp.clear()
    globals.disp.display()
    image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)   
    line1=str(RecordSet[1])
    type = int(RecordSet[3])
    
    fontstr="verdanab.ttf"
    fontsize=10
    
    fontstr2="verdanab.ttf"
    fontsize2=23
    
    fontsize3=8
    
    if type<>7:
            draw.line((0,40,LCD.LCDWIDTH,40), fill=0)
    
    if type==1: # Switch Open
            line2="Open"
            font = ImageFont.truetype(fontstr, fontsize)
            draw.text((1,5), line1, font=font)
            draw.text((1,15), line2, font=font)
                
    elif type==2: # Switch Closed
            line2="Closed"
            font = ImageFont.truetype(fontstr, fontsize)
            draw.text((1,5), line1, font=font)
            draw.text((1,15), line2, font=font)
            
    elif type==3: # Temperature
            temp = round(float(RecordSet[4]),1)
            line2=str(temp)+RecordSet[6]
            font = ImageFont.truetype(fontstr2, fontsize2)
            draw.text((0,-3), line2, font=font)
            font = ImageFont.truetype(fontstr, fontsize)
            draw.text((1,20), line1, font=font)
            
    elif type==4: # Temerature & Humidity
            temp = round(float(RecordSet[4]),1)
            line2=str(temp)+str(RecordSet[6])
            line3=str(round(float(RecordSet[5]),0)).replace(".0", "")+"% humidity"
            font = ImageFont.truetype(fontstr2, fontsize2)
            draw.text((0,-6), line2, font=font)
            font = ImageFont.truetype(fontstr, fontsize)
            draw.text((1,17), line3, font=font)
            draw.text((1,27), line1, font=font)
            
    elif type==5: # Free format string
            temp = RecordSet[2].split('**')
            line1=temp[0]
            line2=temp[1]
            font = ImageFont.truetype(fontstr, fontsize)
            draw.text((1,5), line1, font=font)
            draw.text((1,15), line2, font=font)
            
    elif type==6: # Arm/Disarm
            line1="Armed"
            
    elif type==7: # Log
            line1="Activity Log "+str(RecordSet[4])
            line2=RecordSet[8] 
            line3=RecordSet[1]
            line4=""
            if int(RecordSet[5])==1:
                    line4="Open"
            if int(RecordSet[5])==2:
                    line4="Closed"
            if int(RecordSet[5])==8:
                    line4=str(RecordSet[2])        
            font = ImageFont.truetype(fontstr, fontsize3)
            draw.text((1,0), line1, font=font)
            draw.text((1,10), line2, font=font)
            draw.text((1,20), line3, font=font)
            draw.text((1,30), line4, font=font)
    
    elif type==8: # Alarm
            line2="Alarm!!!"
            font = ImageFont.truetype(fontstr, fontsize)
            draw.text((1,5), line1, font=font)
            draw.text((1,15), line2, font=font)
            
    else:
            line2="Unassigned"
            font = ImageFont.truetype(fontstr, fontsize)
            draw.text((1,5), line1, font=font)
            draw.text((1,15), line2, font=font)

    if int(RecordSet[7])==1: 
            line1="Alarm : Armed"
            font = ImageFont.truetype(fontstr2, fontsize3)
            draw.text((10,40), line1, font=font)

    globals.disp.image(image)
    globals.disp.display()




