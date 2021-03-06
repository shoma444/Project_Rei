# Written and developed by Shoma Yamanouchi, Brian J. Park, and Hannah Cheng
# Contact: syamanou@physics.utoronto.ca OR brianjmpark@gmail.com
# Website: https://sites.google.com/view/shoma-yamanouchi OR https://brianjmpark.github.io/ OR Hannah's websites
# version 1.0
# Developed in Python 2.7.18
version = '1.0'
AppName = 'Exam Goals' # Placeholder app name
DEVELOPED_BY_SHOMA = AppName + ' 2021 (c) was developed by:\nShoma Yamanouchi,\nBrian J. Park,\nand Hannah Cheng'

import os, sys, wx, csv, wx.adv, pickle, random
import wx.lib.scrolledpanel as scrolled
import wx.lib.colourdb as wxcolors
import datetime as dt
from icalendar import Calendar, Event
"""
### Ported everything over to Exam Goals.py edit that file instead
"""
class MainMenu(wx.Frame):
    #main panel constructor
    def __init__(self):
        screensize = (400,575)
        super(MainMenu, self).__init__(parent=None, title=AppName,size=screensize)
        self.Bind(wx.EVT_ACTIVATE_APP, self.OnActivate)
        panel = wx.Panel(self)
        self.panel = panel
        wxcolors.updateColourDB() # wx.lib.colourdb.updateColourDB()
        my_colour = wx.NamedColour("grey")
        #extended colour palette from https://github.com/wxWidgets/Phoenix/blob/master/wx/lib/colourdb.py
        self.SetBackgroundColour(my_colour)
        
        # Menu bar stuff
        self.menubar = wx.MenuBar()
        wx.MenuBar.MacSetCommonMenuBar(self.menubar)
        fileMenu = wx.Menu()
        aboutme = fileMenu.Append(wx.ID_ABOUT, '&About '+AppName,'Information about this program')
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutme)
        wx.App.SetMacExitMenuItemId(wx.ID_EXIT)
        quitmenu = fileMenu.Append(wx.ID_EXIT,'Quit '+AppName,'Terminate this program')
        self.Bind(wx.EVT_MENU, self.menuquit, quitmenu)
        self.menubar.Append(fileMenu, '|')
        self.SetMenuBar(self.menubar)
        
        # Main window layout
        menu_sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = menu_sizer
        #self.text_ctrl = wx.TextCtrl(panel)
        #menu_sizer.AddSpacer(0)
        
        #top left design
        self.shoma_icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('./images/Easy_A_logo_mini.png'),style = wx.ALIGN_LEFT)
        self.sizer.Add(self.shoma_icon, 0, wx.RIGHT | wx.LEFT, 20)
        #menu_sizer.AddSpacer(0)
        self.Header_font = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.Welcome = wx.StaticText(self.panel, -1, style = wx.ALIGN_LEFT)
        self.Welcome.SetLabel(AppName+'\nMain Menu\n\n')
        self.Welcome.SetFont(self.Header_font)
        self.sizer.Add(self.Welcome, 0, wx.RIGHT | wx.LEFT, 20)

        self.Header = wx.StaticText(self.panel, -1, style = wx.ALIGN_LEFT)
        self.Header.SetFont(self.Header_font.Underlined())
        self.Header.SetLabel(' Class\t Target Score  \tExam Date\n')
        self.sizer.Add(self.Header, 0, wx.RIGHT | wx.LEFT, 20)

        self.deleteoredit = []
        self.deleteoredithash = []
        self.addedclass = []
        self.savedhashkeys = [] # list of hash keys
        self.scrollingclasses = scrolled.ScrolledPanel(self.panel,size=(400,100))
        self.classlistpos = self.scrollingclasses.GetPosition()
        self.scrollingclasses.SetAutoLayout(1)
        self.scrollingclasses.SetupScrolling()
        self.scrollsizer = wx.BoxSizer(wx.VERTICAL)
        if existingfile:
            try:
                for i,row in enumerate(savedata):
                    self.savedhashkeys.append(row.split(',')[3]) # read in hash key
                    classname = row.split(',')[0]
                    target = row.split(',')[1]
                    date = row.split(',')[2]
                    # Grades = wx.StaticText(panel, -1, style = wx.ALIGN_LEFT)
                    # Grades.SetFont(Header_font)
                    inputs = ' ' + classname + ':\t' + target + '% \t' + date + '\n'
                    self.cb = wx.CheckBox(self.scrollingclasses, label=inputs)#self.cb = wx.CheckBox(panel, label=inputs)
                    self.Bind(wx.EVT_CHECKBOX,self.ifChecked)
                    self.scrollsizer.Add(self.cb, 0, wx.ALL | wx.RIGHT, 0)#menu_sizer.Add(self.cb)
                self.scrollingclasses.SetSizer(self.scrollsizer)
                self.scrollingclasses.Layout()
                self.classlistpos = self.sizer.GetPosition()
                self.sizer.Add(self.scrollingclasses, 1, wx.EXPAND)
            except: pass
        else:
            save_obj({},hashedinfo)
            self.initmsg = 'No classes added yet.\nYou can add your exams\nby clicking Add Class. '
            self.cb = wx.StaticText(self.scrollingclasses)
            self.cb.SetLabel(self.initmsg)
            self.scrollsizer.Add(self.cb, 1, wx.ALL | wx.EXPAND, 25)#menu_sizer.Add(self.cb)
            self.scrollingclasses.SetSizer(self.scrollsizer)
            self.scrollingclasses.Layout()
            self.classlistpos = self.sizer.GetPosition()
            self.sizer.Add(self.scrollingclasses, 1, wx.EXPAND)

        #buttons UI
        start_button = wx.Button(self.panel, label='Delete selected') # button to add class (calls self.start_press function)
        start_button.Bind(wx.EVT_BUTTON, self.deleteselected)
        self.sizer.Add(start_button, 0, wx.UP | wx.LEFT, 20)
        self.sizer.AddSpacer(5)

        start_button = wx.Button(self.panel, label='Edit selected') # button to add class (calls self.start_press function)
        start_button.Bind(wx.EVT_BUTTON, self.editselected)
        self.sizer.Add(start_button, 0, wx.LEFT, 20)
        self.sizer.AddSpacer(5)

        start_button = wx.Button(self.panel, label='Add Class') # button to add class (calls self.start_press function)
        start_button.Bind(wx.EVT_BUTTON, self.start_press)
        self.sizer.Add(start_button, 0, wx.LEFT, 20)
        self.sizer.AddSpacer(5)

        quit_button = wx.Button(self.panel, label='Quit') # button to quit the program
        quit_button.Bind(wx.EVT_BUTTON, self.QuitAll)
        self.sizer.Add(quit_button, 0, wx.DOWN | wx.LEFT, 20)
        self.sizer.AddSpacer(5)

        #menu_sizer.Add((0,0), 1, wx.EXPAND)
        shoma_statement = wx.StaticText(self.panel, -1, style = wx.ALIGN_CENTRE)
        shoma_statement_font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        shoma_statement.SetFont(shoma_statement_font)
        shoma_statement.SetLabel('Version '+version + '\n' + DEVELOPED_BY_SHOMA)
        self.sizer.Add(shoma_statement,0,wx.BOTTOM | wx.CENTER | wx.EXPAND,0)
        self.panel.SetSizer(self.sizer)
        self.Show()

    def menuquit(self,Event):
        self.Destroy()
    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, AppName+"\nVersion: "+version+"\n\nDeveloped by\nShoma Yamanouchi,\nBrian J. Park,\nHannah Cheng\n",
                                "About Me", wx.CENTER | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
    def MacReopenApp(self):
        self.GetTopWindow().Raise()
    def OnActivate(self, event):
        # if this is an activate event, rather than something else, like iconize.
        if event.GetActive():
            self.BringWindowToFront()
        event.Skip()
    def OpenFileMessage(self, filename):
        dlg = wx.MessageDialog(None,
                               "This app was just asked to open:\n%s\n"%filename,
                               "File Dropped",
                               wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
    def MacOpenFile(self, filename):
        """Called for files droped on dock icon, or opened via finders context menu"""
        print(filename)
        print("%s dropped on app"% + filename) #code to load filename goes here.
        self.OpenFileMessage(filename)        
    def MacReopenApp(self):
        """Called when the doc icon is clicked, and ???"""
        self.BringWindowToFront()
    def MacNewFile(self):
        pass
    def MacPrintFile(self, file_path):
        pass

    # Checkbox to select for deletion/edit
    def ifChecked(self, event):
        cb = event.GetEventObject()
        if cb.GetValue():
            classname = cb.GetLabel().split(':')[0][1:] # get the name of class from label 
            classperc = cb.GetLabel().split(':')[1][1:].split('%')[0]
            classdate = cb.GetLabel().split('%')[1][-11:]
            self.deleteoredit.append([classname,classperc,classdate[:-1]])
        if not cb.GetValue():
            classname = cb.GetLabel().split(':')[0][1:] # get the name of class from label 
            classperc = cb.GetLabel().split(':')[1][1:].split('%')[0]
            classdate = cb.GetLabel().split('%')[1][-11:]
            uncheck = [classname,classperc,classdate[:-1]]
            self.deleteoredit.remove(uncheck)

    def deleteselected(self, event):
        if len(self.deleteoredit) > 0:
            #print('call function to delete: ',self.deleteoredit) # need to write function to delete/edit selected class
            WindowSize = (475,140+len(self.deleteoredit)*25)
            DeleteWarning(self.deleteoredit,WindowSize,self)
        else:
            WarningPopup('Nothing selected!','Please select the classes you wish to delete. ',(475,100),self)

    def editselected(self, event):
        if len(self.deleteoredit) > 0:
            oldsave = open('./save/saved.text','r')
            oldlines = oldsave.read().splitlines()
            oldsave.close()
            deletes = []
            for line in oldlines:
                classname = line.split(',')[0]
                target = line.split(',')[1]
                date = line.split(',')[2]
                current = [classname,target,date]
                if current in self.deleteoredit:
                    class2edit = current
                    editkey = line.split(',')[3]
                    EditClassWindowFunc(class2edit,editkey,self)
        else:
            WarningPopup('Nothing selected!','Please select the classes you wish to edit. ',(475,100),self)

    def start_press(self, event): # add class, calls AddClassWindow, which opens a pop up
        #inputpath = self.text_ctrl.GetValue()
        classinfo = AddClassWindow(self)  

    def newclassreload(self): # function called by OTHER frames to reload this page
        #print('(test) Added class is: ',self.addedclass)
        self.deleteoredit = []
        savefile = open('./save/saved.text','r') # read previously inputted data (if available)
        savedata = savefile.read().splitlines()
        existingfile = True
        savefile.close()
        self.scrollingclasses2 = scrolled.ScrolledPanel(self.panel,pos=self.classlistpos,size=(400,100)) # pos=self.classlistpos
        self.scrollingclasses2.SetAutoLayout(1)
        self.scrollingclasses2.SetupScrolling()
        self.scrollsizer2 = wx.BoxSizer(wx.VERTICAL)
        if existingfile:
            for i,row in enumerate(savedata):
                classname = row.split(',')[0]
                target = row.split(',')[1]
                date = row.split(',')[2]
                # Grades = wx.StaticText(panel, -1, style = wx.ALIGN_LEFT)
                # Grades.SetFont(Header_font)
                inputs = ' ' + classname + ':\t' + target + '% \t' + date + '\n'
                self.cb = wx.CheckBox(self.scrollingclasses2, label=inputs)#self.cb = wx.CheckBox(panel, label=inputs)
                self.Bind(wx.EVT_CHECKBOX,self.ifChecked)
                self.scrollsizer2.Add(self.cb, 0, wx.ALL | wx.RIGHT, 0)#menu_sizer.Add(self.cb)
            inputs = ' ' + self.addedclass[0] + ':\t' + self.addedclass[1] + '% \t' + self.addedclass[2] + '\n'
            self.cb = wx.CheckBox(self.scrollingclasses2, label=inputs)#self.cb = wx.CheckBox(panel, label=inputs)
            self.Bind(wx.EVT_CHECKBOX,self.ifChecked)
            self.scrollsizer2.Add(self.cb, 0, wx.ALL | wx.RIGHT, 0)#menu_sizer.Add(self.cb) 
            self.scrollingclasses2.SetSizer(self.scrollsizer2)
            self.scrollingclasses2.Layout()
        else:
            try:
                #
                savefile = open('./save/saved.text','r') # read previously inputted data (if available)
                newsavedata = savefile.read().splitlines()
                for i,row in enumerate(newsavedata):
                    classname = row.split(',')[0]
                    target = row.split(',')[1]
                    date = row.split(',')[2]
                    # Grades = wx.StaticText(panel, -1, style = wx.ALIGN_LEFT)
                    # Grades.SetFont(Header_font)
                    inputs = ' ' + classname + ':\t' + target + '% \t' + date + '\n'
                    self.cb = wx.CheckBox(self.scrollingclasses2, label=inputs)#self.cb = wx.CheckBox(panel, label=inputs)
                    self.Bind(wx.EVT_CHECKBOX,self.ifChecked)
                    self.scrollsizer2.Add(self.cb, 0, wx.ALL | wx.RIGHT, 0)#menu_sizer.Add(self.cb)
                savefile.close()
                #
            except: pass
            inputs = ' ' + self.addedclass[0] + ':\t' + self.addedclass[1] + '% \t' + self.addedclass[2] + '\n'
            self.cb = wx.CheckBox(self.scrollingclasses2, label=inputs)#self.cb = wx.CheckBox(panel, label=inputs)
            self.Bind(wx.EVT_CHECKBOX,self.ifChecked)
            self.scrollsizer2.Add(self.cb, 0, wx.ALL | wx.RIGHT, 0)#menu_sizer.Add(self.cb) 
            self.scrollingclasses2.SetSizer(self.scrollsizer2)
            self.scrollingclasses2.Layout()

        self.scrollingclasses2.Refresh()
        self.scrollingclasses2.Update()
        self.scrollingclasses2.Show()

        self.sizer.Replace(self.scrollingclasses, self.scrollingclasses2)
        self.scrollingclasses.Destroy()
        self.scrollingclasses = self.scrollingclasses2
        #self.sizer.Add(self.scrollingclasses2, 1, wx.EXPAND)

        self.sizer.Layout()
        self.Refresh()
        self.Update()
        self.Show()
        AddCalWindowFunc(self.addedclass,self)
    def editclassreload(self):
        #print('(test) Deleted class is: ',self.deleteoredit)
        self.deleteoredit_old = self.deleteoredit
        savefile = open('./save/saved.text','r') # read previously inputted data (if available)
        savedata = savefile.read().splitlines()
        existingfile = True
        savefile.close()
        self.deleteoredit = []
        ### delete deleted entries from hash
        currentsavedhash = load_obj(hashedinfo) # load saved hash
        for delkey in self.deleteoredithash: # loop through keys to delete
            del currentsavedhash[delkey]
        save_obj(currentsavedhash, hashedinfo) # save updated hashload hash

        self.scrollingclasses2 = scrolled.ScrolledPanel(self.panel,pos=self.classlistpos,size=(400,100)) # pos=self.classlistpos
        self.scrollingclasses2.SetAutoLayout(1)
        self.scrollingclasses2.SetupScrolling()
        self.scrollsizer2 = wx.BoxSizer(wx.VERTICAL)

        for i,row in enumerate(savedata):
            classname = row.split(',')[0]
            target = row.split(',')[1]
            date = row.split(',')[2]
            current = [classname,target,date]
            if i != self.edittedidx:
                # Grades = wx.StaticText(panel, -1, style = wx.ALIGN_LEFT)
                # Grades.SetFont(Header_font)
                inputs = ' ' + classname + ':\t' + target + '% \t' + date + '\n'
                self.cb = wx.CheckBox(self.scrollingclasses2, label=inputs)#self.cb = wx.CheckBox(panel, label=inputs)
                self.Bind(wx.EVT_CHECKBOX,self.ifChecked)
                self.scrollsizer2.Add(self.cb, 0, wx.ALL | wx.RIGHT, 0)#menu_sizer.Add(self.cb)
                self.scrollingclasses2.SetSizer(self.scrollsizer2)
                self.scrollingclasses2.Layout()
            elif i == self.edittedidx:
                inputs = ' ' + self.addedclass[0] + ':\t' + self.addedclass[1] + '% \t' + self.addedclass[2] + '\n'
                self.cb = wx.CheckBox(self.scrollingclasses2, label=inputs)#self.cb = wx.CheckBox(panel, label=inputs)
                self.Bind(wx.EVT_CHECKBOX,self.ifChecked)
                self.scrollsizer2.Add(self.cb, 0, wx.ALL | wx.RIGHT, 0)#menu_sizer.Add(self.cb)
                self.scrollingclasses2.SetSizer(self.scrollsizer2)
                self.scrollingclasses2.Layout()

        self.scrollingclasses2.Refresh()
        self.scrollingclasses2.Update()
        self.scrollingclasses2.Show()

        self.sizer.Replace(self.scrollingclasses, self.scrollingclasses2)
        self.scrollingclasses.Destroy()
        self.scrollingclasses = self.scrollingclasses2
        #self.sizer.Add(self.scrollingclasses2, 1, wx.EXPAND)

        self.sizer.Layout()
        self.Refresh()
        self.Update()
        self.Show()
        AddCalWindowFunc(self.addedclass,self)

    def delclassreload(self): # function called by OTHER frames to reload this page
        #print('(test) Deleted class is: ',self.deleteoredit)
        self.deleteoredit_old = self.deleteoredit
        savefile = open('./save/saved.text','r') # read previously inputted data (if available)
        savedata = savefile.read().splitlines()
        existingfile = True
        savefile.close()
        self.deleteoredit = []

        self.scrollingclasses2 = scrolled.ScrolledPanel(self.panel,pos=self.classlistpos,size=(400,100)) # pos=self.classlistpos
        self.scrollingclasses2.SetAutoLayout(1)
        self.scrollingclasses2.SetupScrolling()
        self.scrollsizer2 = wx.BoxSizer(wx.VERTICAL)

        for i,row in enumerate(savedata):
            classname = row.split(',')[0]
            target = row.split(',')[1]
            date = row.split(',')[2]
            current = [classname,target,date]
            if current not in self.deleteoredit_old:
                # Grades = wx.StaticText(panel, -1, style = wx.ALIGN_LEFT)
                # Grades.SetFont(Header_font)
                inputs = ' ' + classname + ':\t' + target + '% \t' + date + '\n'
                self.cb = wx.CheckBox(self.scrollingclasses2, label=inputs)#self.cb = wx.CheckBox(panel, label=inputs)
                self.Bind(wx.EVT_CHECKBOX,self.ifChecked)
                self.scrollsizer2.Add(self.cb, 0, wx.ALL | wx.RIGHT, 0)#menu_sizer.Add(self.cb)
                self.scrollingclasses2.SetSizer(self.scrollsizer2)
                self.scrollingclasses2.Layout()
            
        self.scrollingclasses2.Refresh()
        self.scrollingclasses2.Update()
        self.scrollingclasses2.Show()

        self.sizer.Replace(self.scrollingclasses, self.scrollingclasses2)
        self.scrollingclasses.Destroy()
        self.scrollingclasses = self.scrollingclasses2
        #self.sizer.Add(self.scrollingclasses2, 1, wx.EXPAND)

        self.sizer.Layout()
        self.Refresh()
        self.Update()
        self.Show()

    def QuitAll(self, event):
        os.system('rm ./save/*.ics')
        wx.Exit()
        

def WarningPopup(Title,Text,WindowSize,parentframe): # Generic warning popup window
    """
    :type Title: String
    :type Text: String
    :type WindowSize: tuple
    :type parentframe: wx.Frame
    :rtype: None
    """
    class WarningWindow(wx.Frame):
        def __init__(self):
            super(WarningWindow, self).__init__(parent=parentframe, title=Title,size=WindowSize)#(450, 110)
            panel = wx.Panel(self)
            errorwindow_size = wx.BoxSizer(wx.VERTICAL)
            Warning = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
            Warning.SetLabel(Text) # e.g., 'Missing value for Midterm'
            errorwindow_size.Add(Warning, 0, wx.ALL | wx.CENTER, 15)
            close_button = wx.Button(panel, label='Close')
            close_button.Bind(wx.EVT_BUTTON, self.closepress)
            errorwindow_size.Add(close_button, 0, wx.ALL | wx.CENTER, 0)
            panel.SetSizer(errorwindow_size)
            self.Show()
            
        def closepress(self, event):
            self.Close()
    WarningWindow()

def AddCalWindowFunc(addedclass,parentframe): # Generic warning popup window
    """
    :type listdel: List
    :type WindowSize: tuple
    :type parentframe: wx.Frame
    :rtype: None
    """
    class AddCalWindow(wx.Frame):
        def __init__(self):
            super(AddCalWindow, self).__init__(parent=parentframe, title='Deleting entries',size=(450,230))
            panel = wx.Panel(self)

            self.addedclass = addedclass
            classname,classperc,classdate = self.addedclass[0],self.addedclass[1],self.addedclass[2]

            errorwindow_size = wx.BoxSizer(wx.VERTICAL)

            ExamAdded = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
            ExamAdded.SetLabel('Exam for '+classname+' is on '+classdate+'.\n\nYour goal is '+classperc+'%.\n\nGood luck!\n') # e.g., 'Missing value for Midterm'
            errorwindow_size.Add(ExamAdded, 0, wx.ALL | wx.CENTER, 15)

            errorwindow_size.AddSpacer(5)

            addcal = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
            addcal.SetLabel('Would you like to add this exam to your calendar?') 
            errorwindow_size.Add(addcal, 0, wx.CENTER, 5)

            errorwindow_size.AddSpacer(15)
            box = wx.BoxSizer(wx.HORIZONTAL)
            abort_button = wx.Button(panel, label='No')
            abort_button.Bind(wx.EVT_BUTTON, self.closepress)
            box.Add(abort_button)
            procede_button = wx.Button(panel, label='Yes')
            procede_button.Bind(wx.EVT_BUTTON, self.procede)
            box.Add(procede_button,wx.RIGHT|wx.BOTTOM)
            errorwindow_size.Add(box,flag=wx.ALIGN_CENTRE|wx.CENTRE)
            panel.SetSizer(errorwindow_size)
            self.Show()
            
        def closepress(self, event):
            self.Close()
        def procede(self, event):
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
            write_ical(self.addedclass)
            self.Close()
    AddCalWindow()


def DeleteWarning(listdel,WindowSize,parentframe): # Generic warning popup window
    """
    :type listdel: List
    :type WindowSize: tuple
    :type parentframe: wx.Frame
    :rtype: None
    """
    class DeleteWarningWindow(wx.Frame):
        def __init__(self):
            super(DeleteWarningWindow, self).__init__(parent=parentframe, title='Deleting entries',size=WindowSize)#(450, 110)
            panel = wx.Panel(self)
            errorwindow_size = wx.BoxSizer(wx.VERTICAL)
            Warning = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
            Warning.SetLabel('The following will be deleted:') # e.g., 'Missing value for Midterm'
            errorwindow_size.Add(Warning, 0, wx.ALL | wx.CENTER, 15)
            for classes in listdel:
                classname,classperc,classdate = classes[0],classes[1],classes[2]
                info = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
                info.SetLabel(classname+', '+classperc+'%, '+classdate+' ') 
                errorwindow_size.Add(info, 0, wx.CENTER, 5)
                errorwindow_size.AddSpacer(10)
            self.listdel = listdel
            errorwindow_size.AddSpacer(20)
            box = wx.BoxSizer(wx.HORIZONTAL)
            abort_button = wx.Button(panel, label='No, abort')
            abort_button.Bind(wx.EVT_BUTTON, self.closepress)
            box.Add(abort_button)
            procede_button = wx.Button(panel, label='Yes, procede')
            procede_button.Bind(wx.EVT_BUTTON, self.procede)
            box.Add(procede_button,wx.RIGHT|wx.BOTTOM)
            errorwindow_size.Add(box,flag=wx.ALIGN_CENTRE|wx.CENTRE)
            panel.SetSizer(errorwindow_size)
            self.Show()
            
        def closepress(self, event):
            self.Close()
        def procede(self, event):
            parentframe.delclassreload()
            oldsave = open('./save/saved.text','r')
            oldlines = oldsave.read().splitlines()
            oldsave.close()
            deletes = []
            self.deleteoredithash = []
            for line in oldlines:
                classname = line.split(',')[0]
                target = line.split(',')[1]
                date = line.split(',')[2]
                current = [classname,target,date]
                if current in self.listdel:
                    deletes.append(line)
                    self.deleteoredithash.append(line.split(',')[3])
            for del_line in deletes:
                #print(oldlines)
                #print('removing: ',del_line)
                oldlines.remove(del_line)
            ### delete deleted entries from hash
            currentsavedhash = load_obj(hashedinfo) # load saved hash
            for delkey in self.deleteoredithash: # loop through keys to delete
                del currentsavedhash[int(delkey)]
            save_obj(currentsavedhash, hashedinfo) # save updated hashload hash
            newsave = open('./save/saved.text', 'w+')
            for line in oldlines:
                #print('writing: ',line)
                newsave.write(line+'\n')
            newsave.close()
            self.Close()
    DeleteWarningWindow()

def EditClassWindowFunc(class2edit,editkey,parentframe):
    """
    :type parentframe: wx.Frame
    """
    parent = parentframe
    class EditClassWindow(wx.Frame):
        def __init__(self):
            super(EditClassWindow, self).__init__(parent=parentframe, title='Adding a class',size=(375, 700))#(400, 400)
            panel = wx.Panel(self)
            window_size = wx.BoxSizer(wx.VERTICAL)
            self.classinfo = dict()
            self.editkey = editkey
            currentsavedhash = load_obj(hashedinfo) # load saved hash
            self.currentsavedhashFULL = currentsavedhash
            currentsavedhash = currentsavedhash[int(editkey)]
            Name = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
            Name.SetLabel('Class Name')
            window_size.Add(Name, 0, wx.UP | wx.CENTER, 15)
            self.text_ctrl = wx.TextCtrl(panel)

            self.text_ctrl.SetValue(currentsavedhash['classname'].upper()) # set previous value as default
            window_size.Add(self.text_ctrl, 0, wx.UP | wx.CENTER, 15)
            window_size.AddSpacer(10)

            self.scrollingclasses = scrolled.ScrolledPanel(panel,size=(300,575))
            self.scrollingclasses.SetAutoLayout(1)
            self.scrollingclasses.SetupScrolling()
            self.scrollsizer = wx.BoxSizer(wx.VERTICAL)

            self.scrollsizer.AddSpacer(5)
            Quiz = wx.StaticText(self.scrollingclasses, -1, style = wx.ALIGN_CENTRE)
            Quiz.SetLabel('Quiz weight (0-100%) and your score (in %) ')
            self.scrollsizer.Add(Quiz, 0, wx.UP | wx.CENTER, 15)
            self.text_ctrl1 = wx.TextCtrl(self.scrollingclasses)
            self.text_ctrl1.SetValue(currentsavedhash['quiz'][0]) # set previous value as default
            self.text_ctrl11 = wx.TextCtrl(self.scrollingclasses)
            self.text_ctrl11.SetValue(currentsavedhash['quiz'][1]) # set previous value as default
            self.scrollsizer.Add(self.text_ctrl1, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.Add(self.text_ctrl11, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.AddSpacer(10)

            Assignment = wx.StaticText(self.scrollingclasses, -1, style = wx.ALIGN_CENTRE)
            Assignment.SetLabel('Assignment weight (0-100%) and your score (in %) ')
            self.scrollsizer.Add(Assignment, 0, wx.UP | wx.CENTER, 15)
            self.text_ctrl2 = wx.TextCtrl(self.scrollingclasses)
            self.text_ctrl2.SetValue(currentsavedhash['Assignment'][0]) # set previous value as default
            self.text_ctrl21 = wx.TextCtrl(self.scrollingclasses)
            self.text_ctrl21.SetValue(currentsavedhash['Assignment'][1]) # set previous value as default
            self.scrollsizer.Add(self.text_ctrl2, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.Add(self.text_ctrl21, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.AddSpacer(5)

            Midterm = wx.StaticText(self.scrollingclasses, -1, style = wx.ALIGN_CENTRE)
            Midterm.SetLabel('Midterm weight (0-100%) and your score (in %) ')
            self.scrollsizer.Add(Midterm, 0, wx.UP | wx.CENTER, 15)
            self.text_ctrl3 = wx.TextCtrl(self.scrollingclasses)
            self.text_ctrl3.SetValue(currentsavedhash['Midterm'][0]) # set previous value as default
            self.text_ctrl31 = wx.TextCtrl(self.scrollingclasses)
            self.text_ctrl31.SetValue(currentsavedhash['Midterm'][1]) # set previous value as default
            self.scrollsizer.Add(self.text_ctrl3, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.Add(self.text_ctrl31, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.AddSpacer(5)

            Target = wx.StaticText(self.scrollingclasses, -1, style=wx.ALIGN_CENTRE)
            Target.SetLabel('Final exam weight (0-100%) ')
            self.scrollsizer.Add(Target, 0, wx.UP | wx.CENTER, 15)
            self.text_ctrl4 = wx.TextCtrl(self.scrollingclasses)
            self.text_ctrl4.SetValue(currentsavedhash['Target'][0]) # set previous value as default
            Target2 = wx.StaticText(self.scrollingclasses, -1, style=wx.ALIGN_CENTRE)
            Target2.SetLabel('Your target overall course grade (in %) ')
            self.text_ctrl41 = wx.TextCtrl(self.scrollingclasses)
            self.text_ctrl41.SetValue(currentsavedhash['Target'][1]) # set previous value as default
            self.scrollsizer.Add(self.text_ctrl4, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.AddSpacer(5)
            self.scrollsizer.Add(Target2, 0, wx.UP | wx.CENTER, 15)
            self.scrollsizer.Add(self.text_ctrl41, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.AddSpacer(10)

            # Add Misc Grades 1, 2 here
            leaveempty = wx.StaticText(self.scrollingclasses, -1, style=wx.ALIGN_CENTRE)
            leaveempty.SetLabel('If you have other marks, enter them here\nPlease leave unneeded boxes blank ')
            self.scrollsizer.Add(leaveempty, 0, wx.UP | wx.CENTER, 15)
            self.scrollsizer.AddSpacer(8)

            Misc1 = wx.StaticText(self.scrollingclasses, -1, style=wx.ALIGN_CENTRE)
            Misc1.SetLabel('Misc. grades (1), weight (0-100%) and your score (in %) ')
            self.scrollsizer.Add(Misc1, 0, wx.UP | wx.CENTER, 15)
            self.text_misc11 = wx.TextCtrl(self.scrollingclasses)
            self.text_misc11.SetValue(currentsavedhash['Misc_1'][0]) # set previous value as default
            self.text_misc12 = wx.TextCtrl(self.scrollingclasses)
            self.text_misc12.SetValue(currentsavedhash['Misc_1'][1]) # set previous value as default
            self.scrollsizer.Add(self.text_misc11, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.Add(self.text_misc12, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.AddSpacer(5)

            Misc2 = wx.StaticText(self.scrollingclasses, -1, style=wx.ALIGN_CENTRE)
            Misc2.SetLabel('Misc. grades (2), weight (0-100%) and your score (in %) ')
            self.scrollsizer.Add(Misc2, 0, wx.UP | wx.CENTER, 15)
            self.text_misc21 = wx.TextCtrl(self.scrollingclasses)
            self.text_misc21.SetValue(currentsavedhash['Misc_2'][0]) # set previous value as default
            self.text_misc22 = wx.TextCtrl(self.scrollingclasses)
            self.text_misc22.SetValue(currentsavedhash['Misc_2'][1]) # set previous value as default
            self.scrollsizer.Add(self.text_misc21, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.Add(self.text_misc22, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.AddSpacer(5)
            #

            self.scrollingclasses.SetSizer(self.scrollsizer)
            self.scrollingclasses.Layout()
            self.classlistpos = window_size.GetPosition()
            window_size.Add(self.scrollingclasses, 1, wx.EXPAND)


            currentexamdate = currentsavedhash['Date']
            currentexamdate = wx.DateTime.FromDMY(int(currentexamdate.split('/')[2]),int(currentexamdate.split('/')[1])-1,int(currentexamdate.split('/')[0]))

            ExamDate = wx.StaticText(panel, -1, style=wx.ALIGN_CENTRE)
            ExamDate.SetLabel('Final exam date')
            window_size.Add(ExamDate, 0, wx.UP | wx.CENTER, 15)
            self.text_ctrl5 = wx.adv.DatePickerCtrl(panel,style=wx.adv.DP_DEFAULT,dt=currentexamdate)#wx.adv.DatePickerCtrl
            window_size.Add(self.text_ctrl5, 0, wx.UP | wx.CENTER, 15)

            window_size.AddSpacer(30)
            add_button = wx.Button(panel, label='Add')
            add_button.Bind(wx.EVT_BUTTON, self.addpress)
            window_size.Add(add_button, 0, wx.UP | wx.CENTER, 0)
            panel.SetSizer(window_size)
            window_size.AddSpacer(5)

            close_button = wx.Button(panel, label='Close')
            close_button.Bind(wx.EVT_BUTTON, self.closepress)
            window_size.Add(close_button, 0, wx.UP | wx.CENTER, 0)
            window_size.AddSpacer(25)
            panel.SetSizer(window_size)
            self.Show()
            
        def closepress(self, event):
            self.Close()
            return False

        def addpress(self, event):
            classname = self.text_ctrl.GetValue()
            self.classinfo['classname'] = classname 

            quizweight = self.text_ctrl1.GetValue()
            quizscore = self.text_ctrl11.GetValue()
            self.classinfo['quiz'] = (quizweight,quizscore)

            Assignmentweight = self.text_ctrl2.GetValue()
            Assignmentscore = self.text_ctrl21.GetValue()
            self.classinfo['Assignment'] = (Assignmentweight,Assignmentscore)

            Midtermweight = self.text_ctrl3.GetValue()
            Midtermscore = self.text_ctrl31.GetValue()
            self.classinfo['Midterm'] = (Midtermweight,Midtermscore)

         

            Finalweight = self.text_ctrl4.GetValue()
            Targetscore = self.text_ctrl41.GetValue()
            self.classinfo['Target'] = (Finalweight, Targetscore)

            date = self.text_ctrl5.GetValue()
            self.classinfo['Date'] = date.Format('%Y/%m/%d')
            #parent.addedclass = self.classinfo
            #print(self.classinfo)

            Misc1weight = self.text_misc11.GetValue()
            Misc1score = self.text_misc12.GetValue()
            self.classinfo['Misc_1'] = (Misc1weight, Misc1score)

            Misc2weight = self.text_misc21.GetValue()
            Misc2score = self.text_misc22.GetValue()
            self.classinfo['Misc_2'] = (Misc2weight, Misc2score)

            for i,j in self.classinfo.items():
                if j[0] == '' or j[1] == '':
                    self.classinfo[i] = ('0', '0')

            #replacing empty fields with zeroes

            turn = 0
            #initiate loop
            for i, j in self.classinfo.items():
                if isinstance(j, str) != True:
                    if i != 'Target' and i != 'classname':
                        if turn == 0:
                            mark = float(j[1])*(0.01*float(j[0]))
                        if turn != 0:
                            mark1 = float(j[1])*(0.01*float(j[0]))
                            mark = mark1 + mark
                            #summing up marks over loop
                        turn +=1
                    if i == 'Target':
                        pass
                """
                if isinstance(j, str) == True:
                    if i == 'classname':
                        my_course = j
                    if i == 'Date':
                    	exam_date = j
                """

            for i, j in self.classinfo.items():
                if isinstance(j, str) != True:
                    if i == 'Target':
                        target_mark = float(j[1]) - mark
                        #percentage of mark required to hit threshold
                        mark_reqd = (target_mark / float(j[0]))*100
                        #percentage out of 100 required on exam
               
            my_course = self.classinfo['classname']
            exam_date = self.classinfo['Date']
            my_course = my_course.upper() # make classname uppercase
            parent.addedclass = [my_course,str(int(mark_reqd)),exam_date]


            del self.currentsavedhashFULL[int(self.editkey)] # delete old hashed data
            self.currentsavedhashFULL[int(self.editkey)] = self.classinfo # add data hash to hash
            save_obj(self.currentsavedhashFULL, hashedinfo) # save updated hash

            oldsave = open('./save/saved.text','r')
            oldlines = oldsave.read().splitlines()
            oldsave.close()
            deletes = []
            for i, line in enumerate(oldlines):
                classname = line.split(',')[0]
                target = line.split(',')[1]
                date = line.split(',')[2]
                current = [classname,target,date]
                if current == class2edit:
                    parent.edittedidx = i
                    oldlines.remove(line)
                    newline = my_course + ',' + str(int(mark_reqd)) + ',' + exam_date + ',' + str(self.editkey)
                    oldlines.insert(i,newline)
                else: pass
            parent.editclassreload()
            newsave = open('./save/saved.text', 'w+')
            for line in oldlines:
                newsave.write(line+'\n')
            newsave.close()
            
            #print(my_course,mark_reqd,exam_date)
            #print(my_course,str(int(mark_reqd)),exam_date)
            self.Close()
            #return mark_reqd
            #return my_course
            #return exam_date
    EditClassWindow()

def AddClassWindow(parentframe):
    """
    :type parentframe: wx.Frame
    """
    parent = parentframe
    class AddClassWindow(wx.Frame):
        def __init__(self):
            super(AddClassWindow, self).__init__(parent=parentframe, title='Adding a class',size=(375, 700))#(400, 400)
            panel = wx.Panel(self)
            window_size = wx.BoxSizer(wx.VERTICAL)
            self.classinfo = dict()

            Name = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
            Name.SetLabel('Class Name (e.g., MATH101)')
            window_size.Add(Name, 0, wx.UP | wx.CENTER, 15)
            self.text_ctrl = wx.TextCtrl(panel)
            window_size.Add(self.text_ctrl, 0, wx.UP | wx.CENTER, 15)
            window_size.AddSpacer(10)

            self.scrollingclasses = scrolled.ScrolledPanel(panel,size=(300,575))
            self.scrollingclasses.SetAutoLayout(1)
            self.scrollingclasses.SetupScrolling()
            self.scrollsizer = wx.BoxSizer(wx.VERTICAL)
            #self.scrollsizer.Add(

            #Quiz = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
            #Quiz.SetLabel('Quiz weight (0-100%) and your score')
            #window_size.Add(Quiz, 0, wx.UP | wx.CENTER, 15)
            #self.text_ctrl1 = wx.TextCtrl(panel)
            #self.text_ctrl11 = wx.TextCtrl(panel)
            #window_size.Add(self.text_ctrl1, 0, wx.UP | wx.CENTER, 15)
            #window_size.Add(self.text_ctrl11, 0, wx.UP | wx.CENTER, 15)
            self.scrollsizer.AddSpacer(5)
            Quiz = wx.StaticText(self.scrollingclasses, -1, style = wx.ALIGN_CENTRE)
            Quiz.SetLabel('Quiz weight (0-100%) and your score (in %) ')
            self.scrollsizer.Add(Quiz, 0, wx.UP | wx.CENTER, 15)
            self.text_ctrl1 = wx.TextCtrl(self.scrollingclasses)
            self.text_ctrl11 = wx.TextCtrl(self.scrollingclasses)
            self.scrollsizer.Add(self.text_ctrl1, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.Add(self.text_ctrl11, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.AddSpacer(10)

            #Assignment = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
            #Assignment.SetLabel('Assignment weight (0-100%) and your score')
            #window_size.Add(Assignment, 0, wx.UP | wx.CENTER, 15)
            #self.text_ctrl2 = wx.TextCtrl(panel)
            #self.text_ctrl21 = wx.TextCtrl(panel)
            #window_size.Add(self.text_ctrl2, 0, wx.UP | wx.CENTER, 15)
            #window_size.Add(self.text_ctrl21, 0, wx.UP | wx.CENTER, 15)
            Assignment = wx.StaticText(self.scrollingclasses, -1, style = wx.ALIGN_CENTRE)
            Assignment.SetLabel('Assignment weight (0-100%) and your score (in %) ')
            self.scrollsizer.Add(Assignment, 0, wx.UP | wx.CENTER, 15)
            self.text_ctrl2 = wx.TextCtrl(self.scrollingclasses)
            self.text_ctrl21 = wx.TextCtrl(self.scrollingclasses)
            self.scrollsizer.Add(self.text_ctrl2, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.Add(self.text_ctrl21, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.AddSpacer(5)
            
            #Midterm = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
            #Midterm.SetLabel('Midterm weight (0-100%) and your score')
            #window_size.Add(Midterm, 0, wx.UP | wx.CENTER, 15)
            #self.text_ctrl3 = wx.TextCtrl(panel)
            #self.text_ctrl31 = wx.TextCtrl(panel)
            #window_size.Add(self.text_ctrl3, 0, wx.UP | wx.CENTER, 15)
            #window_size.Add(self.text_ctrl31, 0, wx.UP | wx.CENTER, 15)
            Midterm = wx.StaticText(self.scrollingclasses, -1, style = wx.ALIGN_CENTRE)
            Midterm.SetLabel('Midterm weight (0-100%) and your score (in %) ')
            self.scrollsizer.Add(Midterm, 0, wx.UP | wx.CENTER, 15)
            self.text_ctrl3 = wx.TextCtrl(self.scrollingclasses)
            self.text_ctrl31 = wx.TextCtrl(self.scrollingclasses)
            self.scrollsizer.Add(self.text_ctrl3, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.Add(self.text_ctrl31, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.AddSpacer(5)

            #Target = wx.StaticText(panel, -1, style=wx.ALIGN_CENTRE)
            #arget.SetLabel('Final exam weight (0-100%) and your target course %')
            #window_size.Add(Target, 0, wx.UP | wx.CENTER, 15)
            #self.text_ctrl4 = wx.TextCtrl(panel)
            #self.text_ctrl41 = wx.TextCtrl(panel)
            #window_size.Add(self.text_ctrl4, 0, wx.UP | wx.CENTER, 15)
            #window_size.Add(self.text_ctrl41, 0, wx.UP | wx.CENTER, 15)
            Target = wx.StaticText(self.scrollingclasses, -1, style=wx.ALIGN_CENTRE)
            Target.SetLabel('Final exam weight (0-100%) ')
            self.scrollsizer.Add(Target, 0, wx.UP | wx.CENTER, 15)
            self.text_ctrl4 = wx.TextCtrl(self.scrollingclasses)
            Target2 = wx.StaticText(self.scrollingclasses, -1, style=wx.ALIGN_CENTRE)
            Target2.SetLabel('Your target overall course grade (in %) ')
            self.text_ctrl41 = wx.TextCtrl(self.scrollingclasses)
            self.scrollsizer.Add(self.text_ctrl4, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.AddSpacer(5)
            self.scrollsizer.Add(Target2, 0, wx.UP | wx.CENTER, 15)
            self.scrollsizer.Add(self.text_ctrl41, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.AddSpacer(10)

            # Add Misc Grades 1, 2 here
            leaveempty = wx.StaticText(self.scrollingclasses, -1, style=wx.ALIGN_CENTRE)
            leaveempty.SetLabel('If you have other marks, enter them here\nPlease leave unneeded boxes blank ')
            self.scrollsizer.Add(leaveempty, 0, wx.UP | wx.CENTER, 15)
            self.scrollsizer.AddSpacer(8)

            Misc1 = wx.StaticText(self.scrollingclasses, -1, style=wx.ALIGN_CENTRE)
            Misc1.SetLabel('Misc. grades (1), weight (0-100%) and your score (in %) ')
            self.scrollsizer.Add(Misc1, 0, wx.UP | wx.CENTER, 15)
            self.text_misc11 = wx.TextCtrl(self.scrollingclasses)
            self.text_misc12 = wx.TextCtrl(self.scrollingclasses)
            self.scrollsizer.Add(self.text_misc11, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.Add(self.text_misc12, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.AddSpacer(5)

            Misc2 = wx.StaticText(self.scrollingclasses, -1, style=wx.ALIGN_CENTRE)
            Misc2.SetLabel('Misc. grades (2), weight (0-100%) and your score (in %) ')
            self.scrollsizer.Add(Misc2, 0, wx.UP | wx.CENTER, 15)
            self.text_misc21 = wx.TextCtrl(self.scrollingclasses)
            self.text_misc22 = wx.TextCtrl(self.scrollingclasses)
            self.scrollsizer.Add(self.text_misc21, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.Add(self.text_misc22, 0, wx.UP | wx.CENTER, 10)
            self.scrollsizer.AddSpacer(5)
            #

            self.scrollingclasses.SetSizer(self.scrollsizer)
            self.scrollingclasses.Layout()
            self.classlistpos = window_size.GetPosition()
            window_size.Add(self.scrollingclasses, 1, wx.EXPAND)


            ExamDate = wx.StaticText(panel, -1, style=wx.ALIGN_CENTRE)
            ExamDate.SetLabel('Final exam date')
            window_size.Add(ExamDate, 0, wx.UP | wx.CENTER, 15)
            self.text_ctrl5 = wx.adv.DatePickerCtrl(panel,style=wx.adv.DP_DEFAULT,dt=wx.DateTime.Now())#wx.adv.DatePickerCtrl
            window_size.Add(self.text_ctrl5, 0, wx.UP | wx.CENTER, 15)

            window_size.AddSpacer(30)
            add_button = wx.Button(panel, label='Add')
            add_button.Bind(wx.EVT_BUTTON, self.addpress)
            window_size.Add(add_button, 0, wx.UP | wx.CENTER, 0)
            panel.SetSizer(window_size)
            window_size.AddSpacer(5)

            close_button = wx.Button(panel, label='Close')
            close_button.Bind(wx.EVT_BUTTON, self.closepress)
            window_size.Add(close_button, 0, wx.UP | wx.CENTER, 0)
            window_size.AddSpacer(25)
            panel.SetSizer(window_size)
            self.Show()
            
        def closepress(self, event):
            self.Close()
            return False

        def addpress(self, event):
            classname = self.text_ctrl.GetValue()
            self.classinfo['classname'] = classname 

            quizweight = self.text_ctrl1.GetValue()
            quizscore = self.text_ctrl11.GetValue()
            self.classinfo['quiz'] = (quizweight,quizscore)

            Assignmentweight = self.text_ctrl2.GetValue()
            Assignmentscore = self.text_ctrl21.GetValue()
            self.classinfo['Assignment'] = (Assignmentweight,Assignmentscore)

            Midtermweight = self.text_ctrl3.GetValue()
            Midtermscore = self.text_ctrl31.GetValue()
            self.classinfo['Midterm'] = (Midtermweight,Midtermscore)

         

            Finalweight = self.text_ctrl4.GetValue()
            Targetscore = self.text_ctrl41.GetValue()
            self.classinfo['Target'] = (Finalweight, Targetscore)

            date = self.text_ctrl5.GetValue()
            self.classinfo['Date'] = date.Format('%Y/%m/%d')
            #parent.addedclass = self.classinfo
            #print(self.classinfo)

            Misc1weight = self.text_misc11.GetValue()
            Misc1score = self.text_misc12.GetValue()
            self.classinfo['Misc_1'] = (Misc1weight, Misc1score)

            Misc2weight = self.text_misc21.GetValue()
            Misc2score = self.text_misc22.GetValue()
            self.classinfo['Misc_2'] = (Misc2weight, Misc2score)

            for i,j in self.classinfo.items():
                if j[0] == '' or j[1] == '':
                    self.classinfo[i] = ('0', '0')

            #replacing empty fields with zeroes



            turn = 0
            #initiate loop
            for i, j in self.classinfo.items():
                if isinstance(j, str) != True:
                    if i != 'Target' and i != 'classname':
                        if turn == 0:
                            mark = float(j[1])*(0.01*float(j[0]))
                        if turn != 0:
                            mark1 = float(j[1])*(0.01*float(j[0]))
                            mark = mark1 + mark
                            #summing up marks over loop
                        turn +=1
                    if i == 'Target':
                        pass
                """
                if isinstance(j, str) == True:
                    if i == 'classname':
                        my_course = j
                    if i == 'Date':
                    	exam_date = j
                """

            for i, j in self.classinfo.items():
                if isinstance(j, str) != True:
                    if i == 'Target':
                        target_mark = float(j[1]) - mark
                        #percentage of mark required to hit threshold
                        mark_reqd = (target_mark / float(j[0]))*100
                        #percentage out of 100 required on exam
               
            my_course = self.classinfo['classname']
            exam_date = self.classinfo['Date']
            my_course = my_course.upper() # make classname uppercase
            parent.addedclass = [my_course,str(int(mark_reqd)),exam_date]
            parent.classinfo = self.classinfo
            parent.newclassreload()

            # create new key, add to existing list of keys, and append the saved hash
            newkey4newclass = make_hash_key(parent.savedhashkeys) # new key
            parent.savedhashkeys.append(newkey4newclass) # append to list of keys
            currentsavedhash = load_obj(hashedinfo) # load saved hash
            currentsavedhash[newkey4newclass] = self.classinfo # add data hash to hash
            save_obj(currentsavedhash, hashedinfo) # save updated hash

            ### Currently commented out so that the saved txt ###
            ### file does not become filled up during testing ###

            if os.path.isfile('./save/saved.text'): # open existing save file
                saved = open('./save/saved.text','a+')
            else:
                saved = open('./save/saved.text','w+') # open new file
            #saved.write(my_course + ',' + '{:.1f}'.format(mark_reqd) + ',' + exam_date + '\n') # if writing as float (1 decimal prec)
            saved.write(my_course + ',' + str(int(mark_reqd)) + ',' + exam_date + ',' + str(newkey4newclass) + '\n') # if writing as float (1 decimal prec)
            saved.close()
            
            #print(my_course,mark_reqd,exam_date)
            #print(my_course,str(int(mark_reqd)),exam_date)
            self.Close()
            #return mark_reqd
            #return my_course
            #return exam_date
    AddClassWindow()

#########################################################
""" For pickling data"""
def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
#########################################################
def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
#########################################################
def make_hash_key(existing):
    # creates a new, unique key
    newkey = random.choice([x for x in range(10000,99999) if x not in existing])
    return newkey
#########################################################

if __name__ == '__main__':
    app = wx.App()
    hashedinfo = './save/pickedhashtable'
    if os.path.isfile('./save/saved.text'):
        savefile = open('./save/saved.text','r') # read previously inputted data (if available)
        savedata = savefile.read().splitlines()
        savefile.close()
        existingfile = True
        if len(savedata) == 0:
            existingfile = False
        else: existingfile = True
    else:
        savefile = open('./save/saved.text','w+') # read previously inputted data (if available)
        savefile.close()
        existingfile = False
    os.system('rm ./save/*.ics')
    wx.AppConsole.SetAppName(app,AppName)
    wx.AppConsole.SetAppDisplayName(app,AppName)
    frame = MainMenu()
    app.MainLoop()
