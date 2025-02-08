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

class SetupMenu():
    def __init__(self, master, thme:dict, startHidden:bool=False):
        self.hidden = startHidden
        self.master = master
        self.thme = thme
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
        self.console = Console(master, 'Start a decompile and the terminal output will appear here!', 0, 4, self.conFix, 12)
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
        self.outBrowse = Button(master, text='Browse', command=self.output, cursor="hand2")
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
        self.angleSB = BoolSpinbox(self.advOpt, range=[0,360], bg=thme["ent"], fg=thme["txt"])
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
        self.groupSB = BoolSpinbox(self.advOpt, range=[0,4096], bg=thme["ent"], fg=thme["txt"], increment=16)
        self.pf2B = BooleanVar(self.advOpt, value=False)
        self.pf2Chk = Checkbutton(self.advOpt, text="-p", variable=self.pf2B)
        # Tooltips
        self.logChkTT = ToolTip(self.logChk, "Writes the log in the terminal below as a text file inside the logs folder.", background=thme["tt"], foreground=thme["txt"])
        self.dashTChkTT = ToolTip(self.dashTChk, "Specify a texture to replace while compiling, you can globally replace all textures by specifying one bitmap or replace a single texture by following this format: \'tex1.bmp,tex2.bmp\'.", background=thme["tt"], foreground=thme["txt"])
        self.rNormalTT = ToolTip(self.rNormalChk, "Tags flipped normals in the console when enabled, useful for finding issues with backface culling.", background=thme["tt"], foreground=thme["txt"])
        self.angleSBtt = ToolTip(self.angleChk, "Overrides the blend angle of vertex normals, Valve recommends setting this value to 2 according to the HLSDK docs.", background=thme["tt"], foreground=thme["txt"])
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
        self.console = Console(master, 'Currently no warnings or errors!', 0, 5, self.conFix, 10)
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
    
    def groupSBhandler(self):
        if self.angleB.get():
            self.groupSB.unlock()
        else:
            self.groupSB.lock()
    
    def compilerStuff(self, compiler):
        js = open("save/compilers.json", 'r')
        fullJS = json.loads(js.read())
        self.compJS = fullJS["compilers"][self.compSel.get()]
        if self.compJS["type"].lower() == "svengine":
            self.svengine = True
            self.keepBonesChk.grid(column=1, row=2, sticky="w")
            self.pf2Chk.grid_remove()
        else:
            self.svengine = False
            self.keepBonesChk.grid_remove()
            self.pf2Chk.grid(column=1, row=2, sticky="w")

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
            self.flipB.get(),self.angleB.get(),self.hitboxB.get(),self.ignoreB.get(),self.pf2B.get(),self.groupB.get()]
            conVars = ["-t", "-r", "-n", "-f", "-a", "-h", "-i", "-p", "-g"]
        else:
            self.boolVars = [self.dashTbool.get(),self.rNormalB.get(),self.bNormB.get(),
            self.flipB.get(),self.angleB.get(),self.hitboxB.get(),self.ignoreB.get(),self.keepBonesB.get(),self.groupB.get()]
            print()
            conVars = ["-t", "-r", "-n", "-f", "-a", "-h", "-i", "-k", "-g"]
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
                print(oID)
                oID += 1
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
        try:
            paths = self.compJS["path"]["default"][sys.platform]
            for p in paths:
                if os.path.exists(os.path.expanduser(p)):
                    print(p)
                    compilerPath = os.path.expanduser(p)
                    compilerFound = True
                    break
            if not compilerFound:
                paths = self.compJS["path"]["custom"]
                if os._exists(paths):
                    compilerPath = paths
                    compilerFound = True
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

        if sys.platform == 'linux':
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
        elif sys.platform == 'win32':
            if cOpts == None:
                tOutput = subprocess.getoutput(f'\"{compilerPath}\" \"{mdl}\"')
            else:
                tOutput = subprocess.getoutput(f'\"{compilerPath}\" {cOpts} \"{mdl}\"')
        # I don't have a Mac so I can't compile mdldec to Mac targets :(
        # So instead I have to use wine for Mac systems
        """elif sys.platform == 'darwin':
            tOutput = subprocess.getoutput(f'wine third_party/mdldec_win32.exe \"{mdl}\"')"""
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
    def __init__(self, master, thme:dict, thmecallback, startHidden:bool=False):
        self.hidden = startHidden
        self.master = master
        self.thme = thme
        # Grabbing options
        jsf = open('save/options.json', 'r')
        js = jsf.read()
        jsf.close()
        self.options = json.loads(js)
        # Options
        self.setupLabel = Label(master, text=f"Theme: ", background=thme["bg"], foreground=thme["txt"])
        self.nameLabel = Label(master, text="Starting directory: ", background=thme["bg"], fg=thme["txt"])
        themes = ["Freeman", "Shephard", "Calhoun", "Cross"]
        self.themeCBox = ttk.Combobox(master, cursor="hand2", values=themes)
        self.themeCBox.bind("<<ComboboxSelected>>", thmecallback)
        # Tooltips
        self.githubTT = ToolTip(self.setupLabel, "Changes the program's theme, current options are: Freeman, Shephard, Calhoun and Cross.", background=thme["tt"], foreground=thme["txt"])
        self.gameBtt = ToolTip(self.nameLabel, "Sets the directory that the built-in file explorer will start in, the default is the documents folder.", background=thme["tt"], foreground=thme["txt"])
        if not startHidden:
            self.setupLabel.grid(column=1, row=1)
            self.nameLabel.grid(column=1, row=2)
        
        # Applying theme
        self.applyTheme(master)
    
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

    def hide(self):
        self.hidden = True
        for w in self.master.winfo_children():
            w.grid_remove()
    def show(self):
        self.hidden = False
        self.setupLabel.grid(column=1, row=1, sticky="w")
        self.themeCBox.grid(column=2, row=1, sticky="w")
        self.nameLabel.grid(column=1, row=2, sticky="w")
