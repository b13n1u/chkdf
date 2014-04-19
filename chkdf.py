#!/usr/bin/env python
# Check the FS usage and send an email when one of the tresholds is reached 
# 
# v0.002

#from __future__ import division
#TODO: Don't use shell=True, change it

import subprocess
from email.mime.text import MIMEText
from datetime import date
import smtplib

SMTP_SERVER = "example.com"    #sender server address
SMTP_PORT = 25			
SMTP_USERNAME = "sender@example.com"    #username 
SMTP_PASSWORD = ""	      		#WARNING password in plaintext 

EMAIL_TO = ["me@example1.com", "example@example.com"]
EMAIL_FROM = "sender@example.com"
EMAIL_SUBJECT = "High FS space usage on host "    #TODO add hostname 

DATE_FORMAT = "%d/%m/%Y-%H:%M"
EMAIL_SPACE = ", "

DATA=''

TRESHOLD1 = 92   #Warning treshold Usage in %
TRESHOLD2 = 98   #Critical treshold
aaa = []

p = subprocess.Popen('df -hP', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

for line in p.stdout.readlines():
#    print line,
    aaa.append(line.split())
retval = p.wait()

if retval != 0:             #exit if df fails
    print "Ooops something is wrong!!"
    exit(1)

aaa.pop(0)      #remove the first line with the column names

for i in aaa:
    i[4] = i[4].replace('%','')
    if int(i[4]) > TRESHOLD1:
        DATA = DATA + 'WARNING!! Mount point %s (%s) is %s%% full. There is %s left (of %s).\n' % (i[5], i[0],i[4],i[3],i[1])
#TODO add verbose :)
# uncomment folllowing lines in case you would like to see the output:  
#        print 'WARNING!! Mount point %s (%s) is %s%% full. There is %s left (of %s).\n' % (i[5], i[0],i[4],i[3],i[1])
#        print "Filesystem    Size    Used    Avail    Used    Mounted on"
#        print "%s    %s    %s    %s    %s    %s" %(i[0],i[1],i[2],i[3],i[4],i[5])
    elif int(i[4]) > TRESHOLD2:
        DATA = DATA + 'CRITICAL!! Mount point %s (%s) is %s%% full. There is %s left (of %s).\n' % (i[5], i[0],i[4],i[3],i[1])
# uncomment folllowing lines in case you would like to see the output:  
#        print 'CRITICAL!! Mount point %s (%s) is %s%% full. There is %s left (of %s).\n' % (i[5], i[0],i[4],i[3],i[1])
#        print "Filesystem    Size    Used    Avail    Used    Mounted on"
#        print "%s    %s    %s    %s    %s    %s" %(i[0],i[1],i[2],i[3],i[4],i[5])

def send_email():
    msg = MIMEText(DATA)
    msg['Subject'] = EMAIL_SUBJECT + " %s" % (date.today().strftime(DATE_FORMAT))
    msg['To'] = EMAIL_SPACE.join(EMAIL_TO)
    msg['From'] = EMAIL_FROM
    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mail.starttls()
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)
    mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    mail.quit()


if len(DATA) != 0:          #if there is anything to send then  send
#    print "Mail sent"
    send_email()


