import os
import pickle
import shutil
import ctypes
import sys 
import traceback
from time import sleep
import locale
import subprocess
import tempfile
from pathlib import Path
LANG_ES = {
    "not_detected": "TizonaHub no fue detectado. Presiona Enter para salir.",
    "uninstall_warning": "Vas a desinstalar TizonaHub",
    "continue_question": "¿Quieres continuar?",
    "yes": "[y] --> sí",
    "no": "[n] --> no",
    "aborting": "Abortando...",
    "removed": "Eliminado",
    "uninstalled": (
        "TizonaHub ha sido desinstalado. La base de datos no fue eliminada, "
        "por lo que debes borrarla manualmente. "
        "Python, MySQL y Node.js siguen instalados."
    ),
    "press_enter": "Presiona Enter para terminar la desinstalación."
}

LANG_EN = {
    "not_detected": "TizonaHub was not detected. Press Enter to exit.",
    "uninstall_warning": "You are about to uninstall TizonaHub",
    "continue_question": "Do you want to continue?",
    "yes": "[y] --> yes",
    "no": "[n] --> no",
    "aborting": "Aborting...",
    "removed": "Removed",
    "uninstalled": (
        "TizonaHub has been uninstalled. The database was not deleted, "
        "so you should delete it manually. "
        "Python, MySQL, and Node.js are still installed."
    ),
    "press_enter": "Press Enter to finish."
}

def supports_ansi():
    return sys.stdout.isatty() and ('WT_SESSION' in os.environ or 'TERM' in os.environ)

def printGreen(msg): print(f'\033[92m{msg}\033[0m') if supports_ansi() else print(msg)
def get_system_language():
    try:
        locale.setlocale(locale.LC_ALL, "")
        lang, _ = locale.getlocale()  
    except:
        lang = None

    if lang:
        lang = lang.lower()
        if lang.startswith("es"):
            return "es"
        elif lang.startswith("en"):
            return "en"
        
    return "en" #default
def get_language_dict():
    lang = get_system_language()
    if lang == "es":
        return LANG_ES
    return LANG_EN


def getShell():
    if shutil.which('wt'): return shutil.which('wt')
    if shutil.which('powershell'): return shutil.which('powershell')
    if shutil.which('cmd'): return shutil.which('cmd')
def main():
    program_data = os.environ.get("PROGRAMDATA", r"C:\ProgramData")
    app_data_dir = os.path.join(program_data, "TizonaHub")
    data_file = os.path.join(app_data_dir, "data.dat")
    TXT = get_language_dict()


    def readData(index=False):
        info=None 
        try:
            with open(data_file, "rb") as f:
                    info = pickle.load(f)
                    return info if not index else info[index]
        except Exception as e:
            #print('Error at readData: ',e)
            return False

    data=readData()
    if not data:
        input(TXT["not_detected"])
        return

    print(TXT["uninstall_warning"])
    print(TXT["continue_question"])
    print(TXT["yes"])
    print(TXT["no"])

    if input().lower() != 'y':
        print(TXT["aborting"])
        print(3)
        sleep(1)
        print(2)
        sleep(1)
        print(1)
        sleep(1)
        return

    installPath = data['installationPath']
    serverPath=os.path.join(installPath,'TizonaServer')
    clientPath=os.path.join(installPath,'TizonaClient')
    licensesPath=os.path.join(installPath,'LICENSES')
    managerPath=os.path.join(installPath,'TizonaManager.exe')
    if os.path.isdir(serverPath):
        shutil.rmtree(serverPath)
        print(f'{TXT["removed"]} {serverPath}')
    if os.path.isdir(clientPath):
        shutil.rmtree(clientPath)
        print(f'{TXT["removed"]} {clientPath}')
    if os.path.isdir(licensesPath):
        shutil.rmtree(licensesPath)
        print(f'{TXT["removed"]} {licensesPath}')
    if os.path.isfile(managerPath):
        os.remove(managerPath)
        print(f'{TXT["removed"]} {managerPath}')

    if os.path.isdir(app_data_dir):
        shutil.rmtree(app_data_dir)
        print(f'{TXT["removed"]} {app_data_dir}')
    print()
    printGreen(TXT["uninstalled"])
    input(TXT["press_enter"])

    managerLink="C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Tizona Manager"
    if os.path.isfile(managerLink): os.remove(managerLink)

    



def initApp():
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    try:
        if is_admin():
            main()
        else: ctypes.windll.shell32.ShellExecuteW(None, "runas", getShell(), " ".join(sys.argv), None,True)  

    except:
        traceback.print_exc()
        input("\nPress enter to exit...")

initApp()