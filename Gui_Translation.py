import wx
import sys, os
import Global_var
import wx.adv
import wx.lib.scrolledpanel
import pymysql.cursors

# class MyFrame1(wx.Frame):    
#     def __init__(self):
#         super().__init__(parent=None, title='Drive',pos = (100,150), size =(500,130),style = wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)
#         self.panel = wx.Panel(self)
#         self.Select_Drive = wx.StaticText(self.panel,label = "Select Drive : ",pos=(13, 30))
#         font = wx.Font(12, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
#         self.Select_Drive.SetFont(font)
#         drive = ['D','E']
#         self.Select_Drive_drop = wx.ComboBox(self.panel,choices = drive,pos=(130, 29),size=(80, 25))
#         font1 = wx.Font(11, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
#         self.Select_Drive_drop.SetFont(font1)

#         self.Go_btn = wx.Button(self.panel, label='GO', pos=(250, 30),style=wx.NO_BORDER)
#         font = wx.Font(10, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
#         self.Go_btn.SetFont(font)
#         self.Go_btn.Bind(wx.EVT_BUTTON, self.go_fun)
#         self.Go_btn.SetForegroundColour('Black')
#         self.Go_btn.SetBackgroundColour('Green')

#         self.Exit_btn = wx.Button(self.panel, label='EXIT', pos=(350, 30),style=wx.NO_BORDER)
#         font = wx.Font(10, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
#         self.Exit_btn.SetFont(font)
#         self.Exit_btn.Bind(wx.EVT_BUTTON, self.exit_fun)
#         self.Exit_btn.SetForegroundColour('White')
#         self.Exit_btn.SetBackgroundColour('Red')

#         self.Show()
#     def go_fun(self,event):
#         drive:str = self.Select_Drive_drop.GetValue()
#         if drive != '':
#             Global_var.Drive = drive
#             self.Destroy()
#             frame = MyFrame()
#         else:
#             wx.MessageBox(' -_- Please Select Drive  -_- ', 'Gui Translation',
#                           wx.OK | wx.ICON_ERROR)

#     def exit_fun(self,event):
#         dlg = wx.MessageDialog(None, "Kya Aap Ko yaha Se Prasthan (EXIT) karna Hai !!!!", 'Gui Translation', wx.YES_NO | wx.ICON_WARNING)
#         result = dlg.ShowModal()
#         if result == wx.ID_YES:
#             self.Destroy()
#             sys.exit()
#         else:
#             pass

def connection():
    connection = ''
    a3 = 0
    while a3 == 0:
        try:
            connection = pymysql.connect(host='185.142.34.92',
                                         user='ams',
                                         password='TgdRKAGedt%h',
                                         db='tenders_db',
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
            return connection
        except pymysql.connect as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,
                  "\n", exc_tb.tb_lineno)
            time.sleep(10)
            a3 = 0
            connection.close()


class MyFrame(wx.Frame):   
     
    def __init__(self):
        super().__init__(parent=None, title='Google Translation GUI',pos = (100,150), size =(800,500) ,style = wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)
        self.panel = wx.Panel(self,size=(800, 75), pos=(0, 0), style=wx.SIMPLE_BORDER)
        self.bSizer = wx.BoxSizer(wx.VERTICAL)
        self.bSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.scroll = wx.lib.scrolledpanel.ScrolledPanel(self, -1, size=(767, 365), pos=(7, 82),
                                                         style=wx.SIMPLE_BORDER)
        self.scroll.SetupScrolling()
        self.scroll.SetBackgroundColour('#FFFFFF')
        self.scroll.SetForegroundColour('Black')
        self.scroll.SetSizer(self.bSizer)

        # self.Source_lbl = wx.StaticText(self.panel,label = "Add Source Name Like This -> SourcName~Server",pos=(13, 40))
        # self.Source_lbl.SetForegroundColour('Red')

        # self.Source_TB = wx.TextCtrl(self.panel, pos=(110, 10),size=(200, 25))

        # self.Source_btn = wx.Button(self.panel, label='Add Source', pos=(10, 10))
        # font = wx.Font(10, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        # self.Source_btn.SetFont(font)
        # self.Source_btn.Bind(wx.EVT_BUTTON, self.Add_Source)
        
        # self.Select_Source_lbl = wx.StaticText(self.panel,label = "Select Source : ",pos=(340, 14))
        # self.Select_Source_lbl.SetFont(font)

        # f = open(f"C:\\Translation EXE\\source_list.txt", "r")
        # f = f.read()
        # Source_list = str(f).splitlines()
        trasns = connection()
        cur = trasns.cursor()
        cur.execute("SELECT source,COUNT(source) AS `count` FROM l2l_tenders_tbl WHERE `is_english` = '1' GROUP BY source ORDER BY COUNT(source) DESC")  # 0 = English, 1 = Non-English
        rows = cur.fetchall()
        Source_list = []
        for row in rows:
            source_val = "%s" % (row["source"])
            count_val = "%s" % ((row["count"]))
            Source_list.append(f'{source_val} = {count_val}')
        self.Panel_Height = 2
        self.cb_list = []
        for source in Source_list:
            self.scroll_panel = wx.Panel(self.scroll, size=(735, 30), pos=(4, self.Panel_Height),
                                         style=wx.SIMPLE_BORDER)
            self.scroll_panel.SetBackgroundColour('#7854E0')
            self.cb = wx.CheckBox(self.scroll_panel, -1, str(source), (12, 6))
            self.cb.SetForegroundColour('White')
            self.cb_list.append(self.cb)

            self.bSizer.Add(self.scroll_panel, 0, wx.ALL, 5)
            self.scroll.SetupScrolling()

        self.Go_btn = wx.Button(self.panel, label='GO', pos=(580, 10),style=wx.NO_BORDER)
        font = wx.Font(10, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.Go_btn.SetFont(font)
        self.Go_btn.Bind(wx.EVT_BUTTON, self.GO_btn)
        self.Go_btn.SetForegroundColour('Black')
        self.Go_btn.SetBackgroundColour('Green')

        self.Exit_btn = wx.Button(self.panel, label='EXIT', pos=(680, 10),style=wx.NO_BORDER)
        font = wx.Font(10, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        # self.Source_btn.SetFont(font)
        self.Exit_btn.Bind(wx.EVT_BUTTON, self.exit)
        self.Exit_btn.SetForegroundColour('White')
        self.Exit_btn.SetBackgroundColour('Red')
        
        self.Show()

    # def Add_Source(self,event):
    #     Source_Name = self.Source_TB.GetValue()
    #     if str(Source_Name) != '':
    #         f = open(f"C:\\Translation EXE\\source_list.txt", "a")
    #         f.write(f'{str(Source_Name)}\n')
    #         f.close()
    #         print(f'{str(Source_Name)} This Source Name & Server added On Text File')
    #         self.Source_btn.SetForegroundColour('Black')
    #         self.Source_btn.SetBackgroundColour('Green')
    #         wx.MessageBox(' -_- Source Added  -_- ', 'Gui Translation',
    #                       wx.OK | wx.ICON_INFORMATION)
    #         self.Source_btn.SetForegroundColour('')
    #         self.Source_btn.SetBackgroundColour('')
    #     else:
    #         self.Source_btn.SetForegroundColour('White')
    #         self.Source_btn.SetBackgroundColour('Red')
    #         print('Null value Not Accepted Please Add Source Name & Server on TextBox')
    #         wx.MessageBox(' -_- Null value Not Accepted Please Add Source Name & Server on TextBox  -_- ', 'Gui Translation',
    #                       wx.OK | wx.ICON_ERROR)
    #         self.Source_btn.SetForegroundColour('')
    #         self.Source_btn.SetBackgroundColour('')
        
    def GO_btn(self,event):

        source_name_list = []
        for i, self.cb in enumerate(self.cb_list):
            if self.cb.GetValue():
                Source_name = self.cb.GetLabelText()
                Source_name1 = Source_name.partition("=")[0].strip()
                source_name_list.append(Source_name1)
        Global_var.Source_Name = str(source_name_list).replace('[', '').replace(']', '')
        if Global_var.Source_Name !="":
            print(f'Selected Source : {Global_var.Source_Name}')
            # print(Global_var.Server)
            self.Destroy()
            
        else:
            wx.MessageBox(' -_- Please Select Source  -_- ', 'Gui Translation',
                          wx.OK | wx.ICON_ERROR)

        
    def exit(self,event):
        dlg = wx.MessageDialog(None, "Kya Aap Ko yaha Se Prasthan (EXIT) karna Hai !!!!", 'Gui Translation', wx.YES_NO | wx.ICON_WARNING)
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            self.Destroy()
            sys.exit()
        else:
            pass

if __name__ == '__main__':
    app = wx.App()
    # frame = MyFrame1()
    frame = MyFrame()
    app.MainLoop()

import Google_Translation

