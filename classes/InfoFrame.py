from customtkinter import *
from config import FONT, FSIZE
import requests
from staticFuncs import (
    openAbout, getIp, update, readData, downloadResource,
    getResPath, getShell, isExe, get_language_dict,setServerStatus
)
import subprocess
import os
from pathlib import Path
import tempfile
import shutil

class InfoFrame(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        lang = get_language_dict()
        t = lang["InfoFrame"]  # shortcut
        ip = getIp()
        button_config = {
            "text_color": "white",
            "cursor": "hand2",
        }

        CTkLabel(self,text=t["labels"]["host_ip"].format(ip=ip),font=(FONT, FSIZE)).pack(pady=10)

        CTkButton(self,**button_config,text=t["buttons"]["update"],command=self.handleUpdate,
                  fg_color="#006d09",hover_color="#005807").pack(pady=10)

        CTkButton(self,**button_config,text=t["buttons"]["uninstall"],command=self.handleUninstall,
                  fg_color="#d10000",hover_color="#910000").pack(pady=10) 
        self.updateWarning = CTkLabel(self,text=t["labels"]["up_to_date"],font=(FONT, FSIZE))

        CTkLabel(self,text=t["labels"]["version"],text_color="gray",font=(FONT, FSIZE - 2)).pack()

        about = CTkLabel(self,text=t["labels"]["about"],font=(FONT, FSIZE),text_color=("blue", "#4999ff"),cursor="hand2")
        about.pack()
        about.bind("<Button-1>", lambda event: openAbout())

    def handleUninstall(self):
        exePath = getResPath("uninstall.exe")
        temp_path = Path(tempfile.gettempdir())
        dest = os.path.join(temp_path, "uninstall.exe")
        if exePath:
            shutil.copy(exePath, dest)
            if os.path.isfile(dest):
                setServerStatus(3)
                self.openTerminalAndEnd(dest)

    def handleUpdate(self):
        data = readData()
        installerVersion = data["installerVersion"]
        temp_path = Path(tempfile.gettempdir())
        response = requests.get("https://tizonahub.com/downloads/installers/windows/latest?data=true")
        responseText = response.text
        latestVersion = responseText.split("v")[1].replace(".exe", "")
        if latestVersion > installerVersion:
            exePath = ""
            if isExe():
                exePath = os.path.join(temp_path, "installerLatest.exe")
                downloadResource("https://tizonahub.com/downloads/installers/windows/latest", exePath)
            else:
                exePath = getResPath("installerLatest")
            self.openTerminalAndEnd(exePath)
        else:
            self.updateWarning.configure(text_color="lime")
            self.updateWarning.pack()
            self.after(3000, self.updateWarning.pack_forget)

    def openTerminalAndEnd(self, exePath):
        shell = getShell()

        if shell is None:
            raise RuntimeError("Shell is not available")

        shell = shell.lower()
        if shell.endswith("wt.exe"):
            subprocess.Popen([shell, exePath, "--update"], creationflags=subprocess.CREATE_NEW_CONSOLE)
        elif shell.endswith("powershell.exe"):
            subprocess.Popen(
                [shell, "-Command", f'Start-Process "{exePath}" -ArgumentList "--update"'],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        elif shell.endswith("cmd.exe"):
            subprocess.Popen(
                [shell, "/c", "start", "", exePath, "--update"],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        os._exit(1)
