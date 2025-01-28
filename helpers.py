from tkinter import *
from tkinter import ttk
from tktooltip import ToolTip
import os
from tkinter.filedialog import askopenfilename, askdirectory
import subprocess
import shutil
import datetime

class FuncMenu():

    def __init__(self, master, variable=None, default=None, *values, command):
        self.menu = OptionMenu(master, variable, *values, command=self.callback)
        self.command = command
        self.name = variable
        self.text = variable.get()
    def callback(self, opt):
        print(opt)
        self.command(opt)
        self.name.set(self.text)

class Console():

    def __init__(self, master, startText:str='', columnn=0, roww=0, widthh=100, heightt=20):
        self.column = columnn
        self.row = roww
        self.width = widthh
        self.height = heightt
        self.miniTerminal = Text(master, width=self.width, height=self.height)
        ys = Scrollbar(master, orient='vertical', command=self.miniTerminal.yview)
        self.miniTerminal['yscrollcommand'] = ys.set
        self.miniTerminal.insert('1.0', startText)
        self.miniTerminal['state'] = 'disabled'
    
    def setOutput(self, replace):
        self.miniTerminal['state'] = 'normal'
        self.miniTerminal.delete('1.0', 'end')
        self.miniTerminal.insert('1.0', replace)
        self.miniTerminal['state'] = 'disabled'
    
    def subprocessHelper(self, query):
        tOutputTmp = query.split('\n')
        tOutputTmp.pop(0)
        tOutput = ''
        count = -1
        llChk = len(tOutputTmp) - 1
        if len(tOutputTmp) == 1:
            tOutput += tOutputTmp[0]
        else:
            for l in tOutputTmp:
                count += 1
                if count == llChk:
                    tOutput += tOutputTmp[count]
                else:
                    tOutput += tOutputTmp[count] + '\n'
        return tOutput
    
    def show(self):
        self.miniTerminal.grid(column=self.column, row=self.row, sticky=(N, S, E, W), columnspan=69)
    
    def hide(self):
        self.miniTerminal.grid_remove()

class BoolEntry():

    def __init__(self, master, textvariable, placeholder="placeholder", bg="white", fg="black"):
        self.placeholder = placeholder
        self.entry = Entry(master, state="disabled", textvariable=textvariable, bg=bg, fg=fg)
    
    def grid(self, column=0, row=0, padx=0, pady=0, sticky="nsew"):
        self.entry.grid(column=column, row=row, padx=padx, pady=pady, sticky=sticky)
    
    def unlock(self):
        self.entry["state"] = 'normal'
        self.entry.delete('0', 'end')
    
    def lock(self):
        self.entry.delete('0', 'end')
        self.entry.insert('0', self.placeholder)
        self.entry["state"] = 'disabled'

class BoolSpinbox():

    def __init__(self, master, range=[0,1], increment=1, bg="white", fg="black"):
        self.entry = Spinbox(master, state="disabled", from_=range[0], to=range[1], bg=bg, buttonbackground=bg, fg=fg, increment=increment, width=3)
    
    def grid(self, column=0, row=0, padx=0, pady=0, sticky="nsew"):
        self.entry.grid(column=column, row=row, padx=padx, pady=pady, sticky=sticky)
    
    def unlock(self):
        self.entry["state"] = 'normal'
    
    def lock(self):
        self.entry["state"] = 'disabled'
    
    def get(self):
        return self.entry.get()
