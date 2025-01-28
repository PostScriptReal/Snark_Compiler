from tkinter import *
from tkinter import ttk
from tktooltip import ToolTip
import os
from tkinter.filedialog import askopenfilename, askdirectory
import subprocess
import shutil
import datetime
from helpers import BoolEntry, Console, BoolSpinbox
import json

class SetupMenu():
    def __init__(self, master, thme:dict, startHidden:bool=False):
        self.hidden = startHidden
        self.master = master
        gOptions = ["Half-Life", "Sven Co-op"]
        gText = StringVar()
        gText.set(gOptions[0])
        self.gameSel = ttk.Combobox(master, textvariable=gText, values=gOptions)
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
        for w in master.winfo_children():
            if w.winfo_class() == "Button":
                w.configure(bg=thme["btn"][0])
                w.configure(highlightbackground=thme["btn"][1])
                w.configure(activebackground=thme["btn"][2])
            elif w.winfo_class() == "Entry":
                pass
                # w.configure(bg=thme["ent"])
            elif isinstance(w, ttk.Combobox):
                pass
                w.configure(foreground='black')
                # w["menu"].config(bg=thme["btn"][1])
            else:
                w.configure(bg=thme["bg"])
            try:
                w.configure(fg=thCol["txt"])
            except:
                pass
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

class DecompMenu():
    def __init__(self, master, thme:dict, startHidden:bool=False):
        self.hidden = startHidden
        self.master = master
        self.advOpt = Frame(master, borderwidth=2, bg=thme["bg"], relief="sunken")
        self.thme = thme
        """gOptions = ["Half-Life", "Sven Co-op"]
        gText = StringVar()
        gText.set(gOptions[0])
        self.gameSel = ttk.Combobox(master, textvariable=gText, values=gOptions)
        self.gameSel.grid(column=1, row=2)"""
        self.setupLabel = Label(master, text="MDL Input: ")
        self.nameLabel = Label(master, text="Output: ")
        self.name = StringVar()
        self.nameEntry = Entry(master, textvariable=self.name, width=55)
        self.out = StringVar()
        self.outputEntry = Entry(master, textvariable=self.out, width=55)
        self.mdlBrowse = Button(master, text='Browse', command=self.findMDL)
        self.outBrowse = Button(master, text='Browse', command=self.output)
        self.advOptLabel = Label(self.advOpt, text="Advanced Options")
        self.logVal = BooleanVar(self.advOpt, value=False)
        self.logChk = Checkbutton(self.advOpt, text="Write log to file", variable=self.logVal, command=self.setLog)
        self.logChkTT = ToolTip(self.logChk, "Writes the log in the terminal below as a text file inside the logs folder.", background=thme["tt"], foreground=thme["txt"])
        self.decomp = Button(master, text='Decompile', command=self.startDecomp)
        self.console = Console(master, 'Start a decompile and the terminal output will appear here!', 0, 4, 50, 10)
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
            self.decomp.grid(column=0, row=3, pady=(20,0))
            self.console.show()
        
        # Applying theme
        self.applyTheme(master)
        self.applyTheme(self.advOpt)
    def setLog(self):
        self.logOutput = self.logVal.get()

    def applyTheme(self, master):
        for w in master.winfo_children():
            if w.winfo_class() == "Button":
                w.configure(bg=self.thme["btn"][0])
                w.configure(highlightbackground=self.thme["btn"][1])
                w.configure(activebackground=self.thme["btn"][2])
                w.configure(fg=self.thme["txt"])
            elif w.winfo_class() == "Entry":
                pass
                # w.configure(bg=self.thme["ent"])
            elif isinstance(w, ttk.Combobox):
                pass
                w.configure(foreground='black')
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
        self.mdlBrowse.grid(column=2, row=0, padx=(6,0))
        self.outBrowse.grid(column=2, row=1, padx=(6,0))
        self.advOpt.grid(column=0, row=2, sticky="nsew", columnspan=10, pady=(20,0))
        self.advOptLabel.grid(column=0, row=0, sticky="w")
        self.logChk.grid(column=0, row=1, sticky="w")
        self.decomp.grid(column=0, row=3, pady=(20,0))
        self.console.show()
    
    def findMDL(self):
        # startdir = self.options["startFolder"]
        startDir = os.path.expanduser("~/Documents")
        fileTypes = [("GoldSRC Model", "*.mdl"), ("All Files", "*.*")]
        self.name.set(askopenfilename(title="Select MDL", initialdir=startDir, filetypes=fileTypes))
    def output(self):
        # startdir = self.options["startFolder"]
        startDir = os.path.expanduser("~/Documents")
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
            curDate = f"{date.strftime('%Y')}-{date.strftime('%m')}-{date.strftime('%d')}-{date.strftime('%H')}-{date.strftime('%M')}-{date.strftime('%S')}"
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
        self.hidden = startHidden
        self.master = master
        self.svengine = False
        self.selects = Frame(master, borderwidth=2, bg=thme["bg"])
        self.advOpt = Frame(master, borderwidth=2, bg=thme["bg"], relief="sunken")
        self.thme = thme
        self.setupLabel = Label(master, text="QC Input: ")
        self.nameLabel = Label(master, text="Output: ")
        self.name = StringVar()
        self.nameEntry = Entry(master, textvariable=self.name, width=55)
        self.out = StringVar()
        self.outputEntry = Entry(master, textvariable=self.out, width=55)
        self.mdlBrowse = Button(master, text='Browse', command=self.findMDL)
        self.outBrowse = Button(master, text='Browse', command=self.output)
        self.compLabel = Label(self.selects, text="Compiler: ")
        cList = open("save/compilers.txt", "r")
        cOptions = cList.read().split('\n')
        cOptions.pop(len(cOptions)-1)
        cText = StringVar()
        cText.set(cOptions[0])
        self.compSel = ttk.Combobox(self.selects, textvariable=cText, values=cOptions, width=8)
        self.compSel.bind("<<ComboboxSelected>>", self.compilerStuff)
        self.gameLabel = Label(self.selects, text="Game Profile: ")
        gList = open("save/games.txt", "r")
        gOptions = gList.read().split('\n')
        gOptions.pop(len(gOptions)-1)
        gText = StringVar()
        gText.set(gOptions[0])
        self.gameSel = ttk.Combobox(self.selects, textvariable=gText, values=gOptions, width=10)
        # self.gameSel.bind("<<ComboboxSelected>>", self.compilerStuff)


        # Advanced Options
        # All options for Half-Life's StudioMDL can be found here https://github.com/ValveSoftware/halflife/blob/master/utils/studiomdl/studiomdl.c at line 3362-3408
        # Note that the Half-Life SDK doesn't document every command available to the compiler
        # Some information for other GoldSRC compilers can be found here: https://developer.valvesoftware.com/wiki/StudioMDL_(GoldSrc)
        """ Commands that have yet to be implemented into the GUI:
                -n - Tags bad normals
                -f - Flips all triangles
                -i - Ignore warnings
                -p - Force power of 2 textures (Unavailable in Sven Co-op StudioMDL)
                -g - Sets the maximum group size for sequences in KB
            While -t is implemented, the option to replace one texture with another isn't yet.
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
        self.angleSB = BoolSpinbox(self.advOpt, range=[0,360], bg=thme["ent"], fg=thme["txt"])
        self.hitboxB = BooleanVar(self.advOpt, value=False)
        self.hitboxChk = Checkbutton(self.advOpt, text="-h", variable=self.hitboxB)
        self.keepBonesB = BooleanVar(self.advOpt, value=False)
        self.keepBonesChk = Checkbutton(self.advOpt, text="-k", variable=self.keepBonesB)
        # Tooltips
        self.logChkTT = ToolTip(self.logChk, "Writes the log in the terminal below as a text file inside the logs folder.", background=thme["tt"], foreground=thme["txt"])
        self.dashTChkTT = ToolTip(self.dashTChk, "Specify a texture to replace while compiling, you can globally replace all textures by specifying one bitmap or replace a single texture by following this format: \'tex1.bmp,tex2.bmp\'.", background=thme["tt"], foreground=thme["txt"])
        self.rNormalTT = ToolTip(self.rNormalChk, "Tags flipped normals in the console when enabled, useful for finding issues with backface culling.", background=thme["tt"], foreground=thme["txt"])
        self.angleSBtt = ToolTip(self.angleChk, "Overrides the blend angle of vertex normals, Valve recommends setting this value to 2 according to the HLSDK docs.", background=thme["tt"], foreground=thme["txt"])
        self.angleChkTT = ToolTip(self.hitboxChk, "Dumps hitbox information to the console when enabled.", background=thme["tt"], foreground=thme["txt"])
        self.keepBonesChkTT = ToolTip(self.keepBonesChk, "Tells the compiler to keep all bones, including unweighted bones.", background=thme["tt"], foreground=thme["txt"])
        
        self.decomp = Button(master, text='Compile', command=self.startCompile)
        self.console = Console(master, 'Currently no warnings or errors!', 0, 5, 50, 10)
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
    def setLog(self):
        self.logOutput = self.logVal.get()
    
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
    
    def compilerStuff(self, compiler):
        js = open("save/compilers.json", 'r')
        fullJS = json.loads(js.read())
        self.compJS = fullJS["compilers"][self.compSel.get()]
        if self.compJS["type"].lower() == "svengine":
            self.svengine = True
            self.keepBonesChk.grid(column=7, row=1)
        else:
            self.svengine = False
            self.keepBonesChk.grid_remove()

    def applyTheme(self, master):
        for w in master.winfo_children():
            if w.winfo_class() == "Button":
                w.configure(bg=self.thme["btn"][0])
                w.configure(highlightbackground=self.thme["btn"][1])
                w.configure(activebackground=self.thme["btn"][2])
                w.configure(fg=self.thme["txt"])
            elif w.winfo_class() == "Entry":
                pass
                # w.configure(bg=self.thme["ent"])
            elif isinstance(w, ttk.Combobox):
                pass
                w.configure(foreground='black')
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
        self.mdlBrowse.grid(column=2, row=0, padx=(6,0))
        self.outBrowse.grid(column=2, row=1, padx=(6,0))
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
        if self.svengine:
            self.keepBonesChk.grid(column=7, row=1, sticky="w")
        self.decomp.grid(column=0, row=4, pady=(20,0))
        self.console.show()
    
    def findMDL(self):
        # startdir = self.options["startFolder"]
        startDir = os.path.expanduser("~/Documents")
        fileTypes = [("Quake Compile Files", "*.qc"), ("All Files", "*.*")]
        self.name.set(askopenfilename(title="Select QC", initialdir=startDir, filetypes=fileTypes))
    def output(self):
        # startdir = self.options["startFolder"]
        startDir = os.path.expanduser("~/Documents")
        self.out.set(askdirectory(title="Select Output Folder", initialdir=startDir))
    
    def startCompile(self):
        mdl = self.name.get()
        output = self.out.get()
        tOutput = ''
        compilerPath = ''
        compilerFound = False
        try:
            paths = self.compJS["path"]["default"][sys.platform]
            for p in paths:
                if os._exists(p):
                    compilerPath = p
                    compilerFound = True
                    break
            if not compilerFound:
                paths = self.compJS["paths"]["custom"]
                if os._exists(paths):
                    compilerPath = paths
                    compilerFound = True
        except:
            self.console.setOutput("ERROR: Couldn't find compiler, have you selected one?")
        if sys.platform == 'linux':
            tOutput = subprocess.getoutput(f'./third_party/mdldec \"{mdl}\"')
        elif sys.platform == 'win32':
            tOutput = subprocess.getoutput(f'third_party/mdldec_win32.exe \"{mdl}\"')
        # I don't have a Mac so I can't compile mdldec to Mac targets :(
        # So instead I have to use wine for Mac systems
        """elif sys.platform == 'darwin':
            tOutput = subprocess.getoutput(f'wine third_party/mdldec_win32.exe \"{mdl}\"')"""
        print(tOutput)
        self.console.setOutput(tOutput)
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
