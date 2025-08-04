from staticFuncs import *
from customtkinter import *
from tkinter import *
from classes.UpperFrame import UpperFrame
from classes.InfoFrame import InfoFrame
from time import sleep
from config import *
import traceback
import ctypes
import threading

class App(CTk):
    def __init__(self):
        super().__init__()
        self.resizable(False,False)
        self.title('Tizona manager')
        self.iconbitmap(getResPath('icon.ico'))
        self.geometry(getGeometry(self))
        self.grid_rowconfigure((0),weight=1)
        self.grid_rowconfigure((1),weight=3)
        self.grid_columnconfigure(0,weight=1)
        serverStatus=0 #getServerStatus()
        self.upperFrame=UpperFrame(self,serverStatus)
        self.upperFrame.grid(row=0,column=0,sticky='nsew')
        self.infoFrame=InfoFrame(self)
        self.infoFrame.grid(row=1,column=0,sticky='nsew')
        self.sendPingReq=False
       
        self.after(100, lambda: threading.Thread(target=self.ping, daemon=True).start())

        

    def ping(self,times=2):
        counter=1
        while counter<=times:
            sleep(0.2)
            status = getServerStatus()
            if status:
                self.after(0, lambda: self.updateUpperFrame(status))
                break
            counter=counter+1

    def updateUpperFrame(self,serverStatus):
        self.upperFrame.update(serverStatus)

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
        else: ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, DEBUG_MODE)  

    except:
        traceback.print_exc()
        input("\nPress enter to exit...")

initApp()