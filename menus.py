from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import PhotoImage
from tktooltip import ToolTip
import os
from tkinter.filedialog import askopenfilename, askdirectory
import subprocess
import shutil
import datetime
from helpers import BoolEntry, Console, BoolSpinbox, QCHandler, HyperlinkImg
import json
import sys
import jsonc

class SetupMenu():
    def __init__(self, master, thme:dict, startHidden:bool=False):
        self.hidden = startHidden
        self.master = master
        self.thme = thme
        # Setting up options
        js = open("save/options.json", 'r')
        self.options = json.loads(js.read())
        js.close()
        gOptions = ["Half-Life", "Sven Co-op"]
        self.gameSel = ttk.Combobox(master, values=gOptions)
        self.gameSel.current(0)
        self.setupLabel = Label(master, text="Game Setup", background=thme["bg"], foreground=thme["txt"])
        self.nameLabel = Label(master, text="Name: ", background=thme["bg"], foreground=thme["txt"])
        self.name = StringVar()
        self.name.set(gOptions[0])
        self.nameEntry = Entry(master, textvariable=self.name, width=50)
        if not startHidden:
            self.gameSel.grid(column=1, row=2)
            self.setupLabel.grid(column=1, row=3, sticky=(W), padx=(10, 0))
            self.nameLabel.grid(column=1, row=4, sticky=(W))
            self.nameEntry.grid(column=2, row=4, sticky=(W))
        
        # Applying theme
        style=ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=self.thme["ent"])
        for w in master.winfo_children():
            if w.winfo_class() == "Button":
                w.configure(bg=self.thme["btn"][0])
                w.configure(highlightbackground=self.thme["btn"][1])
                w.configure(activebackground=self.thme["btn"][2])
                w.configure(fg=self.thme["txt"])
            elif w.winfo_class() == "Entry":
                w.configure(bg=self.thme["ent"])
                w.configure(fg=self.thme["txt"])
            elif isinstance(w, ttk.Combobox):
                pass
                w.configure(foreground='white')
                # w["menu"].config(bg=self.thme["btn"][1])
            elif isinstance(w, Text):
                w.configure(bg=self.thme["ent"])
                w.configure(fg=self.thme["txt"])
            elif w.winfo_class() == "Checkbutton":
                w.configure(bg=self.thme["bg"])
                w.configure(highlightbackground=self.thme["bg"])
                w.configure(activebackground=self.thme["bg"])
                w.configure(fg=self.thme["txt"])
                w.configure(selectcolor=self.thme["ent"])
            else:
                w.configure(bg=self.thme["bg"])
                try:
                    w.configure(fg=self.thme["txt"])
                except:
                    pass
    
    def changeTheme(self, newTheme):
        self.thme = newTheme
        style=ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=self.thme["ent"])
        for w in self.master.winfo_children():
            if w.winfo_class() == "Button":
                w.configure(bg=self.thme["btn"][0])
                w.configure(highlightbackground=self.thme["btn"][1])
                w.configure(activebackground=self.thme["btn"][2])
                w.configure(fg=self.thme["txt"])
            elif w.winfo_class() == "Entry":
                w.configure(bg=self.thme["ent"])
                w.configure(fg=self.thme["txt"])
            elif isinstance(w, ttk.Combobox):
                pass
                w.configure(foreground='white')
                # w["menu"].config(bg=self.thme["btn"][1])
            elif isinstance(w, Text):
                w.configure(bg=self.thme["ent"])
                w.configure(fg=self.thme["txt"])
            elif w.winfo_class() == "Checkbutton":
                w.configure(bg=self.thme["bg"])
                w.configure(highlightbackground=self.thme["bg"])
                w.configure(activebackground=self.thme["bg"])
                w.configure(fg=self.thme["txt"])
                w.configure(selectcolor=self.thme["ent"])
            else:
                w.configure(bg=self.thme["bg"])
                try:
                    w.configure(fg=self.thme["txt"])
                except:
                    pass
    
    def updateOpt(self, key, value):
        self.options[key] = value

    def hide(self):
        self.hidden = True
        for w in self.master.winfo_children():
            w.grid_remove()
    def show(self):
        self.hidden = False
        self.gameSel.grid(column=1, row=2)
        self.setupLabel.grid(column=1, row=3, sticky=(W), padx=(10, 0))
        self.nameLabel.grid(column=1, row=4, sticky=(W))
        self.nameEntry.grid(column=2, row=4, sticky=(W))

class CompSetupMenu():
    def __init__(self, master, thme:dict, startHidden:bool=False):
        self.hidden = startHidden
        self.master = master
        self.thme = thme
        self.hiddenEdit = True
        # Setting up options
        js = open("save/options.json", 'r')
        self.options = json.loads(js.read())
        js.close()
        js = open("save/compilers.jsonc", 'r')
        self.fullCJS = jsonc.load(js)
        self.fullCJS = self.fullCJS["compilers"]
        js.close()
        cOptions = ["GoldSRC", "Svengine"]
        self.selComp = "GoldSRC"
        self.gameSel = ttk.Combobox(master, values=cOptions)
        self.gameSel.current(0)
        self.gameSel.bind("<<ComboboxSelected>>", self.chComp)
        self.setupLabel = Label(master, text="Compiler Setup", background=thme["bg"], foreground=thme["txt"])
        self.nameLabel = Label(master, text="Name: ", background=thme["bg"], foreground=thme["txt"])
        self.pathLabel = Label(master, text="Custom path: ", background=thme["bg"], foreground=thme["txt"])
        self.name = StringVar()
        self.name.set(cOptions[0])
        self.nameEntry = Entry(master, textvariable=self.name, width=50)
        self.csPath = StringVar()
        self.csPath.set(self.fullCJS["GoldSRC"]["path"]["custom"])
        self.csPathEntry = Entry(master, textvariable=self.csPath, width=50)
        if not startHidden:
            self.gameSel.grid(column=1, row=2)
            self.setupLabel.grid(column=1, row=3, sticky=(W), padx=(10, 0))
            self.nameLabel.grid(column=1, row=4, sticky=(W))
            self.nameEntry.grid(column=2, row=4, sticky=(W))
        
        # Applying theme
        style=ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=self.thme["ent"])
        for w in master.winfo_children():
            if w.winfo_class() == "Button":
                w.configure(bg=self.thme["btn"][0])
                w.configure(highlightbackground=self.thme["btn"][1])
                w.configure(activebackground=self.thme["btn"][2])
                w.configure(fg=self.thme["txt"])
            elif w.winfo_class() == "Entry":
                w.configure(bg=self.thme["ent"])
                w.configure(fg=self.thme["txt"])
            elif isinstance(w, ttk.Combobox):
                pass
                w.configure(foreground='white')
                # w["menu"].config(bg=self.thme["btn"][1])
            elif isinstance(w, Text):
                w.configure(bg=self.thme["ent"])
                w.configure(fg=self.thme["txt"])
            elif w.winfo_class() == "Checkbutton":
                w.configure(bg=self.thme["bg"])
                w.configure(highlightbackground=self.thme["bg"])
                w.configure(activebackground=self.thme["bg"])
                w.configure(fg=self.thme["txt"])
                w.configure(selectcolor=self.thme["ent"])
            else:
                w.configure(bg=self.thme["bg"])
                try:
                    w.configure(fg=self.thme["txt"])
                except:
                    pass
    
    def changeTheme(self, newTheme):
        self.thme = newTheme
        style=ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=self.thme["ent"])
        for w in self.master.winfo_children():
            if w.winfo_class() == "Button":
                w.configure(bg=self.thme["btn"][0])
                w.configure(highlightbackground=self.thme["btn"][1])
                w.configure(activebackground=self.thme["btn"][2])
                w.configure(fg=self.thme["txt"])
            elif w.winfo_class() == "Entry":
                w.configure(bg=self.thme["ent"])
                w.configure(fg=self.thme["txt"])
            elif isinstance(w, ttk.Combobox):
                pass
                w.configure(foreground='white')
                # w["menu"].config(bg=self.thme["btn"][1])
            elif isinstance(w, Text):
                w.configure(bg=self.thme["ent"])
                w.configure(fg=self.thme["txt"])
            elif w.winfo_class() == "Checkbutton":
                w.configure(bg=self.thme["bg"])
                w.configure(highlightbackground=self.thme["bg"])
                w.configure(activebackground=self.thme["bg"])
                w.configure(fg=self.thme["txt"])
                w.configure(selectcolor=self.thme["ent"])
            else:
                w.configure(bg=self.thme["bg"])
                try:
                    w.configure(fg=self.thme["txt"])
                except:
                    pass
    
    def updateOpt(self, key, value):
        self.options[key] = value
    
    def chComp(self, e):
        self.selComp = self.gameSel.get()
        self.name.set(self.selComp)
        self.csPath.set(self.fullCJS[self.selComp]["path"]["custom"])
        # If editing options were removed and the compiler doesn't have editing disabled
        if self.hiddenEdit and not self.fullCJS[self.selComp]["disableEdit"]:
            self.hiddenEdit = False
            self.nameLabel.grid(column=1, row=4, sticky=(W))
            self.nameEntry.grid(column=2, row=4, sticky=(W))
            self.pathLabel.grid(column=1, row=5, sticky="w")
            self.csPathEntry.grid(column=2, row=5, sticky="w")
        # If editing options were available and the compiler has editing disabled
        elif not self.hiddenEdit and self.fullCJS[self.selComp]["disableEdit"]:
            self.hiddenEdit = True
            self.nameLabel.grid_remove()
            self.nameEntry.grid_remove()
            self.pathLabel.grid(column=1, row=4, sticky="w")
            self.csPathEntry.grid(column=2, row=4, sticky="w")

    def hide(self):
        self.hidden = True
        for w in self.master.winfo_children():
            w.grid_remove()
    def show(self):
        self.hidden = False
        self.gameSel.grid(column=1, row=2)
        self.setupLabel.grid(column=1, row=3, sticky=(W), padx=(10, 0))
        if not self.fullCJS[self.selComp]["disableEdit"]:
            self.hiddenEdit = False
            self.nameLabel.grid(column=1, row=4, sticky=(W))
            self.nameEntry.grid(column=2, row=4, sticky=(W))
            self.pathLabel.grid(column=1, row=5, sticky="w")
            self.csPathEntry.grid(column=2, row=5, sticky="w")
        else:
            self.hiddenEdit = True
            self.pathLabel.grid(column=1, row=4, sticky="w")
            self.csPathEntry.grid(column=2, row=4, sticky="w")

class DecompMenu():
    def __init__(self, master, thme:dict, startHidden:bool=False):
        self.curFont = font.nametofont('TkDefaultFont').actual()
        self.widthFix = 51
        self.conFix = 46
        self.logOutput = False
        if self.curFont["family"].lower() == "nimbus sans l":
            self.widthFix = 55
            self.conFix = 50
        else:
            pass
        self.hidden = startHidden
        self.master = master
        self.advOpt = Frame(master, borderwidth=2, bg=thme["bg"], relief="sunken")
        self.thme = thme
        # Setting up options
        js = open("save/options.json", 'r')
        self.options = json.loads(js.read())
        js.close()
        self.setupLabel = Label(master, text="MDL Input: ")
        self.nameLabel = Label(master, text="Output: ")
        self.name = StringVar()
        self.nameEntry = Entry(master, textvariable=self.name, width=self.widthFix)
        self.out = StringVar()
        self.outputEntry = Entry(master, textvariable=self.out, width=self.widthFix)
        self.mdlBrowse = Button(master, text='Browse', command=self.findMDL, cursor="hand2")
        self.outBrowse = Button(master, text='Browse', command=self.output, cursor="hand2")
        self.advOptLabel = Label(self.advOpt, text="Advanced Options")
        self.logVal = BooleanVar(self.advOpt, value=False)
        self.logChk = Checkbutton(self.advOpt, text="Write log to file", variable=self.logVal, command=self.setLog)
        self.logChkTT = ToolTip(self.logChk, "Writes the log in the terminal below as a text file inside the logs folder.", background=thme["tt"], foreground=thme["txt"])
        self.decomp = Button(master, text='Decompile', command=self.startDecomp, cursor="hand2")
        self.console = Console(master, 'Start a decompile and the terminal output will appear here!', 0, 4, self.conFix, 14)
        if not startHidden:
            self.setupLabel.grid(column=0, row=0, sticky=(W))
            self.nameLabel.grid(column=0, row=1, sticky=(W))
            self.nameEntry.grid(column=1, row=0)
            self.outputEntry.grid(column=1, row=1)
            self.mdlBrowse.grid(column=2, row=0, padx=(6,0))
            self.outBrowse.grid(column=2, row=1, padx=(6,0))
            self.advOpt.grid(column=0, row=2, sticky="nsew", columnspan=10, pady=(20,0))
            self.advOptLabel.grid(column=0, row=0, sticky="w")
            self.logChk.grid(column=0, row=1, sticky="w")
            self.decomp.grid(column=0, row=3, pady=(25,0))
            self.console.show()
        
        self.mdlTT = ToolTip(self.mdlBrowse, "REQUIRED, specifies the MDL file used to decompile a model, you cannot leave this blank.", background=thme["tt"], foreground=thme["txt"])
        self.outputTT = ToolTip(self.outBrowse, "REQUIRED, you must specify an output folder to place all files into.", background=thme["tt"], foreground=thme["txt"])
        
        # Applying theme
        self.applyTheme(master)
        self.applyTheme(self.advOpt)
    def setLog(self):
        self.logOutput = self.logVal.get()

    def applyTheme(self, master):
        style= ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=self.thme["ent"])
        for w in master.winfo_children():
            if w.winfo_class() == "Button":
                w.configure(bg=self.thme["btn"][0])
                w.configure(highlightbackground=self.thme["btn"][1])
                w.configure(activebackground=self.thme["btn"][2])
                w.configure(fg=self.thme["txt"])
            elif w.winfo_class() == "Entry":
                w.configure(bg=self.thme["ent"])
                w.configure(fg=self.thme["txt"])
            elif isinstance(w, ttk.Combobox):
                pass
                w.configure(foreground='white')
                # w["menu"].config(bg=self.thme["btn"][1])
            elif isinstance(w, Text):
                w.configure(bg=self.thme["ent"])
                w.configure(fg=self.thme["txt"])
            elif w.winfo_class() == "Checkbutton":
                w.configure(bg=self.thme["bg"])
                w.configure(highlightbackground=self.thme["bg"])
                w.configure(activebackground=self.thme["bg"])
                w.configure(fg=self.thme["txt"])
                w.configure(selectcolor=self.thme["ent"])
            else:
                w.configure(bg=self.thme["bg"])
                try:
                    w.configure(fg=self.thme["txt"])
                except:
                    pass
    
    def changeTheme(self, newTheme):
        self.thme = newTheme
        self.applyTheme(self.master)
        self.applyTheme(self.advOpt)
        self.mdlTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.outputTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.logChkTT.changeTheme(newTheme["tt"], newTheme["txt"])
    
    def updateOpt(self, key, value):
        self.options[key] = value

    def hide(self):
        self.hidden = True
        for w in self.master.winfo_children():
            w.grid_remove()
    
    def show(self):
        self.hidden = False
        self.setupLabel.grid(column=0, row=0, sticky=(W))
        self.nameLabel.grid(column=0, row=1, sticky=(W))
        self.nameEntry.grid(column=1, row=0, padx=(5,0))
        self.outputEntry.grid(column=1, row=1, padx=(5,0))
        self.mdlBrowse.grid(column=2, row=0, padx=(12,0))
        self.outBrowse.grid(column=2, row=1, padx=(12,0))
        self.advOpt.grid(column=0, row=2, sticky="nsew", columnspan=10, pady=(20,0))
        self.advOptLabel.grid(column=0, row=0, sticky="w")
        self.logChk.grid(column=0, row=1, sticky="w")
        self.decomp.grid(column=0, row=3, pady=(27,0))
        self.console.show()
    
    def findMDL(self):
        startDir = self.options["startFolder"]
        if startDir.startswith("~"):
            startDir = os.path.expanduser(startDir)
        fileTypes = [("GoldSRC Model", "*.mdl"), ("All Files", "*.*")]
        self.name.set(askopenfilename(title="Select MDL", initialdir=startDir, filetypes=fileTypes))
    def output(self):
        startDir = self.options["startFolder"]
        if startDir.startswith("~"):
            startDir = os.path.expanduser(startDir)
        self.out.set(askdirectory(title="Select Output Folder", initialdir=startDir))
    
    def startDecomp(self):
        mdl = self.name.get()
        output = self.out.get()
        tOutput = ''
        if sys.platform == 'linux':
            tOutput = subprocess.getoutput(f'./third_party/mdldec \"{mdl}\"')
        elif sys.platform == 'win32':
            tOutput = subprocess.getoutput(f'third_party/mdldec_win32.exe \"{mdl}\"')
        # I don't have a Mac so I can't compile mdldec to Mac targets :(
        # So instead I have to use wine for Mac systems
        elif sys.platform == 'darwin':
            tOutput = subprocess.getoutput(f'wine third_party/mdldec_win32.exe \"{mdl}\"')
        print(tOutput)
        self.console.setOutput(tOutput)
        if self.logOutput:
            date = datetime.datetime.now()
            curDate = f"{date.strftime('%d')}-{date.strftime('%m')}-{date.strftime('%Y')}-{date.strftime('%H')}-{date.strftime('%M')}-{date.strftime('%S')}"
            log = open(f"logs/decomp-{curDate}.txt", 'w')
            log.write(tOutput)
            log.close()
        # Moving files to output directory (this is a workaround to a bug with Xash3D's model decompiler)
        filesToMove = []
        mdlFolder = os.path.dirname(mdl)
        anims = os.path.join(mdlFolder, 'anims/')
        texFolder = os.path.join(mdlFolder, 'textures/')
        for f in os.listdir(mdlFolder):
            print(f)
            if f.endswith("smd") or f.endswith("qc"):
                shutil.copy(f"{mdlFolder}/{f}", os.path.join(output, f))
                os.remove(f"{mdlFolder}/{f}")
        shutil.copytree(anims, os.path.join(output, 'anims/'))
        shutil.copytree(texFolder, os.path.join(output, 'textures/'))
        try:
            shutil.rmtree(anims)
        except:
            pass
        try:
            shutil.rmtree(texFolder)
        except:
            pass

class CompMenu():
    def __init__(self, master, thme:dict, startHidden:bool=False):
        self.curFont = font.nametofont('TkDefaultFont').actual()
        self.widthFix = 52
        self.conFix = 47
        self.advOptFix = True
        if self.curFont["family"].lower() == "nimbus sans l":
            self.widthFix = 55
            self.conFix = 50
            self.advOptFix = False
        else:
            pass
        self.hidden = startHidden
        self.master = master
        self.svengine = False
        self.logOutput = False
        # Setting up JSON stuff
        js = open("save/compilers.jsonc", 'r')
        self.fullCJS = jsonc.load(js)
        js.close()
        js = open("save/profiles.json", 'r')
        self.profiles = json.loads(js.read())
        js.close()
        js = open("save/options.json", 'r')
        self.options = json.loads(js.read())
        js.close()
        self.selects = Frame(master, borderwidth=2, bg=thme["bg"])
        self.advOpt = Frame(master, borderwidth=2, bg=thme["bg"], relief="sunken")
        self.thme = thme
        self.setupLabel = Label(master, text="QC Input: ")
        self.nameLabel = Label(master, text="Output: ")
        self.name = StringVar()
        self.nameEntry = Entry(master, textvariable=self.name, width=self.widthFix)
        self.out = StringVar()
        self.outputEntry = Entry(master, textvariable=self.out, width=self.widthFix)
        self.mdlBrowse = Button(master, text='Browse', command=self.findMDL, cursor="hand2")
        self.mdlBrowse.bind("<FocusOut>", self.inputHandler)
        self.outBrowse = Button(master, text='Browse', command=self.output, cursor="hand2")
        self.compLabel = Label(self.selects, text="Compiler: ")
        cList = open("save/compilers.txt", "r")
        cOptions = cList.read().split('\n')
        cOptions.pop(len(cOptions)-1)
        self.compSel = ttk.Combobox(self.selects, values=cOptions, width=8)
        self.compSel.current(0)
        self.compSel.bind("<<ComboboxSelected>>", self.compilerStuff)
        self.gameLabel = Label(self.selects, text="Game Profile: ")
        gList = open("save/games.txt", "r")
        gOptions = gList.read().split('\n')
        gOptions.pop(len(gOptions)-1)
        self.gameSel = ttk.Combobox(self.selects, values=gOptions, width=10)
        self.gameSel.current(0)
        self.gameSel.bind("<<ComboboxSelected>>", self.compatChk)


        # Advanced Options
        # All options for Half-Life's StudioMDL can be found here https://github.com/ValveSoftware/halflife/blob/master/utils/studiomdl/studiomdl.c at line 3362-3408
        # Note that the Half-Life SDK doesn't document every command available to the compiler
        # Some information for other GoldSRC compilers can be found here: https://developer.valvesoftware.com/wiki/StudioMDL_(GoldSrc)
        """ Commands that have yet to be implemented into the GUI:
                -n - Tags bad normals (IMPLEMENTED!)
                -f - Flips all triangles (IMPLEMENTED!)
                -i - Ignore warnings (IMPLEMENTED!)
                -p - Force power of 2 textures (Unavailable in Sven Co-op StudioMDL)
                -g - Sets the maximum group size for sequences in KB (IMPLEMENTED)
        """
        self.advOptLabel = Label(self.advOpt, text="Advanced Options")
        self.logVal = BooleanVar(self.advOpt, value=False)
        self.logChk = Checkbutton(self.advOpt, text="Write log to file", variable=self.logVal, command=self.setLog)
        self.dashTvar = StringVar(self.advOpt, value="<texture.bmp>")
        self.dashTbool = BooleanVar(self.advOpt, value=False)
        self.dashTChk = Checkbutton(self.advOpt, text="-t", variable=self.dashTbool, command=self.dashThandler)
        self.dashT = BoolEntry(self.advOpt, textvariable=self.dashTvar, placeholder="<texture.bmp>")
        self.rNormalB = BooleanVar(self.advOpt, value=False)
        self.rNormalChk = Checkbutton(self.advOpt, text="-r", variable=self.rNormalB)
        self.angleB = BooleanVar(self.advOpt, value=False)
        self.angleChk = Checkbutton(self.advOpt, text="-a", variable=self.angleB, command=self.angleSBhandler)
        self.angleSB = BoolSpinbox(self.advOpt, range=[0,360], bg=thme["ent"], bBG=thme["btn"][0], fg=thme["txt"])
        self.hitboxB = BooleanVar(self.advOpt, value=False)
        self.hitboxChk = Checkbutton(self.advOpt, text="-h", variable=self.hitboxB)
        self.keepBonesB = BooleanVar(self.advOpt, value=False)
        self.keepBonesChk = Checkbutton(self.advOpt, text="-k", variable=self.keepBonesB)
        self.ignoreB = BooleanVar(self.advOpt, value=False)
        self.ignoreChk = Checkbutton(self.advOpt, text="-i", variable=self.ignoreB)
        self.bNormB = BooleanVar(self.advOpt, value=False)
        self.bNormChk = Checkbutton(self.advOpt, text="-n", variable=self.bNormB)
        self.flipB = BooleanVar(self.advOpt, value=False)
        self.flipChk = Checkbutton(self.advOpt, text="-f", variable=self.flipB)
        self.groupB = BooleanVar(self.advOpt, value=False)
        self.groupChk = Checkbutton(self.advOpt, text="-g", variable=self.groupB, command=self.groupSBhandler)
        self.groupSB = BoolSpinbox(self.advOpt, range=[0,4096], bg=thme["ent"], bBG=thme["btn"][0], fg=thme["txt"], increment=16)
        self.groupSB.entry.config(width=4)
        self.pf2B = BooleanVar(self.advOpt, value=False)
        self.pf2Chk = Checkbutton(self.advOpt, text="-p", variable=self.pf2B)
        # Tooltips
        self.logChkTT = ToolTip(self.logChk, "Writes the log in the terminal below as a text file inside the logs folder.", background=thme["tt"], foreground=thme["txt"])
        self.dashTChkTT = ToolTip(self.dashTChk, "Specify a texture to replace while compiling, you can globally replace all textures by specifying one bitmap or replace a single texture by following this format: \'tex1.bmp,tex2.bmp\'.", background=thme["tt"], foreground=thme["txt"])
        self.rNormalTT = ToolTip(self.rNormalChk, "Tags flipped normals in the console when enabled, useful for finding issues with backface culling.", background=thme["tt"], foreground=thme["txt"])
        self.angleSBtt = ToolTip(self.angleChk, "Overrides the blend angle of vertex normals, Valve recommends keeping this value at 2 (the default) according to the HLSDK docs.", background=thme["tt"], foreground=thme["txt"])
        self.angleChkTT = ToolTip(self.hitboxChk, "Dumps hitbox information to the console when enabled.", background=thme["tt"], foreground=thme["txt"])
        self.keepBonesChkTT = ToolTip(self.keepBonesChk, "Tells the compiler to keep all bones, including unweighted bones.", background=thme["tt"], foreground=thme["txt"])
        self.ignoreChkTT = ToolTip(self.ignoreChk, "Tells the compiler to ignore all warnings, useful for if you want to quickly test a model that isn't complete yet.", background=thme["tt"], foreground=thme["txt"])
        self.bNormChkTT = ToolTip(self.bNormChk, "Tags bad normals in the console.", background=thme["tt"], foreground=thme["txt"])
        self.flipChkTT = ToolTip(self.flipChk, "Tells the compiler to flip all triangles in the model.", background=thme["tt"], foreground=thme["txt"])
        self.groupChkTT = ToolTip(self.groupChk, "Sets the maximum group size for sequences in KB", background=thme["tt"], foreground=thme["txt"])
        self.pf2ChkTT = ToolTip(self.pf2Chk, "Forces power of 2 textures when enabled", background=thme["tt"], foreground=thme["txt"])
        self.mdlTT = ToolTip(self.mdlBrowse, "REQUIRED, specifies the QC file used to compile your model, you cannot leave this blank.", background=thme["tt"], foreground=thme["txt"])
        self.outputTT = ToolTip(self.outBrowse, "OPTIONAL, if an output folder is not specified, then it will place the compiled model in a models subfolder of where the QC file is located.", background=thme["tt"], foreground=thme["txt"])
        
        self.decomp = Button(master, text='Compile', command=self.startCompile, cursor="hand2")
        self.console = Console(master, 'Currently no warnings or errors!', 0, 5, self.conFix, 12)
        if not startHidden:
            self.setupLabel.grid(column=0, row=0, sticky=(W))
            self.nameLabel.grid(column=0, row=1, sticky=(W))
            self.nameEntry.grid(column=1, row=0)
            self.outputEntry.grid(column=1, row=1)
            self.mdlBrowse.grid(column=2, row=0, padx=(6,0))
            self.outBrowse.grid(column=2, row=1, padx=(6,0))
            self.advOpt.grid(column=0, row=2, sticky="nsew", columnspan=10, pady=(20,0))
            self.advOptLabel.grid(column=0, row=0, sticky="w")
            self.logChk.grid(column=0, row=1, sticky="w")
            self.decomp.grid(column=0, row=3, pady=(40,0))
            self.console.show()
        
        # Applying theme
        self.applyTheme(master)
        self.applyTheme(self.advOpt)
        self.applyTheme(self.selects)
        self.angleSB.changeTheme(thme["ent"], thme["btn"][0], thme["txt"])
        self.groupSB.changeTheme(thme["ent"], thme["btn"][0], thme["txt"])
    def setLog(self):
        self.logOutput = self.logVal.get()
    
    def inputHandler(self):
        print("Entry Lost Focus")
        self.name.set(self.nameEntry.get())
        self.compatChk()
    
    def dashThandler(self):
        if self.dashTbool.get():
            self.dashT.unlock()
        else:
            self.dashT.lock()
    
    def angleSBhandler(self):
        if self.angleB.get():
            self.angleSB.unlock()
        else:
            self.angleSB.lock()
    
    def groupSBhandler(self):
        if self.groupB.get():
            self.groupSB.unlock()
        else:
            self.groupSB.lock()
    
    def compilerStuff(self, event):
        self.compJS = self.fullCJS["compilers"][self.compSel.get()]
        if self.compJS["type"].lower() == "svengine":
            self.svengine = True
            self.keepBonesChk.grid(column=1, row=2, sticky="w")
            self.pf2Chk.grid_remove()
        else:
            self.svengine = False
            self.keepBonesChk.grid_remove()
            self.pf2Chk.grid(column=1, row=2, sticky="w")
        self.compatChk()

    def applyTheme(self, master):
        style= ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=self.thme["ent"])
        for w in master.winfo_children():
            if w.winfo_class() == "Button":
                w.configure(bg=self.thme["btn"][0])
                w.configure(highlightbackground=self.thme["btn"][1])
                w.configure(activebackground=self.thme["btn"][2])
                w.configure(fg=self.thme["txt"])
            elif w.winfo_class() == "Entry":
                w.configure(bg=self.thme["ent"])
                w.configure(fg=self.thme["txt"])
            elif isinstance(w, ttk.Combobox):
                pass
                w.configure(foreground='white')
                # w["menu"].config(bg=self.thme["btn"][1])
            elif isinstance(w, Text):
                w.configure(bg=self.thme["ent"])
                w.configure(fg=self.thme["txt"])
            elif w.winfo_class() == "Checkbutton":
                w.configure(bg=self.thme["bg"])
                w.configure(highlightbackground=self.thme["bg"])
                w.configure(activebackground=self.thme["bg"])
                w.configure(fg=self.thme["txt"])
                w.configure(selectcolor=self.thme["ent"])
            else:
                w.configure(bg=self.thme["bg"])
                try:
                    w.configure(fg=self.thme["txt"])
                except:
                    pass
    
    def changeTheme(self, newTheme):
        self.thme = newTheme
        self.applyTheme(self.master)
        self.applyTheme(self.advOpt)
        self.applyTheme(self.selects)
        self.logChkTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.dashTChkTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.rNormalTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.angleSBtt.changeTheme(newTheme["tt"], newTheme["txt"])
        self.angleChkTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.keepBonesChkTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.ignoreChkTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.bNormChkTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.flipChkTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.groupChkTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.pf2ChkTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.mdlTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.outputTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.angleSB.changeTheme(newTheme["ent"], newTheme["btn"][0], newTheme["txt"])
        self.groupSB.changeTheme(newTheme["ent"], newTheme["btn"][0], newTheme["txt"])

    def updateOpt(self, key, value):
        self.options[key] = value
    
    def hide(self):
        self.hidden = True
        for w in self.master.winfo_children():
            w.grid_remove()
    
    def show(self):
        self.hidden = False
        self.setupLabel.grid(column=0, row=0, sticky=(W))
        self.nameLabel.grid(column=0, row=1, sticky=(W))
        self.nameEntry.grid(column=1, row=0, padx=(18, 0))
        self.outputEntry.grid(column=1, row=1, padx=(18,0))
        self.mdlBrowse.grid(column=2, row=0, padx=(7,0))
        self.outBrowse.grid(column=2, row=1, padx=(7,0))
        self.selects.grid(column=0, row=2, sticky="nsew", columnspan=10)
        self.compLabel.grid(column=0, row=0)
        self.compSel.grid(column=1, row=0, padx=(0,10))
        self.gameLabel.grid(column=2, row=0)
        self.gameSel.grid(column=3, row=0)
        self.advOpt.grid(column=0, row=3, sticky="nsew", columnspan=10, pady=(20,0))
        self.advOptLabel.grid(column=0, row=0, sticky="w")
        self.logChk.grid(column=0, row=1, sticky="w")
        self.dashT.grid(column=2, row=1, sticky="w")
        self.dashTChk.grid(column=1, row=1, sticky="w")
        self.rNormalChk.grid(column=3, row=1, sticky="w")
        self.angleChk.grid(column=4, row=1, sticky="w")
        self.angleSB.grid(column=5, row=1, sticky="w")
        self.hitboxChk.grid(column=6, row=1, sticky="w")
        self.ignoreChk.grid(column=7, row=1, sticky="w")
        self.bNormChk.grid(column=8, row=1, sticky="w")
        if not self.advOptFix:
            self.flipChk.grid(column=9, row=1, sticky="w")
        else:
            self.flipChk.grid(column=0, row=2, sticky="w")
        if not self.advOptFix:
            self.groupChk.grid(column=0, row=2, sticky="w")
            self.groupSB.grid(column=0, row=2, sticky="w",padx=(40,0))
        else:
            self.groupChk.grid(column=0, row=2, sticky="w",padx=(40,0))
            self.groupSB.grid(column=0, row=2, sticky="w",padx=(81,0))
        if not self.svengine:
            self.pf2Chk.grid(column=1, row=2, sticky="w")
        if self.svengine:
            self.keepBonesChk.grid(column=1, row=2, sticky="w")
        self.decomp.grid(column=0, row=4, pady=(10,0))
        self.console.show()
    
    def findMDL(self):
        startDir = self.options["startFolder"]
        if startDir.startswith("~"):
            startDir = os.path.expanduser(startDir)
        fileTypes = [("Quake Compile Files", "*.qc"), ("All Files", "*.*")]
        self.name.set(askopenfilename(title="Select QC", initialdir=startDir, filetypes=fileTypes))
        self.compatChk()
    
    def compatChk(self, e=False):
        if not self.name.get() == "":
            handler = QCHandler(self.name.get())
            gameDat = self.profiles["profiles"][self.gameSel.get()]
            compDat = self.fullCJS["compilers"][self.compSel.get()]
            warnings = []
            if compDat["capabilities"]["1024px"]:
                # If the game doesn't support higher resolution textures, then give a warning in the console
                if not gameDat["capabilities"]["1024px"] and handler.check1024px():
                    warnings.append("WARNING: The selected game does not support textures higher than 512x512, please downscale the offending textures!")
            else:
                if handler.check1024px() and gameDat["capabilities"]["unlockedChrome"]:
                    warnings.append("WARNING: The selected compiler does not support textures higher than 512x512, please downscale the offending textures!")
                elif handler.check1024px():
                    warnings.append("WARNING: The selected compiler and game does not support textures higher than 512x512, please downscale the offending textures!")
            if compDat["capabilities"]["unlockedChrome"]:
                # If the game doesn't support chrome textures that aren't 64x64, then give a warning in the console
                if not gameDat["capabilities"]["unlockedChrome"] and handler.checkCHROME():
                    warnings.append("WARNING: There are one or more chrome textures that aren't at a fixed resolution of 64x64, please fix that as the selected game does not support this!")
            else:
                if handler.checkCHROME() and gameDat["capabilities"]["unlockedChrome"]:
                    warnings.append("WARNING: There are one or more chrome textures that aren't at a fixed resolution of 64x64, please fix that as the selected compiler does not support this!")
                elif handler.checkCHROME():
                    warnings.append("WARNING: There are one or more chrome textures that aren't at a fixed resolution of 64x64, please fix that as the selected compiler and game does not support this!")
            # Update the console
            if len(warnings) != 0:
                self.console.setOutput("\n".join(warnings))
            else:
                self.console.setOutput('Currently no warnings or errors!')

    def output(self):
        startDir = self.options["startFolder"]
        if startDir.startswith("~"):
            startDir = os.path.expanduser(startDir)
        self.out.set(askdirectory(title="Select Output Folder", initialdir=startDir))
    
    def getCompilerOptions(self):
        self.boolVars = []
        conVars = []
        # Setting up the variables in lists for easy checking
        if self.svengine:
            self.boolVars = [self.dashTbool.get(),self.rNormalB.get(),self.bNormB.get(),
            self.flipB.get(),self.angleB.get(),self.hitboxB.get(),self.ignoreB.get(),self.keepBonesB.get(),self.groupB.get()]
            conVars = ["-t", "-r", "-n", "-f", "-a", "-h", "-i", "-k", "-g"]
        else:
            self.boolVars = [self.dashTbool.get(),self.rNormalB.get(),self.bNormB.get(),
            self.flipB.get(),self.angleB.get(),self.hitboxB.get(),self.ignoreB.get(),self.pf2B.get(),self.groupB.get()]
            conVars = ["-t", "-r", "-n", "-f", "-a", "-h", "-i", "-p", "-g"]
        optionEn = False
        # Using the index method so that I can check if any of these options are enabled.
        # If it gives an error, that means that none of the options are enabled.
        try:
            self.boolVars.index(True)
            optionEn = True
        except:
            pass
        oID = -1
        self.para = []
        if optionEn:
            # Using a while loop as it is faster than a for loop
            while oID < len(self.boolVars)-1:
                oID += 1
                print(oID)
                if self.boolVars[oID]:
                    if conVars[oID] == "-t":
                        uInput = self.dashTvar.get()
                        uInput = uInput.split(',', 1)
                        if len(uInput) == 1:
                            self.para.append(f"-t {uInput[0]}")
                        else:
                            self.para.append(f"-t {uInput[0]} {uInput[1]}")
                    elif conVars[oID] == "-a" or conVars[oID] == "-g":
                        uInput = None
                        if conVars[oID] == "-a":
                            uInput = str(self.angleSB.get())
                        else:
                            uInput = str(self.groupSB.get())
                        self.para.append(f"{conVars[oID]} {uInput}")
                    else:
                        self.para.append(f"{conVars[oID]}")
        if optionEn:
            print("Found parameters!")
            paraStr = ' '.join(self.para)
            print(paraStr)
            return paraStr
        else:
            print("No paramaters found!")
            return None

    def startCompile(self):
        mdl = self.name.get()
        output = self.out.get()
        tOutput = ''
        compilerPath = ''
        compilerFound = False
        forceDefault = self.options["forceDefPaths"]
        try:
            if forceDefault:
                paths = self.compJS["path"]["default"][sys.platform]
                for p in paths:
                    if os.path.exists(os.path.expanduser(p)):
                        print(p)
                        compilerPath = os.path.expanduser(p)
                        compilerFound = True
                        break
                if not compilerFound:
                    paths = self.compJS["path"]["custom"]
                    if os.path.exists(paths):
                        compilerPath = paths
                        compilerFound = True
            else:
                paths = self.compJS["path"]["custom"]
                if not paths == "":
                    if os.path.exists(paths):
                        compilerPath = paths
                        compilerFound = True
                else:
                    paths = self.compJS["path"]["default"][sys.platform]
                    for p in paths:
                        if os.path.exists(os.path.expanduser(p)):
                            print(p)
                            compilerPath = os.path.expanduser(p)
                            compilerFound = True
                            break
        except:
            self.console.setOutput("ERROR: Couldn't find compiler, have you selected one?")
            return
        # Getting advanced options the user has enabled and turning that into a string that can be used with StudioMDL
        cOpts = self.getCompilerOptions()
        # Checking if the QC file supplied uses relative pathing for $cd and $cdtexture as the compiler cannot find the files otherwise
        qcRelChk = QCHandler(mdl)
        qcRelChk.crowbarFormatCheck()
        if qcRelChk.cbarFrmt:
            mdl = qcRelChk.newQCPath

        if sys.platform == 'linux' and compilerFound:
            # I will check if it is a native executable anyway for future proofing
            # Pretty much all StudioMDL compilers are windows executables only
            if compilerPath.endswith(".exe"):
                if cOpts == None:
                    print(f'wine \"{compilerPath}\" \"{mdl}\"')
                    tOutput = subprocess.getoutput(f'wine \"{compilerPath}\" \"{mdl}\"')
                else:
                    print(f'wine \"{compilerPath}\" {cOpts} \"{mdl}\"')
                    tOutput = subprocess.getoutput(f'wine \"{compilerPath}\" {cOpts} \"{mdl}\"')
            else:
                if cOpts == None:
                    tOutput = subprocess.getoutput(f'\"{compilerPath}\" \"{mdl}\"')
                else:
                    tOutput = subprocess.getoutput(f'\"{compilerPath}\" {cOpts} \"{mdl}\"')
        elif sys.platform == 'win32' and compilerFound:
            if cOpts == None:
                tOutput = subprocess.getoutput(f'\"{compilerPath}\" \"{mdl}\"')
            else:
                tOutput = subprocess.getoutput(f'\"{compilerPath}\" {cOpts} \"{mdl}\"')
        else:
            self.console.setOutput("ERROR: Couldn't find compiler, have you installed it?")
        # I don't have a Mac so I can't compile mdldec to Mac targets :(
        # So instead I have to use wine for Mac systems
        """elif sys.platform == 'darwin':
            tOutput = subprocess.getoutput(f'wine third_party/mdldec_win32.exe \"{mdl}\"')"""
        if compilerFound:
            print(tOutput)
            self.console.setOutput(tOutput)
            # Removing temporary QC file used to compile model when the QC file supplied had used relative pathing
            if qcRelChk.cbarFrmt:
                os.remove(mdl)
            if self.logOutput:
                date = datetime.datetime.now()
                curDate = f"{date.strftime('%d')}-{date.strftime('%m')}-{date.strftime('%Y')}-{date.strftime('%H')}-{date.strftime('%M')}-{date.strftime('%S')}"
                log = open(f"logs/compile-{curDate}.txt", 'w')
                log.write(tOutput)
                log.close()
            # Moving the compiled MDL file to the output folder
            mdlFolder = ""
            if output == "" or output == None:
                mdlFolder = qcRelChk.qcLoc
                mdlFolder = os.path.join(mdlFolder, "models/")
            else:
                mdlFolder = output
            mdlF = qcRelChk.getMDLname()
            shutil.copy(mdlF, os.path.join(mdlFolder, mdlF))
            os.remove(mdlF)

class AboutMenu():
    def __init__(self, master, thme:dict, startHidden:bool=False):
        self.hidden = startHidden
        self.master = master
        self.thme = thme
        # Setting up options
        js = open("save/options.json", 'r')
        self.options = json.loads(js.read())
        js.close()
        # Images
        self.snarkLogoPNG = PhotoImage(file="logo128.png")
        self.gitLogoPNG = PhotoImage(file="images/github.png")
        self.gbLogoPNG = PhotoImage(file="images/gamebanana.png")
        # Labels displaying the images
        self.snarkLogo = Label(master, image=self.snarkLogoPNG)
        self.githubLogo = HyperlinkImg(master, image=self.gitLogoPNG, lID=0)
        self.gameBLogo = HyperlinkImg(master, image=self.gbLogoPNG, lID=1)
        # Text
        vnum = open('version.txt', "r")
        self.ver = vnum.read().replace("(OS)", sys.platform)
        self.setupLabel = Label(master, text=f"Snark {self.ver} by:", background=thme["bg"], foreground=thme["txt"])
        credits = ["PostScript", "\nusing:", "MDLDec by Flying With Gauss", "get_image_size by Paulo Scardine", "TkTooltip by DaedalicEntertainment"]
        self.nameLabel = Label(master, text="\n".join(credits), background=thme["bg"], fg=thme["txt"])
        # Tooltips
        self.githubTT = ToolTip(self.githubLogo.link, "Source Code and Releases on Github", background=thme["tt"], foreground=thme["txt"])
        self.gameBtt = ToolTip(self.gameBLogo.link, "Official Download page on Gamebanana", background=thme["tt"], foreground=thme["txt"])
        if not startHidden:
            self.snarkLogo.grid(column=1,row=0)
            self.setupLabel.grid(column=1, row=1)
            self.nameLabel.grid(column=1, row=2)
        
        # Applying theme
        self.applyTheme(master)
    
    def applyTheme(self, master):
        style= ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=self.thme["ent"])
        for w in master.winfo_children():
            if w.winfo_class() == "Button":
                w.configure(bg=self.thme["btn"][0])
                w.configure(highlightbackground=self.thme["btn"][1])
                w.configure(activebackground=self.thme["btn"][2])
                w.configure(fg=self.thme["txt"])
            elif w.winfo_class() == "Entry":
                w.configure(bg=self.thme["ent"])
                w.configure(fg=self.thme["txt"])
            elif isinstance(w, ttk.Combobox):
                pass
                w.configure(foreground='white')
                # w["menu"].config(bg=self.thme["btn"][1])
            elif isinstance(w, Text):
                w.configure(bg=self.thme["ent"])
                w.configure(fg=self.thme["txt"])
            elif w.winfo_class() == "Checkbutton":
                w.configure(bg=self.thme["bg"])
                w.configure(highlightbackground=self.thme["bg"])
                w.configure(activebackground=self.thme["bg"])
                w.configure(fg=self.thme["txt"])
                w.configure(selectcolor=self.thme["ent"])
            else:
                w.configure(bg=self.thme["bg"])
                try:
                    w.configure(fg=self.thme["txt"])
                except:
                    pass
    
    def changeTheme(self, newTheme):
        self.thme = newTheme
        self.applyTheme(self.master)
        self.githubTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.gameBtt.changeTheme(newTheme["tt"], newTheme["txt"])

    def updateOpt(self, key, value):
        self.options[key] = value
    
    def hide(self):
        self.hidden = True
        for w in self.master.winfo_children():
            w.grid_remove()
    def show(self):
        self.hidden = False
        self.snarkLogo.grid(column=1, row=0)
        self.githubLogo.grid(column=1,row=1, padx=(0,50))
        self.gameBLogo.grid(column=1,row=1, padx=(50,0))
        self.setupLabel.grid(column=1, row=2)
        self.nameLabel.grid(column=1, row=3)

class OptionsMenu():
    def __init__(self, master, thme:dict, thmecallback, updFunc, startHidden:bool=False):
        self.hidden = startHidden
        self.master = master
        self.thme = thme
        self.updFunc = updFunc
        # Grabbing options
        jsf = open('save/options.json', 'r')
        js = jsf.read()
        jsf.close()
        self.options = json.loads(js)
        # Options
        self.setupLabel = Label(master, text=f"Theme: ", background=thme["bg"], foreground=thme["txt"])
        self.nameLabel = Label(master, text="Starting directory: ", background=thme["bg"], fg=thme["txt"])
        themes = ["Freeman", "Shephard", "Calhoun", "Cross"]
        usrThemes = self.checkNewThemes()
        if not usrThemes == False:
            count = -1
            while count < len(usrThemes)-1:
                count += 1
                t = usrThemes[count]
                if t.endswith('json'):
                    themes.append(t.replace(".json", ""))
                elif t.endswith('jsonc'):
                    themes.append(t.replace(".jsonc", ""))
        self.themeCBox = ttk.Combobox(master, cursor="hand2", values=themes)
        self.themeCBox.bind("<<ComboboxSelected>>", thmecallback)
        self.themeCBox.set(self.options["theme"])
        self.startFSV = StringVar(master, value=self.options["startFolder"])
        # I just realised I shortened the name so it looks like it's name is Start Fent.
        # I promise you there is no illicit drugs to be found anywhere in the program lol.
        self.startFent = Entry(master, textvariable=self.startFSV)
        self.setSF = Button(master, text="Set Start Folder", cursor="hand2", command=self.chSF)
        self.forceDefB = BooleanVar(master, value=self.options["forceDefPaths"])
        self.fdLabel = Label(master, text="Prioritise default paths:")
        self.forceDefault = Checkbutton(master, command=self.chFDP, variable=self.forceDefB)
        # Tooltips
        self.themeTT = ToolTip(self.themeCBox, "Changes the program's theme, the built-in themes are: Freeman, Shephard, Calhoun and Cross.", background=thme["tt"], foreground=thme["txt"])
        self.startFolderTT = ToolTip(self.startFent, "Sets the directory that the built-in file explorer will start in, the default is the documents folder.", background=thme["tt"], foreground=thme["txt"])
        self.startFolderTT2 = ToolTip(self.setSF, "Sets the directory that the built-in file explorer will start in, the default is the documents folder.", background=thme["tt"], foreground=thme["txt"])
        self.forceDefTT = ToolTip(self.forceDefault, "By default, Snark prioritises the custom path you set over the default paths for compilers, enabling this will prioritise the default paths instead, meaning that Snark won't use the custom path if it finds the compiler in its default path.", background=thme["tt"], foreground=thme["txt"])
        if not startHidden:
            self.setupLabel.grid(column=1, row=1)
            self.nameLabel.grid(column=1, row=2)
        
        # Applying theme
        self.applyTheme(master)
    
    def checkNewThemes(self):
        tList = os.listdir("themes/")
        tList.remove("template.jsonc")
        if len(tList) >= 1:
            return tList
        return False
    
    def applyTheme(self, master):
        style=ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=self.thme["ent"])
        for w in master.winfo_children():
            if w.winfo_class() == "Button":
                w.configure(bg=self.thme["btn"][0])
                w.configure(highlightbackground=self.thme["btn"][1])
                w.configure(activebackground=self.thme["btn"][2])
                w.configure(fg=self.thme["txt"])
            elif w.winfo_class() == "Entry":
                w.configure(bg=self.thme["ent"])
                w.configure(fg=self.thme["txt"])
            elif isinstance(w, ttk.Combobox):
                pass
                w.configure(foreground='white')
            elif isinstance(w, Text):
                w.configure(bg=self.thme["ent"])
                w.configure(fg=self.thme["txt"])
            elif w.winfo_class() == "Checkbutton":
                w.configure(bg=self.thme["bg"])
                w.configure(highlightbackground=self.thme["bg"])
                w.configure(activebackground=self.thme["bg"])
                w.configure(fg=self.thme["txt"])
                w.configure(selectcolor=self.thme["ent"])
            else:
                w.configure(bg=self.thme["bg"])
                try:
                    w.configure(fg=self.thme["txt"])
                except:
                    pass
    
    def changeTheme(self, newTheme):
        self.thme = newTheme
        self.applyTheme(self.master)
        self.themeTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.startFolderTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.startFolderTT2.changeTheme(newTheme["tt"], newTheme["txt"])
        self.forceDefTT.changeTheme(newTheme["tt"], newTheme["txt"])
    
    def chSF(self):
        path = askdirectory(title="Set starting directory for this file explorer")
        if not path == "":
            if path.startswith("/home") and sys.platform == "linux":
                path = path[1:]
                pos = path.find("/", 5)
                tarLen = len(path) - pos
                while len(path) > tarLen:
                    path = path[1:]
                path = "~" + path
            print(path)
            self.startFSV.set(path)
            self.options["startFolder"] = path
            self.save_options()
            self.updFunc("startFolder", path)
    
    def chFDP(self):
        self.options["forceDefPaths"] = self.forceDefB.get()
        self.save_options()
        self.updFunc("forceDefPaths", self.forceDefB.get())

    
    def save_options(self):
        newjson = json.dumps(self.options, sort_keys=True, indent=5)
        opts = open('save/options.json', 'w')
        opts.write(newjson)
        opts.close()
    
    def updateOpt(self, key, value):
        self.options[key] = value

    def hide(self):
        self.hidden = True
        for w in self.master.winfo_children():
            w.grid_remove()
    def show(self):
        self.hidden = False
        self.setupLabel.grid(column=1, row=1, sticky="w")
        self.themeCBox.grid(column=2, row=1, sticky="w")
        self.nameLabel.grid(column=1, row=2, sticky="w")
        self.startFent.grid(column=2, row=2, sticky="w")
        self.setSF.grid(column=3, row=2, sticky="w")
        self.fdLabel.grid(column=1, row=3, sticky="w")
        self.forceDefault.grid(column=2, row=3, sticky="w")
