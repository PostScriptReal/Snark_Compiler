from tkinter import *
from tkinter import ttk
from tktooltip import ToolTip
import os
from tkinter.filedialog import askopenfilename, askdirectory
import subprocess
import shutil
import datetime
import webbrowser as browser
import get_image_size

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
    
    def grid_remove(self):
        self.entry.grid_remove()
    
    def unlock(self):
        self.entry["state"] = 'normal'
        self.entry.delete('0', 'end')
    
    def lock(self):
        self.entry.delete('0', 'end')
        self.entry.insert('0', self.placeholder)
        self.entry["state"] = 'disabled'

class BoolSpinbox():

    def __init__(self, master, range=[0,1], increment=1, bg="white", bBG="bisque", fg="black"):
        self.entry = Spinbox(master, state="disabled", from_=range[0], to=range[1], bg=bg, buttonbackground=bBG, fg=fg, increment=increment, width=3)
    
    def grid(self, column=0, row=0, padx=0, pady=0, sticky="nsew"):
        self.entry.grid(column=column, row=row, padx=padx, pady=pady, sticky=sticky)
    
    def unlock(self):
        self.entry["state"] = 'normal'
    
    def lock(self):
        self.entry["state"] = 'disabled'
    
    def get(self):
        return self.entry.get()
    def changeTheme(self, newBG, newBbg, newFG):
        self.entry.config(bg=newBG)
        self.entry.config(buttonbackground=newBbg)
        self.entry.config(fg=newFG)

class QCHandler:

    def __init__(self, qc):
        f = open(qc, 'r')
        self.qcf = f.readlines()
        f.close()
        self.qcLoc = os.path.dirname(qc)
        self.cbarFrmt = False
    
    def crowbarFormatCheck(self):
        checks = 0
        count = -1
        cd = False
        cdTex = 0
        newCD = ""
        cdRef = 0
        newCDtex = ""
        cdTexR = 0
        self.newQC = self.qcf
        self.newQCPath = ""
        while checks < 2:
            count += 1
            qcL = self.qcf[count]
            if qcL.startswith("$cdtex"):
                if qcL.find('\"./textures/\"') != -1:
                    cdTex = 1
                    cdTexR = count
                    checks += 1
                elif qcL.find('\".\"') != -1:
                    cdTex = 2
                    cdTexR = count
                    checks += 1
            elif qcL.startswith("$cd") and qcL.find('\".\"') != -1:
                cd = True
                cdRef = count
                checks += 1
        if cd or cdTex != 0:
            self.cbarFrmt = True
            print(cd)
            print(cdTex)
            if cd:
                newCD = self.qcf[cdRef]
                newCD = newCD.replace('\".\"', f'\"{self.qcLoc}\"')
                self.newQC[cdRef] = newCD
                print(newCD)
            if cdTex == 1:
                newCDtex = self.qcf[cdTexR]
                newCDtex = newCDtex.replace('\"./textures/\"', f'\"{self.qcLoc}/textures/\"')
                self.newQC[cdTexR] = newCDtex
            elif cdTex == 2:
                newCDtex = self.qcf[cdTexR]
                newCDtex = newCDtex.replace('\".\"', f'\"{self.qcLoc}\"')
                self.newQC[cdTexR] = newCDtex
            self.newQCPath = os.path.join(self.qcLoc, "temp.qc")
            f = open(self.newQCPath, "w")
            f.write("".join(self.newQC))
            f.close()
    def getMDLname(self):
        checks = 0
        count = -1
        capture = False
        mdlName = ""
        while checks < 1:
            count += 1
            qcL = self.qcf[count]
            if qcL.startswith("$modelname"):
                for c in qcL:
                    if capture:
                        mdlName += c
                    if c == '\"' and not capture:
                        capture = True
                    elif c == '\"' and capture:
                        capture = False
                        break
                break
        return mdlName[:-1]
    
    def check1024px(self):
        checks = 0
        count = -1
        newCDtex = ""
        self.newQC = self.qcf
        self.newQCPath = ""
        self.found1024 = False
        while checks < 1:
            count += 1
            qcL = self.qcf[count]
            if qcL.startswith("$cdtex"):
                if qcL.find('\"./textures/\"') != -1:
                    cdTex = 1
                    checks += 1
                elif qcL.find('\".\"') != -1:
                    cdTex = 2
                    checks += 1
        if cdTex != 0:
            if cdTex == 1:
                count = -1
                texPath = os.path.join(self.qcLoc, "textures/")
                textures = os.listdir(texPath)
                while count < len(textures)-1:
                    count += 1
                    tex = textures[count]
                    fTex = os.path.join(self.qcLoc,tex)
                    if os.path.isfile(fTex):
                        try:
                            width, height = get_image_size.get_image_size(os.path.join(self.qcLoc,tex))
                        except get_image_size.UnknownImageFormat:
                            width, height = -1, -1
                        if width > 512 or height > 512:
                            self.found1024 = True
            elif cdTex == 2:
                count = -1
                files = os.listdir(self.qcLoc)
                textures = []
                while count < len(files)-1:
                    count += 1
                    if files[count].endswith('.bmp'):
                        textures.append(files[count])
                count = -1
                while count < len(textures)-1:
                    count += 1
                    tex = textures[count]
                    fTex = os.path.join(self.qcLoc,tex)
                    if os.path.isfile(fTex):
                        try:
                            width, height = get_image_size.get_image_size(os.path.join(self.qcLoc,tex))
                        except get_image_size.UnknownImageFormat:
                            width, height = -1, -1
                        if width > 512 or height > 512:
                            self.found1024 = True
        return self.found1024
    
    def checkCHROME(self):
        checks = 0
        count = -1
        newCDtex = ""
        texmodes = []
        self.newQC = self.qcf
        self.newQCPath = ""
        self.fndUnlChr = False
        while count < len(self.qcf)-1:
            count += 1
            qcL = self.qcf[count]
            if qcL.startswith("$cdtex"):
                if qcL.find('\"./textures/\"') != -1:
                    cdTex = 1
                    checks += 1
                elif qcL.find('\".\"') != -1:
                    cdTex = 2
                    checks += 1
        if cdTex != 0:
            if cdTex == 1:
                count = -1
                texPath = os.path.join(self.qcLoc, "textures/")
                textures = os.listdir(texPath)
                while count < len(textures)-1:
                    count += 1
                    tex = textures[count]
                    fTex = os.path.join(self.qcLoc,tex)
                    texL = tex.lower()
                    print(tex)
                    if texL.find("chrome") != -1 and os.path.isfile(fTex):
                        try:
                            width, height = get_image_size.get_image_size(os.path.join(texPath,tex))
                        except get_image_size.UnknownImageFormat:
                            width, height = -1, -1
                        if not width == 64 or not height == 64:
                            self.fndUnlChr = True
            elif cdTex == 2:
                count = -1
                files = os.listdir(self.qcLoc)
                textures = []
                while count < len(files)-1:
                    count += 1
                    if files[count].endswith('.bmp'):
                        textures.append(files[count])
                count = -1
                while count < len(textures)-1:
                    count += 1
                    tex = textures[count]
                    fTex = os.path.join(self.qcLoc,tex)
                    texL = tex.lower()
                    print(tex)
                    if texL.find("chrome") != -1 and os.path.isfile(fTex):
                        try:
                            width, height = get_image_size.get_image_size(fTex)
                        except get_image_size.UnknownImageFormat:
                            width, height = -1, -1
                        if not width == 64 or not height == 64:
                            self.fndUnlChr = True
        return self.fndUnlChr
    def checkTRM(self, renderM:int):
        count = -1
        rm = renderM
        newCDtex = ""
        texmodes = []
        self.newQC = self.qcf
        self.newQCPath = ""
        self.fndTRM = False
        while count < len(self.qcf)-1:
            count += 1
            qcL = self.qcf[count]
            noNL = qcL.replace("\n", "")
            if qcL.startswith("$texrendermode"):
                if rm == 0 and noNL.endswith("fullbright") or rm == 0 and noNL.endswith('fullbright\"') or rm == 0 and noNL.endswith('fullbright\''):
                    self.fndTRM = True
                    print("FULLBRIGHT FLAG")
                elif rm == 1 and noNL.endswith("flatshade") or rm == 1 and noNL.endswith('flatshade\"') or rm == 0 and noNL.endswith('fullbright\''):
                    self.fndTRM = True
                    print("FLATSHADE FLAG")
                elif rm == 2 and noNL.endswith("chrome") or rm == 2 and noNL.endswith('chrome\"') or rm == 2 and noNL.endswith('chrome\''):
                    self.fndTRM = True
                    print("CHROME FLAG")
        return self.fndTRM

class HyperlinkImg():

    def __init__(self, master, image:PhotoImage, lID:int=0):
        self.link = Label(master, image=image, cursor="hand2")
        self.link.bind("<Button-1>", lambda e: self.openLink(lID))
    
    def grid(self, column=0, row=0, padx=0, pady=0, sticky=""):
        self.link.grid(column=column, row=row, padx=padx, pady=pady, sticky=sticky)
    
    def openLink(self, id):
        if id == 0:
            browser.open_new("https://github.com/PostScriptReal/Snark_Compiler")
        elif id == 1:
            browser.open_new("https://gamebanana.com/tools/19255")

class Game():

    def __init__(self, name, isCustom):
        self.name = name
        self.isCustom = isCustom

class GamesHandler():

    def __init__(self, gList):
        count = -1
        self.games = []
        self.gNames = []
        while count < len(gList)-1:
            count += 1
            g = gList[count]
            if g.endswith("~"):
                a = Game(g[:-1], True)
                self.games.append(a)
                self.gNames.append(g[:-1])
            else:
                a = Game(g, False)
                self.games.append(a)
                self.gNames.append(g)
    
    def checkCustom(self, name):
        count = -1
        while count < len(self.games)-1:
            count += 1
            g = self.games[count]
            if g.name == name and g.isCustom:
                return True
        return False
