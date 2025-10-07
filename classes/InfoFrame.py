from customtkinter import *
from config import FONT,FSIZE
import socket
from staticFuncs import openAbout,getIp
class InfoFrame(CTkFrame):
    def __init__(self,parent):
        super().__init__(parent,fg_color='transparent')
        ip=getIp()
        CTkLabel(self,text=f'Host IP adress is {ip}',font=(FONT,FSIZE)).pack(pady=10)
        CTkLabel(self,text='v0.4.0',text_color='gray',font=(FONT,FSIZE-2)).pack()
        about=CTkLabel(self,text=f'About',font=(FONT,FSIZE),text_color=('blue','#4999ff'),cursor='hand2')
        about.pack()
        about.bind('<Button-1>', lambda event: openAbout())

