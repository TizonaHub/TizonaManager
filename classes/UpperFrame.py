from customtkinter import *
from config import *
from staticFuncs import *
class UpperFrame(CTkFrame):
    def __init__(self,parent,serverStatus):
        super().__init__(parent)
        #UPPER FRAME
        self.grid_columnconfigure((0,1),weight=1,uniform='a')
        self.grid_rowconfigure(0,weight=1)
        #Container1 (INFO)
        self.statusColor,self.buttonText,self.statusText=self.updateValues(serverStatus)

        upperContainer1=CTkFrame(self,fg_color='transparent')
        upperContainer1.grid_rowconfigure(0,weight=1)
        upperContainer1.grid_columnconfigure((0,2),weight=1)
        
        self.statusBall=CTkFrame(upperContainer1,fg_color=self.statusColor,width=STATUSBALLSIZE,height=STATUSBALLSIZE,corner_radius=100)
        self.statusBall.grid(row=0,column=0,sticky='e',padx=(0,10))
        self.statusTextLabel=CTkLabel(upperContainer1,text=self.statusText,font=(FONT,FSIZE),anchor='w')
        self.statusTextLabel.grid(row=0,column=1)
        upperContainer1.grid(row=0,column=0,sticky='nsew')
        #Container2 (BUTTONS)
        button_config = {
        "fg_color": "#0092d1",
        "text_color": "white",
        "cursor": "hand2",
        "hover_color": "#007bb5",
        }
        upperContainer2=CTkFrame(self,fg_color='transparent')
        upperContainer2.grid_rowconfigure((0,1,2),weight=1)
        upperContainer2.grid_columnconfigure(0,weight=1)
        self.startStopButton=CTkButton(upperContainer2,**button_config,text=self.buttonText,command= lambda: handleSetServerStatus(parent))
        self.startStopButton.grid(row=1,column=0)
        #CTkButton(upperContainer2,**button_config,text='Enable auto startup',command= lambda: handleSetServerStatus(parent)).grid(row=1,column=0)
        #CTkButton(upperContainer2,**button_config,text='Disable auto startup',command= lambda: handleSetServerStatus(parent)).grid(row=2,column=0)

        upperContainer2.grid(row=0,column=1,sticky='nsew')
    
    def update(self,serverStatus):
        self.updateValues(serverStatus)
        self.statusBall.configure(fg_color=self.statusColor)
        self.statusTextLabel.configure(text=self.statusText)
        self.startStopButton.configure(text=self.buttonText)

    def updateValues(self,serverStatus):
        self.statusColor= ('green','lime') if serverStatus else 'red'
        self.buttonText='Start server' if not serverStatus else 'Stop server'
        self.statusText='Server is not running'
        if serverStatus==2: self.statusText='HTTP server is running'
        elif serverStatus ==1: self.statusText='HTTPS server is running'

        return self.statusColor,self.buttonText,self.statusText


