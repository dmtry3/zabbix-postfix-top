#!/usr/bin/python3

import json
import os
import sys
import re
#mport subprocess

lim = int(sys.argv[2])
cmd = sys.argv[1]

def topsenders():
    cmdline = "pflogsumm -d today --bounce_detail=0 --deferral_detail=0 --no_no_msg_size --smtpd_warning_detail=0 --reject_detail=0 /var/log/maillog | sed -n '/Senders by message count/,$p'  | sed -n 3,10p"
    logSum = os.popen(cmdline).readlines()
    ans = 0
    for i in logSum:
        mt = 0
        cnt = int(re.search('^\s*(\d+)', i).group(1))
        name = re.search('^\s*(\d+)\s*(.*)', i).group(2)
        excl = open("/etc/zabbix/posttop.excl", "r")
        if cnt >= lim:
            while True:
                ree = excl.readline().rstrip('\n')
                if not ree:
                    break
                fnd = re.search(ree, name)
                if fnd:
                    mt = 1      
                    break                
            if mt == 0:
                ans = ans +1
                print (cnt, name)
    if not ans:
        print('-')

def toprecp():
    cmdline = "pflogsumm -d today --bounce_detail=0 --deferral_detail=0 --no_no_msg_size --smtpd_warning_detail=0 --reject_detail=0 /var/log/maillog | sed -n '/Recipients by message count/,$p'  | sed -n 3,10p"
    logSum = os.popen(cmdline).readlines()
    ans = 0
    for i in logSum:
        mt = 0
        cnt = int(re.search('^\s*(\d+)', i).group(1))
        name = re.search('^\s*(\d+)\s*(.*)', i).group(2)
        excl = open("/etc/zabbix/posttop.excl", "r")
        if cnt >= lim:
            while True:
                ree = excl.readline().rstrip('\n')
                if not ree:
                    break
                fnd = re.search(ree, name)
                if fnd:                
                    mt = 1
                    break
            if mt == 0:
                ans = ans +1
                print (cnt, name)
    if not ans:
        print('-')
if cmd == 'sndr':
    topsenders()
elif cmd == 'recv':
    toprecp()
else:
    print ("f1111f")

#print (logSum)
