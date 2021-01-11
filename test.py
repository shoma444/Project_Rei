# Written and developed by Shoma Yamanouchi, Brian J. Park, and Hannah Cheng
# Contact: syamanou@physics.utoronto.ca OR brianjmpark@gmail.com
# Website: https://sites.google.com/view/shoma-yamanouchi OR https://brianjmpark.github.io/ OR Hannah's websites
# version 1.0
# Developed in Python 2.7.18
version = '1.0'
DEVELOPED_BY_SHOMA = 'Easy A 2021 (c) was developed by:\nShoma Yamanouchi,\nBrian J. Park,\nand Hannah Cheng'

import os, sys, wx, csv, wx.adv
import wx.lib.scrolledpanel as scrolled
from wx.lib.colourdb import *
import datetime as dt
from icalendar import Calendar, Event

def write_ical(newexam):#newexam = classname, target, date
    # write iCal
    cal = Calendar()
    event = Event()
    examdate = dt.datetime.strptime(newexam[2] + ' 08:00','%Y/%m/%d %H:%M')
    event.add('summary', newexam[0]+' Exam')
    event.add('dtstart', examdate)
    event.add('dtend', examdate + dt.timedelta(hours=3))
    event.add('description','Final exam for '+newexam[0]+'.\nYour goal is '+newexam[1]+'%!\nGood luck!')
    #event.add('location', newexam)
    cal.add_component(event)

    with open('./save/'+newexam[0]+'_'+newexam[2].replace('/','-')+'.ics', 'wb') as ics:
        ics.write(cal.to_ical()) 
    os.system('open ./save/'+newexam[0]+'_'+newexam[2].replace('/','-')+'.ics')
    #os.system('rm ./save/'+newexam[0]+'_'+newexam[2].replace('/','-')+'.ics')

dat = ['MATH141','88','2021/01/25']
write_ical(dat)