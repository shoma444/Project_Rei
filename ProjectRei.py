# Written and developed by Shoma Yamanouchi, Brian J. Park, and Hannah Cheng
# Contact: syamanou@physics.utoronto.ca OR brianjmpark@gmail.com
# Website: https://sites.google.com/view/shoma-yamanouchi OR https://brianjmpark.github.io/ OR Hannah's websites
# version 1.0
# Developed in Python 2.7.18
version = '1.0'
DEVELOPED_BY_SHOMA = 'Easy A 2021 (c) was developed by:\nShoma Yamanouchi,\nBrian J. Park,\nand Hannah Cheng'

import os, sys, wx, csv, wx.adv
import wx.lib.scrolledpanel as scrolled

class MainMenu(wx.Frame):
    #main panel constructor
    def __init__(self):
        screensize = (400,575)
        super(MainMenu, self).__init__(parent=None, title='Easy A',size=screensize)
        self.Bind(wx.EVT_ACTIVATE_APP, self.OnActivate)
        panel = wx.Panel(self)
        self.panel = panel

        # Menu bar stuff
        self.menubar = wx.MenuBar()
        wx.MenuBar.MacSetCommonMenuBar(self.menubar)
        fileMenu = wx.Menu()
        aboutme = fileMenu.Append(wx.ID_ABOUT, '&About Easy A','Information about this program')
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutme)
        wx.App.SetMacExitMenuItemId(wx.ID_EXIT)
        quitmenu = fileMenu.Append(wx.ID_EXIT,'Quit Easy A','Terminate this program')
        self.Bind(wx.EVT_MENU, self.menuquit, quitmenu)
        self.menubar.Append(fileMenu, '|')
        self.SetMenuBar(self.menubar)
        
        # Main window layout
        menu_sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = menu_sizer
        #self.text_ctrl = wx.TextCtrl(panel)
        #menu_sizer.AddSpacer(0)
        
        #top left design
        shoma_icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('./images/Easy_A_logo_mini.png'),style = wx.ALIGN_LEFT)
        self.sizer.Add(shoma_icon, 0, wx.RIGHT | wx.LEFT, 20)
        #menu_sizer.AddSpacer(0)
        Header_font = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        Welcome = wx.StaticText(panel, -1, style = wx.ALIGN_LEFT)
        Welcome.SetLabel('Easy A\nMain Menu\n\n')
        Welcome.SetFont(Header_font)
        self.sizer.Add(Welcome, 0, wx.RIGHT | wx.LEFT, 20)

        Header = wx.StaticText(panel, -1, style = wx.ALIGN_LEFT)
        Header.SetFont(Header_font.Underlined())
        Header.SetLabel(' Class\t Target Score  \tExam Date\n')
        self.sizer.Add(Header, 0, wx.RIGHT | wx.LEFT, 20)

        self.deleteoredit = []
        self.addedclass = []
        self.scrollingclasses = scrolled.ScrolledPanel(self.panel,size=(400,100))
        self.classlistpos = self.scrollingclasses.GetPosition()
        self.scrollingclasses.SetAutoLayout(1)
        self.scrollingclasses.SetupScrolling()
        self.scrollsizer = wx.BoxSizer(wx.VERTICAL)
        if existingfile:
            try:
                for i,row in enumerate(savedata):
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
            self.cb = wx.StaticText('No classes added yet.')
            self.scrollsizer.Add(self.cb, 0, wx.ALL | wx.RIGHT, 0)#menu_sizer.Add(self.cb)
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
        dlg = wx.MessageDialog(self, "Easy A\nVersion: "+version+"\nBy Shoma Yamanouchi,\nBrian J. Park,\nHannah Cheng\n",
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
            self.deleteoredit.append(classname)

    def deleteselected(self, event):
        if len(self.deleteoredit) > 0:
            print('call function to delete: ',self.deleteoredit) # need to write function to delete/edit selected class
            wx.Yield()
        else:
            WarningPopup('Nothing selected!','Please select the classes you wish to delete.',(450,100),self)

    def editselected(self, event):
        if len(self.deleteoredit) > 0:
            print('call function to edit: ',self.deleteoredit) # need to write function to delete/edit selected class
            wx.Yield()
        else:
            WarningPopup('Nothing selected!','Please select the classes you wish to edit.',(450,100),self)

    def start_press(self, event): # add class, calls AddClassWindow, which opens a pop up
        #inputpath = self.text_ctrl.GetValue()
        classinfo = AddClassWindow(self)  

    def newclassreload(self): # function called by OTHER frames to reload this page
        print('(test) Added class is: ',self.addedclass)
        """
        self.panel = wx.Panel(self)
        self.sizer  = wx.BoxSizer(wx.VERTICAL)

        #top left design
        shoma_icon = wx.StaticBitmap(self.panel, bitmap=wx.Bitmap('./images/Easy_A_logo_mini.png'),style = wx.ALIGN_LEFT)
        self.sizer.Add(shoma_icon, 0, wx.RIGHT | wx.LEFT, 20)
        #menu_sizer.AddSpacer(0)
        Header_font = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        Welcome = wx.StaticText(self.panel, -1, style = wx.ALIGN_LEFT)
        Welcome.SetLabel('Easy A\nMain Menu\n\n')
        Welcome.SetFont(Header_font)
        self.sizer.Add(Welcome, 0, wx.RIGHT | wx.LEFT, 20)
        """
        self.deleteoredit = []
        self.scrollingclasses.Destroy()
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
            inputs = ' ' + self.addedclass[0] + ':\t' + self.addedclass[1] + '% \t' + self.addedclass[2] + '\n'
            self.cb = wx.CheckBox(self.scrollingclasses2, label=inputs)#self.cb = wx.CheckBox(panel, label=inputs)
            self.Bind(wx.EVT_CHECKBOX,self.ifChecked)
            self.scrollsizer2.Add(self.cb, 0, wx.ALL | wx.RIGHT, 0)#menu_sizer.Add(self.cb) 
            self.scrollingclasses2.SetSizer(self.scrollsizer2)
            self.scrollingclasses2.Layout()
        self.scrollingclasses2.Refresh()
        self.scrollingclasses2.Update()
        self.scrollingclasses2.Show()

        #self.sizer.Replace(self.scrollingclasses, self.scrollingclasses2)
        self.sizer.Add(self.scrollingclasses2, 1, wx.EXPAND)

        self.Refresh()
        self.Update()
        self.Layout()
        self.Show()

    def QuitAll(self, event):
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

def AddClassWindow(parentframe):
    """
    :type parentframe: wx.Frame
    :rtype: dict classinfo (False if closed)
    """
    parent = parentframe
    class AddClassWindow(wx.Frame):
        def __init__(self):
            super(AddClassWindow, self).__init__(parent=parentframe, title='Adding a class',size=(350, 800))#(400, 400)
            panel = wx.Panel(self)
            window_size = wx.BoxSizer(wx.VERTICAL)
            self.classinfo = dict()

            Name = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
            Name.SetLabel('Class Name (e.g., MATH101)')
            window_size.Add(Name, 0, wx.UP | wx.CENTER, 15)
            self.text_ctrl = wx.TextCtrl(panel)
            window_size.Add(self.text_ctrl, 0, wx.UP | wx.CENTER, 15)

            Quiz = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
            Quiz.SetLabel('Quiz weight (0-100%) and your score')
            window_size.Add(Quiz, 0, wx.UP | wx.CENTER, 15)
            self.text_ctrl1 = wx.TextCtrl(panel)
            self.text_ctrl11 = wx.TextCtrl(panel)
            window_size.Add(self.text_ctrl1, 0, wx.UP | wx.CENTER, 15)
            window_size.Add(self.text_ctrl11, 0, wx.UP | wx.CENTER, 15)

            Assignment = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
            Assignment.SetLabel('Assignment weight (0-100%) and your score')
            window_size.Add(Assignment, 0, wx.UP | wx.CENTER, 15)
            self.text_ctrl2 = wx.TextCtrl(panel)
            self.text_ctrl21 = wx.TextCtrl(panel)
            window_size.Add(self.text_ctrl2, 0, wx.UP | wx.CENTER, 15)
            window_size.Add(self.text_ctrl21, 0, wx.UP | wx.CENTER, 15)

            Midterm = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
            Midterm.SetLabel('Midterm weight (0-100%) and your score')
            window_size.Add(Midterm, 0, wx.UP | wx.CENTER, 15)
            self.text_ctrl3 = wx.TextCtrl(panel)
            self.text_ctrl31 = wx.TextCtrl(panel)
            window_size.Add(self.text_ctrl3, 0, wx.UP | wx.CENTER, 15)
            window_size.Add(self.text_ctrl31, 0, wx.UP | wx.CENTER, 15)

            Target = wx.StaticText(panel, -1, style=wx.ALIGN_CENTRE)
            Target.SetLabel('Final exam weight (0-100%) and your target course %')
            window_size.Add(Target, 0, wx.UP | wx.CENTER, 15)
            self.text_ctrl4 = wx.TextCtrl(panel)
            self.text_ctrl41 = wx.TextCtrl(panel)
            window_size.Add(self.text_ctrl4, 0, wx.UP | wx.CENTER, 15)
            window_size.Add(self.text_ctrl41, 0, wx.UP | wx.CENTER, 15)

            ExamDate = wx.StaticText(panel, -1, style=wx.ALIGN_CENTRE)
            ExamDate.SetLabel('Final exam date')
            window_size.Add(ExamDate, 0, wx.UP | wx.CENTER, 15)
            self.text_ctrl5 = wx.adv.DatePickerCtrl(panel,style=wx.adv.DP_DEFAULT,dt=wx.DateTime.Now())
            window_size.Add(self.text_ctrl5, 0, wx.UP | wx.CENTER, 15)

            window_size.AddSpacer(60)
            add_button = wx.Button(panel, label='Add')
            add_button.Bind(wx.EVT_BUTTON, self.addpress)
            window_size.Add(add_button, 0, wx.UP | wx.CENTER, 0)
            panel.SetSizer(window_size)
            window_size.AddSpacer(5)

            close_button = wx.Button(panel, label='Close')
            close_button.Bind(wx.EVT_BUTTON, self.closepress)
            window_size.Add(close_button, 0, wx.UP | wx.CENTER, 0)
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

            turn = 0
            #initiate loop
            for i, j in self.classinfo.items():
                if isinstance(j, str) != True:
                    if i != 'Target':
                        if turn == 0:
                            mark = float(j[1])*(0.01*float(j[0]))
                        if turn != 0:
                            mark1 = float(j[1])*(0.01*float(j[0]))
                            mark = mark1 + mark
                            #summing up marks over loop
                        turn +=1
                    if i == 'Target':
                        target_mark = float(j[1]) - mark
                        #percentage of mark required to hit threshold
                        mark_reqd = (target_mark / float(j[0]))*100
                        #percentage out of 100 required on exam
                if isinstance(j, str) == True:
                    if i == 'classname':
                        my_course = j
                    if i == 'Date':
                    	exam_date = j

            my_course = my_course.upper() # make classname uppercase
            parent.addedclass = [my_course,str(int(mark_reqd)),exam_date]
            parent.newclassreload()
            """ 

            ### Currently commented out so that the saved txt ###
            ### file does not become filled up during testing ###

            if os.path.isfile('./save/saved.text'): # open existing save file
                saved = open('./save/saved.text','a+')
            else:
                saved = open('./save/saved.text','w+') # open new file
            #saved.write(my_course + ',' + '{:.1f}'.format(mark_reqd) + ',' + exam_date + '\n') # if writing as float (1 decimal prec)
            saved.write(my_course + ',' + str(int(mark_reqd)) + ',' + exam_date + '\n') # if writing as float (1 decimal prec)
            saved.close()
            """
            #print(my_course,mark_reqd,exam_date)
            #print(my_course,str(int(mark_reqd)),exam_date)
            self.Close()
            #return mark_reqd
            #return my_course
            #return exam_date



    AddClassWindow()


if __name__ == '__main__':
    AppName = 'Easy A' # Placeholder app name
    app = wx.App()
    if os.path.isfile('./save/saved.text'):
        savefile = open('./save/saved.text','r') # read previously inputted data (if available)
        savedata = savefile.read().splitlines()
        existingfile = True
        savefile.close()
    else:
        #savefile = open('./save/saved.text','w+') # read previously inputted data (if available)
        existingfile = False
    wx.AppConsole.SetAppName(app,AppName)
    wx.AppConsole.SetAppDisplayName(app,AppName)
    frame = MainMenu()
    app.MainLoop()

