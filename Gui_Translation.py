import wx
import sys, os
import Global_var

class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='Google Translation GUI',pos = (100,150), size =(950,130),style = wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)
        self.panel = wx.Panel(self)

        self.Source_lbl = wx.StaticText(self.panel,label = "Add Source Name Like This -> SourcName~Server",pos=(13, 40))
        self.Source_lbl.SetForegroundColour('Red')

        self.Source_TB = wx.TextCtrl(self.panel, pos=(110, 10),size=(200, 25))

        self.Source_btn = wx.Button(self.panel, label='Add Source', pos=(10, 10))
        font = wx.Font(10, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.Source_btn.SetFont(font)
        self.Source_btn.Bind(wx.EVT_BUTTON, self.Add_Source)
        
        self.Select_Source_lbl = wx.StaticText(self.panel,label = "Select Source : ",pos=(340, 14))
        self.Select_Source_lbl.SetFont(font)

        f = open("D:\\Translation EXE\\source_list.txt", "r")
        f = f.read()
        Source_list = str(f).splitlines()
        self.combo = wx.ComboBox(self.panel,choices = Source_list,pos=(450, 10),size=(250, 25))
        font1 = wx.Font(11, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.combo.SetFont(font1)

        self.Go_btn = wx.Button(self.panel, label='GO', pos=(730, 10),style=wx.NO_BORDER)
        font = wx.Font(10, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.Go_btn.SetFont(font)
        self.Go_btn.Bind(wx.EVT_BUTTON, self.GO_btn)
        self.Go_btn.SetForegroundColour('Black')
        self.Go_btn.SetBackgroundColour('Green')

        self.Exit_btn = wx.Button(self.panel, label='EXIT', pos=(830, 10),style=wx.NO_BORDER)
        font = wx.Font(10, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.Source_btn.SetFont(font)
        self.Exit_btn.Bind(wx.EVT_BUTTON, self.exit)
        self.Exit_btn.SetForegroundColour('White')
        self.Exit_btn.SetBackgroundColour('Red')

        self.Show()

    def Add_Source(self,event):
        Source_Name = self.Source_TB.GetValue()
        if str(Source_Name) != '':
            f = open("D:\\Translation EXE\\source_list.txt", "a")
            f.write(f'{str(Source_Name)}\n')
            f.close()
            print(f'{str(Source_Name)} This Source Name & Server added On Text File')
            self.combo.AppendItems(Source_Name)
            print(f'{str(Source_Name)} This Source Name Updated On Dropdown')
            self.Source_btn.SetForegroundColour('Black')
            self.Source_btn.SetBackgroundColour('Green')
            wx.MessageBox(' -_- Null value Not Accepted Please Add Source Name & Server on TextBox  -_- ', 'Gui Translation',
                          wx.OK | wx.ICON_ERROR)
            self.Source_btn.SetForegroundColour('')
            self.Source_btn.SetBackgroundColour('')
        else:
            self.Source_btn.SetForegroundColour('White')
            self.Source_btn.SetBackgroundColour('Red')
            print('Null value Not Accepted Please Add Source Name & Server on TextBox')
            wx.MessageBox(' -_- Null value Not Accepted Please Add Source Name & Server on TextBox  -_- ', 'Gui Translation',
                          wx.OK | wx.ICON_ERROR)
            self.Source_btn.SetForegroundColour('')
            self.Source_btn.SetBackgroundColour('')
        
    def GO_btn(self,event):
        Drop_Value:str = self.combo.GetValue()
        if str(Drop_Value) != '':
            print(f'Selected Dropdown Value : {Drop_Value}')
            Global_var.Source_Name = Drop_Value.partition("~")[0]
            Global_var.Server = Drop_Value.partition("~")[2]	
        else:
            wx.MessageBox(' -_- Plaese Select Dropdown Value  -_- ', 'Gui Translation',
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
    frame = MyFrame()
    app.MainLoop()