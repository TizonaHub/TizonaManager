import requests
import socket
import subprocess
import os
from threading import Thread
from config import *
import sys
from time import sleep
serverFilePath=os.path.abspath(os.path.abspath(os.path.dirname(__file__))+SERVER_FILE_NAME)

def getIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

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
    sleep(0.5)
    os.startfile(getResPath('licenses'))

# 0: SERVER UNREACHABLE
# 1: HTTPS
# 2: HTTP
def getServerStatus(maxTries=2,timeoutParam=1):
    print('maxTries: ', maxTries)
    url=f"http://localhost/api/system/ping"
    tries=1
    while tries <=maxTries:
        module=tries % 2 ==0
        url=f"https://localhost/api/system/ping" if module else f"http://localhost/api/system/ping"
        print('url: ', url)
        try:
            if requests.get(url,timeout=timeoutParam,verify=False).status_code==200: 
                return 1 if module else 2  #1: HTTPS  ||   2: HTTP
        except:None
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
    path=os.path.abspath(os.path.join(get_app_dir(), SERVER_FILE_NAME if not isExe() else 'TizonaServer/start.js'))
    
    if order==0:   command= ['pm2','stop',path]
    elif order==1: command= ['pm2','start', path]
    elif order==2: command= ['pm2','startup']

    process=subprocess.run(command,shell=True,check=True,cwd=os.path.dirname(path))
        
def handleSetServerStatus(mainComponent=False):
    def task():
        status=getServerStatus()
        setServerStatus(0) if status else setServerStatus(1)
        if status and mainComponent:
            mainComponent.after(0, lambda: mainComponent.updateUpperFrame(0))
        else:
            if mainComponent:
                mainComponent.ping(6)
            else:
                status=getServerStatus(6,0.5) 
                mainComponent.after(0, lambda: mainComponent.updateUpperFrame(status))

    thread = Thread(target=task)
    thread.start()
    
    
def get_app_dir():
    if getattr(sys, 'frozen', False): return os.path.dirname(sys.executable)
    else: return os.path.dirname(os.path.abspath(__file__))

def isExe():
    return getattr(sys, 'frozen', False)
