from staticFuncs import *
from customtkinter import *
from tkinter import *
from classes.UpperFrame import UpperFrame
from classes.InfoFrame import InfoFrame
from config import *
import traceback
import ctypes

class App(CTk):
    def __init__(self):
        super().__init__()
        self.resizable(False,False)
        self.geometry(getGeometry(self))
        self.grid_rowconfigure((0),weight=1)
        self.grid_rowconfigure((1),weight=3)
        self.grid_columnconfigure(0,weight=1)
        serverStatus=getServerStatus()
        self.upperFrame=UpperFrame(self,serverStatus)
        self.upperFrame.grid(row=0,column=0,sticky='nsew')
        self.infoFrame=InfoFrame(self)
        self.infoFrame.grid(row=1,column=0,sticky='nsew')

    def updateUpperFrame(self,serverStatus):
        newFrame=UpperFrame(self,serverStatus)
        self.upperFrame.destroy()
        self.upperFrame=newFrame
        self.upperFrame.grid(row=0,column=0,sticky='nsew')

def initApp():
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    try:
        if is_admin():
            app = App()
            app.mainloop()
        else: ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, True)  

    except:
        traceback.print_exc()
        input("\nPress enter to exit...")

initApp()