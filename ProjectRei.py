# Written and developed by Shoma Yamanouchi, Brian J. Park, and Hannah Cheng
# Contact: syamanou@physics.utoronto.ca OR xxx
# Website: https://sites.google.com/view/shoma-yamanouchi OR https://brianjmpark.github.io/ OR Hannah's websites
# version 1.0
# Developed in Python 2.7.18
version = '1.0'
DEVELOPED_BY_SHOMA = 'Easy A 2021 (c) was developed by:\nShoma Yamanouchi,\nBrian J. Park,\nand Hannah Cheng'

import os, sys, wx, csv
import wx.lib.scrolledpanel as scrolled

class MainMenu(wx.Frame):
    def __init__(self):
        super(MainMenu, self).__init__(parent=None, title='Easy A',size=(550,600))
        self.Bind(wx.EVT_ACTIVATE_APP, self.OnActivate)
        panel = wx.Panel(self)
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
        #self.text_ctrl = wx.TextCtrl(panel)
        #menu_sizer.AddSpacer(0)
        shoma_icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('./images/Easy_A_logo_mini.png'),style = wx.ALIGN_LEFT)
        menu_sizer.Add(shoma_icon, 0, wx.RIGHT | wx.LEFT, 20)
        #menu_sizer.AddSpacer(0)
        Header_font = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        Welcome = wx.StaticText(panel, -1, style = wx.ALIGN_LEFT)
        Welcome.SetLabel('Easy A\nMain Menu\n\n')
        Welcome.SetFont(Header_font)
        menu_sizer.Add(Welcome, 0, wx.RIGHT | wx.LEFT, 20)
        if existingfile:
            try:
                for i,row in enumerate(savedata):
                    classname = row.split(',')[0]
                    target = row.split(',')[1]
                    date = row.split(',')[2]
                    if i == 0:
                        Header = wx.StaticText(panel, -1, style = wx.ALIGN_LEFT)
                        Header.SetFont(Header_font.Underlined())
                        Header.SetLabel('Class: \t Target Score  \tExam Date\n')
                        menu_sizer.Add(Header, 0, wx.RIGHT | wx.LEFT, 20)
                    Grades = wx.StaticText(panel, -1, style = wx.ALIGN_LEFT)
                    Grades.SetFont(Header_font)
                    Grades.SetLabel(classname + ':\t' + target + '% \t' + date + '\n')
                    menu_sizer.Add(Grades, 0, wx.RIGHT | wx.LEFT, 20)

            except: pass
        else: pass

        start_button = wx.Button(panel, label='Add Class') # button to add class (calls self.start_press function)
        start_button.Bind(wx.EVT_BUTTON, self.start_press)
        menu_sizer.Add(start_button, 0, wx.UP | wx.LEFT, 20)
        menu_sizer.AddSpacer(5)

        quit_button = wx.Button(panel, label='Quit') # button to quit the program
        quit_button.Bind(wx.EVT_BUTTON, self.QuitAll)
        menu_sizer.Add(quit_button, 0, wx.DOWN | wx.LEFT, 20)
        menu_sizer.AddSpacer(15)

        menu_sizer.Add((0,0), 1, wx.EXPAND)
        shoma_statement = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
        shoma_statement_font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        shoma_statement.SetFont(shoma_statement_font)
        shoma_statement.SetLabel('Version '+version + '\n' + DEVELOPED_BY_SHOMA)
        menu_sizer.Add(shoma_statement,1,wx.UP | wx.CENTER,0)
        panel.SetSizer(menu_sizer)
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
    def start_press(self, event): # add class, calls AddClassWindow, which opens a pop up
        #inputpath = self.text_ctrl.GetValue()
        classinfo = AddClassWindow(self)  
        return classinfo 
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
    class AddClassWindow(wx.Frame):
        def __init__(self):
            super(AddClassWindow, self).__init__(parent=parentframe, title='Adding a class',size=(400, 700))#(400, 400)
            panel = wx.Panel(self)
            window_size = wx.BoxSizer(wx.VERTICAL)
            self.classinfo = dict()

            Name = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
            Name.SetLabel('Class Name (e.g., MATH101)')
            window_size.Add(Name, 0, wx.UP | wx.CENTER, 15)
            self.text_ctrl = wx.TextCtrl(panel)
            window_size.Add(self.text_ctrl, 0, wx.UP | wx.CENTER, 15)
            classname = self.text_ctrl.GetValue()
            self.classinfo['classname'] = classname

            Quiz = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
            Quiz.SetLabel('Quiz weight (0-100%) and your score')
            window_size.Add(Quiz, 0, wx.UP | wx.CENTER, 15)
            self.text_ctrl1 = wx.TextCtrl(panel)
            window_size.Add(self.text_ctrl1, 0, wx.UP | wx.CENTER, 15)
            quizweight = self.text_ctrl1.GetValue()
            self.text_ctrl11 = wx.TextCtrl(panel)
            window_size.Add(self.text_ctrl11, 0, wx.UP | wx.CENTER, 15)
            quizscore = self.text_ctrl11.GetValue()
            self.classinfo['quiz'] = (quizweight,quizscore)

            Assignment = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
            Assignment.SetLabel('Assignment weight (0-100%) and your score')
            window_size.Add(Assignment, 0, wx.UP | wx.CENTER, 15)
            self.text_ctrl2 = wx.TextCtrl(panel)
            window_size.Add(self.text_ctrl2, 0, wx.UP | wx.CENTER, 15)
            Assignmentweight = self.text_ctrl2.GetValue()
            self.text_ctrl21 = wx.TextCtrl(panel)
            window_size.Add(self.text_ctrl21, 0, wx.UP | wx.CENTER, 15)
            Assignmentscore = self.text_ctrl21.GetValue()
            self.classinfo['Assignment'] = (Assignmentweight,Assignmentscore)

            Midterm = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
            Midterm.SetLabel('Midterm weight (0-100%) and your score')
            window_size.Add(Midterm, 0, wx.UP | wx.CENTER, 15)
            self.text_ctrl3 = wx.TextCtrl(panel)
            window_size.Add(self.text_ctrl3, 0, wx.UP | wx.CENTER, 15)
            Midtermweight = self.text_ctrl3.GetValue()
            self.text_ctrl31 = wx.TextCtrl(panel)
            window_size.Add(self.text_ctrl31, 0, wx.UP | wx.CENTER, 15)
            Midtermscore = self.text_ctrl31.GetValue()
            self.classinfo['Midterm'] = (Midtermweight,Midtermscore)
            window_size.AddSpacer(60)
            add_button = wx.Button(panel, label='Add')
            add_button.Bind(wx.EVT_BUTTON, self.addpress)
            window_size.Add(add_button, 0, wx.UP | wx.CENTER, 0)
            panel.SetSizer(window_size)
            window_size.AddSpacer(30)

            close_button = wx.Button(panel, label='Close')
            close_button.Bind(wx.EVT_BUTTON, self.closepress)
            window_size.Add(close_button, 0, wx.UP | wx.CENTER, 0)
            panel.SetSizer(window_size)
            self.Show()
            
        def closepress(self, event):
            self.Close()
            return False
        def addpress(self, event):
            self.Close()
            return self.classinfo
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

