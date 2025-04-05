import requests
import socket
import subprocess
import os
from threading import Thread
from config import *
import sys

serverFilePath=os.path.abspath(os.path.abspath(os.path.dirname(__file__))+SERVER_FILE_NAME)
def getGeometry(self):
    screenWidth=self.winfo_screenwidth()
    screenHeight=self.winfo_screenheight()
    width=500
    height=400
    xPos=(screenWidth//2)-((width//2)+0)
    yPos=(screenHeight//2)-((height//2)+0)
    return f"{width}x{height}+{xPos}+{yPos}"

def getResPath(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    path=os.path.join(base_path, relative_path)
    return os.path.abspath(path)

def openAbout():
    os.startfile(getResPath('LICENSE'))
    os.startfile(getResPath('THIRD-PARTY-LICENSES.txt'))

def getServerStatus():
    url=f"http://localhost/api/testConnection"
    tries=0
    while tries <=1:
        print('url ',url)
        try:
            if requests.get(url,timeout=1,verify=False).status_code==200: 
                return 1 if tries==0 else 2 
        except:None
        url=f"https://localhost/api/testConnection"
        tries+=1
    return False

'''
0: stop server
1: start server
2: start server at startup
'''
def setServerStatus(order):
    try:
        process=subprocess.run(['npm','list', '-g','pm2'], capture_output=True, text=True,shell=True)
        if not'pm2' in process.stdout: raise ValueError()
    except:
        return False
    command=''
    path=os.path.abspath(os.path.join(get_app_dir(), SERVER_FILE_NAME if not isExe() else 'TizonaServer.js'))
    print('path: ', path)
    if order==0:   command= ['pm2','stop',path]
    elif order==1: command= ['pm2','start',path]
    elif order==2: command= ['pm2','startup']

    process=subprocess.run(command,shell=True)

    return getServerStatus()
        
def handleSetServerStatus(mainFrame):
    def task():
        status = setServerStatus(0) if getServerStatus() else setServerStatus(1)
        mainFrame.after(0, lambda:mainFrame.updateUpperFrame(status))

    thread = Thread(target=task)
    thread.start()
    
    
def get_app_dir():
    if getattr(sys, 'frozen', False): return os.path.dirname(sys.executable)
    else: return os.path.dirname(os.path.abspath(__file__))

def isExe():
    return getattr(sys, 'frozen', False)
