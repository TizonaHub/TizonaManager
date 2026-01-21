from customtkinter import *
from config import *
from staticFuncs import *


class UpperFrame(CTkFrame):
    def __init__(self, parent, serverStatus):
        super().__init__(parent)

        self.lang = get_language_dict()
        self.t = self.lang["UpperFrame"]

        self.grid_columnconfigure((0, 1), weight=1, uniform="a")
        self.grid_rowconfigure(0, weight=1)

        self.statusColor, self.buttonText, self.statusText = self.updateValues(serverStatus)

        upperContainer1 = CTkFrame(self, fg_color="transparent")
        upperContainer1.grid_rowconfigure(0, weight=1)
        upperContainer1.grid_rowconfigure(1, weight=0)
        upperContainer1.grid_columnconfigure((0, 2), weight=1)

        self.statusBall = CTkFrame(upperContainer1,fg_color=self.statusColor,width=STATUSBALLSIZE,height=STATUSBALLSIZE,corner_radius=100)
        self.statusBall.grid(row=0, column=0, sticky="e", padx=(0, 10))

        self.statusTextLabel = CTkLabel(upperContainer1,text=self.statusText,font=(FONT, FSIZE),anchor="w",)
        self.statusTextLabel.grid(row=0, column=1)

        upperContainer1.grid(row=0, column=0, sticky="nsew")

        button_config = {
            "fg_color": "#0092d1",
            "text_color": "white",
            "cursor": "hand2",
            "hover_color": "#007bb5",
        }

        upperContainer2 = CTkFrame(self, fg_color="transparent")
        upperContainer2.grid_rowconfigure((0, 1, 2), weight=1)
        upperContainer2.grid_columnconfigure(0, weight=1)
        upperContainer2.grid(row=0, column=1, sticky="nsew")

        self.startStopButton = CTkButton(upperContainer2,**button_config,text=self.buttonText,command=lambda: self.handleClick(parent))
        self.startStopButton.grid(row=1, column=0)

        self.progressBarFrame = CTkFrame(self, fg_color="transparent", height=8)
        self.progressBarFrame.grid(row=1, column=0, columnspan=2, sticky="ns", pady=(0, 8))

        self.progressBar = CTkProgressBar(self.progressBarFrame,mode="indeterminate",progress_color="orange")
        self.progressBar.start()

    def handleClick(self, parent):
        self.progressBar.grid(row=1, column=0, columnspan=2)
        handleSetServerStatus(parent)

    def update(self, serverStatus):
        self.lang = get_language_dict()
        self.t = self.lang["UpperFrame"]

        self.updateValues(serverStatus)
        self.statusBall.configure(fg_color=self.statusColor)
        self.statusTextLabel.configure(text=self.statusText)
        self.startStopButton.configure(text=self.buttonText)
        self.progressBar.grid_forget()

    def updateValues(self, serverStatus):
        self.statusColor = ("green", "lime") if serverStatus else "red"
        self.buttonText = self.t["buttons"]["start_server"] if not serverStatus else self.t["buttons"]["stop_server"]

        self.statusText = self.t["status"]["server_not_running"]
        if serverStatus == 2:
            self.statusText = self.t["status"]["http_running"]
        elif serverStatus == 1:
            self.statusText = self.t["status"]["https_running"]

        return self.statusColor, self.buttonText, self.statusText
