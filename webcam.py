######################################################################################
## webcam.py 3.00 Creates an alarm alert from webcam motion                         ##
## ---------------------------------------------------------------------------------##
## Works conjunction with host at www.privateeyepi.com                              ##
## Visit projects.privateeyepi.com for full details                                 ##
##                                                                                  ##
## R. Brown 2018                                                                    ##
##                                                                                  ##
## Revision History                                                                 ## 
## V1.00 - Initial version created                                                  ##
## V2.00 - Added email alerts                                                       ##
## V3.00 - Moved to token based authentication										##
#####################################################################################

import time
import urllib2
import subprocess
global token
global PrintToScreen 
global smtp_server
global smtp_user
global smtp_pass
global EmailPhoto
global SensorNumber
global SendEmails
import sys
import smtplib
import os, glob, time, operator
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

#Configure the sensor number that you set up on the server
SensorNumber = 99

# If you want to receive email alerts define SMTP email server details
# This is the SMTP server, username and password trequired to send email through your internet service provider
# If you have a GMAIL or Yahoo account or one that uses encryption you need to make the relevant changes 
# to the SendEmailPhoto() and SendEmail() functions below. For help on how to do this go to:
# http://projects.privateeyepi.com/home/home-alarm-system-project/installation/configure-alarmpy-with-user-and-password
smtp_server="smtp.gmail.com"    # usually something like smtp.yourisp.com or smtp.gmail.com or smtp.mail.yahoo.com
smtp_user="mrkstinger@gmail.com"      # usually the main email address of the account holder
smtp_pass="06026203"      # usually your email address password

#Token that has been registered on www.privateeyepi.com website
token="acc8c3c811914ee354679919b8d4754c"

# Set this to True if you want to send outputs to the screen
# This is useful for debugging
PrintToScreen=False

# Change this to your path where the 
# web cam pictures are stored. 
# *.jpg means all JPEG files
photopath = "/home/webcam/*.jpg"

#set the following to true if you want to send email alerts
SendEmails=True

#set the following to True if you want to attach photos
#to your email alerts. The latest photo specified in the
#photopath directory will be sent
EmailPhoto=True

def get_latest_photo(files):
    lt = operator.lt
    if not files:
        return None
    now = time.time()
    latest = files[0], now - os.path.getctime(files[0])
    for f in files[1:]:
        age = now - os.path.getctime(f)
        if lt(age, latest[1]):
            latest = f, age
    return latest[0]

def SendEmailPhoto(SensorNumber):
        global smtp_server
        global smtp_user
        global smtp_pass      
        global photopath
        global smtp_server
        global smtp_user
        global smtp_pass
    
        # Get the email addresses that you configured on the server
        RecordSet = GetDataFromHost(5,[0])
        if RecordSet==False:
                return
        
        numrows = len(RecordSet)
        
        if smtp_server=="":
                return
                
        for i in range(numrows):
                # Define email addresses to use
                addr_to   = RecordSet[i][0]
                addr_from = smtp_user      
        
                files = glob.glob(photopath)
                latestphoto = get_latest_photo(files)
                msgtext = BuildMessage(SensorNumber);
                
                msg = MIMEMultipart() 
            
                addr_to   = RecordSet[i][0]
                addr_from = smtp_user
                msg['To']   = addr_to 
                msg['From'] = addr_from
                msg['Subject'] = "Webcam Motion Alert" 
                msg.preamble = 'Multipart message.\n'  
                part = MIMEText(msgtext) 
                msg.attach(part)
                part = MIMEApplication(open(latestphoto,"rb").read())
                part.add_header('Content-Disposition', 'attachment', filename=latestphoto)
                msg.attach(part)
                                
                # Send the message via an SMTP server with no encryption
                #s = smtplib.SMTP(smtp_server)
                #s.login(smtp_user,smtp_pass)
                #s.sendmail(addr_from, addr_to, msg.as_string())
                
                # Send the message via an SMTP server with TLS encryption e.g. YAHOO!
                # uncommend the next 4 lines and comment the above 3 starting with s = smtplib.SMTP(smtp_server)
                s = smtplib.SMTP(smtp_server,587)
                s.ehlo()
                s.starttls()
                s.ehlo()

                # Send the message via an SMTP server with SSL encryption e.g. GMAIL
                # uncommend the next 3 lines and comment the above 3 starting with s = smtplib.SMTP(smtp_server)
                #s = smtplib.SMTP_SSL(smtp_server, 465)
                #s.login(smtp_user,smtp_pass)
                #s.sendmail(msg['From'], msg['To'], msg.as_string())

                s.quit()
                if PrintToScreen: print msg;
              
def NotifyHostEvent(WebcamNumber):

    # Notify the host that an IO was switched (e.g. door open)
    rt=UpdateHost(13,[WebcamNumber])
    # The host will return True if this IO port is linked to a zone that is armed, then send an email
    return(rt)      
           
def SendEmailAlert(SensorNumber):
        global smtp_server
        global smtp_user
        global smtp_pass
    
        # Get the email addresses that you configured on the server
        RecordSet = GetDataFromHost(5,[SensorNumber])
        if RecordSet==False:
                return
        
        numrows = len(RecordSet)
        
        if smtp_server=="":
                return
                
        for i in range(numrows):
                # Define email addresses to use
                addr_to   = RecordSet[i][0]
                addr_from = smtp_user #Or change to another valid email recognized under your account by your ISP      
                # Construct email
                msg = MIMEText(BuildMessage(SensorNumber))
                msg['To'] = addr_to
                msg['From'] = addr_from
                msg['Subject'] = 'Alarm Notification' #Configure to whatever subject line you want
                
                # Send the message via an SMTP server
                s = smtplib.SMTP(smtp_server)
                s.login(smtp_user,smtp_pass)
                s.sendmail(addr_from, addr_to, msg.as_string())
                
                # Send the message via an SMTP server with TLS encryption e.g. YAHOO!
                # uncommend the next 4 lines and comment the above 3 starting with s = smtplib.SMTP(smtp_server)
                #s = smtplib.SMTP(smtp_server,587)
                #s.ehlo()
                #s.starttls()
                #s.ehlo()

                # Send the message via an SMTP server with SSL encryption e.g. GMAIL
                # uncommend the next 3 lines and comment the above 3 starting with s = smtplib.SMTP(smtp_server)
                #s = smtplib.SMTP_SSL(smtp_server, 465)
                #s.login(smtp_user,smtp_pass)
                #s.sendmail(msg['From'], msg['To'], msg.as_string())
                
                s.quit()
                if PrintToScreen: print msg;


def GetDataFromHost(function,opcode):
# Request data and receive reply (request/reply) from the server
 
    script_path = "https://www.privateeyepi.com/alarmhost.php?token="+token+"&function="+str(function)
    
    i=0
    for x in opcode:
        script_path=script_path+"&opcode"+str(i)+"="+str(opcode[i])
        i=i+1
        
    if PrintToScreen: print script_path 
    try:
        rt = urllib2.urlopen(script_path)
    except urllib2.HTTPError:
        return False
    temp=rt.read()
    if PrintToScreen: print temp
    
    l = find_all(temp,"/n");
    RecordSet = temp.split(',')
    c=[]
    y=0
    c.append([])
    for x in RecordSet:
        if x=="/n":
            y=y+1
            if y < l:
                c.append([])
        else:
            if isNumber(x):
                c[y].append(int(x))
            else:
                c[y].append(x)
        if x=="/FALSE":
            return False    
    return(c)

def UpdateHost(function,opcode):
# Sends data to the server
    global token
    global PrintToScreen
    
    script_path = "https://www.privateeyepi.com/alarmhost.php?token="+token+"&function="+str(function)

    i=0
    for x in opcode:
        script_path=script_path+"&opcode"+str(i)+"="+str(opcode[i])
        i=i+1
    
    if PrintToScreen: print "Host Update: "+script_path 
    try:
        rt=urllib2.urlopen(script_path)
    except urllib2.HTTPError:
        if PrintToScreen: print "HTTP Error"
        return False
    temp=rt.read()
    if PrintToScreen: print temp
    if temp=="TRUE":
        return(1)
    else:
        return(0)

def find_all(a_str, sub):
    start = 0
    cnt=0
    while True:
        start = a_str.find(sub, start)
        if start == -1: 
            return cnt
        start += len(sub)
        cnt=cnt+1

def isNumber(x):
    # Test whether the contents of a string is a number
    try:
        val = int(x)
    except ValueError:
        return False
    return True

def BuildMessage(SensorNumber):
        # Routine to fetch the location and zone descriptions from the server  
        
        RecordSet = GetDataFromHost(6,[SensorNumber])
        if PrintToScreen: print RecordSet
        if RecordSet==False:
            return  
        zonedesc=RecordSet[0][0]
        locationdesc = RecordSet[0][1]
        messagestr="This is an automated email from your house alarm system. Alarm activated for Zone: "+zonedesc+" ("+locationdesc+")"
        return messagestr


#Start Main Program

if smtp_server=="": 
        print "No smtp server defined"
        exit
if smtp_user=="": 
        print "No smtp user defined"
        exit
if smtp_pass=="":
        print "No smtp password defined"
        exit
if token=="": 
        print "No token defined"
        exit

rt=NotifyHostEvent(SensorNumber)
if SendEmails and rt==True:
        if EmailPhoto==True:
                SendEmailPhoto(SensorNumber)
        else:
                SendEmailAlert(SensorNumber)
         