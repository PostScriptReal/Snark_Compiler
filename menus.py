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
from helpers import BoolEntry, Console, BoolSpinbox, QCHandler, HyperlinkImg, Game, GamesHandler
import json
import sys
import jsonc
from interp import SSTReader

# To make things easier for myself, I'm making a new class that contains common values that won't (or usually doesn't) change for each menu.
class MenuTemp():

    def __init__(self, thme:dict, safeWidth:int):
        self.thme = thme
        self.safeWidth = safeWidth

class SetupMenu():
    def __init__(self, template, master, updFunc, startHidden:bool=False, allowGUI:bool=True):
        self.hidden = startHidden
        self.master = master
        thme = template.thme
        self.thme, self.safeWidth = thme, template.safeWidth
        self.allowGUI = allowGUI
        self.updFunc = updFunc
        self.advOpt = Frame(master, borderwidth=2, bg=thme["bg"], relief="sunken")
        self.top = Frame(master, borderwidth=2, bg=thme["bg"])
        self.newGame = False
        self.nameEntW = 62
        if self.safeWidth > 609:
            self.nameEntW = 59

        # Setting up options
        js = open("save/options.json", 'r')
        self.options = json.loads(js.read())
        js.close()
        js = open("save/profiles.json", 'r')
        self.fullGamePFs = json.loads(js.read())
        self.gamePFs = self.fullGamePFs["profiles"]
        js.close()
        gList = open("save/games.txt", "r")
        self.gOptions = gList.read().split('\n')
        self.gOptions.pop(len(self.gOptions)-1)
        gList.close()
        self.games = GamesHandler(self.gOptions)
        self.gameSel = ttk.Combobox(self.top, values=self.games.gNames)
        self.gameSel.current(0)
        self.gameSel.bind("<<ComboboxSelected>>", self.chGame)
        self.setupLabel = Label(master, text="Game Setup", background=thme["bg"], foreground=thme["txt"])
        self.nameLabel = Label(master, text="Name: ", background=thme["bg"], foreground=thme["txt"])
        self.typeLabel = Label(master, text="Engine type:")
        tOpts = ["GoldSRC", "Svengine"]
        self.typeSel = ttk.Combobox(master, values=tOpts, width=8)
        self.typeSel.set(self.gamePFs[self.gameSel.get()]["type"])
        self.name = StringVar()
        self.name.set(self.gOptions[0])
        self.nameEntry = Entry(master, textvariable=self.name, width=self.nameEntW)
        # Capability options
        self.hrBool = BooleanVar(self.advOpt, False)
        self.highRes = Checkbutton(self.advOpt, text="High Resolution BMPs", variable=self.hrBool)
        self.ucBool = BooleanVar(self.advOpt, False)
        self.unlockChrome = Checkbutton(self.advOpt, text="Unlocked Chrome", variable=self.ucBool)
        self.fbBool = BooleanVar(self.advOpt, False)
        self.fullBright = Checkbutton(self.advOpt, text="Fullbright", variable=self.fbBool)
        # Tooltips
        self.typeTT = ToolTip(self.typeSel, "The Engine type variable is used to check if the compiler supports the features that an engine has, for example if you set the type to Svengine, you'll have the -k compiler option show up.", thme["tt"], thme["txt"])
        self.highResTT = ToolTip(self.highRes, "Check this if the game supports having textures with a resolution higher than 512x512.", thme["tt"], thme["txt"])
        self.unlockChromeTT = ToolTip(self.unlockChrome, "Check this if the game supports having Chrome textures with a resolution other than 64x64.", thme["tt"], thme["txt"])
        self.fullBrightTT = ToolTip(self.fullBright, "Check this if the game supports the fullbright flag for models.", thme["tt"], thme["txt"])

        self.addGame = Button(self.top, text="Add New Game", command=self.addNGame)
        self.saveGame = Button(self.top, text="Save Game", command=self.saveGame)
        if not startHidden:
            self.show()

        # Applying theme
        self.applyTheme(master)
        self.applyTheme(self.advOpt)
        self.applyTheme(self.top)
    
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
    
    def addNGame(self):
        self.gameSel.set("")
        self.name.set("")
        self.typeSel.current(0)
        self.hrBool.set(False)
        self.ucBool.set(False)
        self.fbBool.set(False)
        self.newGame = True
    
    def saveGame(self):
        if self.newGame:
            # Newgrounds Reference!?!?!
            self.nG = self.name.get()
            if not self.nG.lower() == "half-life" or not self.nG.lower() == "sven co-op":
                oList = open("save/games.txt", "w")
                self.gOptions.append(f"{self.nG}~")
                nList = '\n'.join(self.gOptions)
                nList = nList + '\n'
                oList.write(nList)
                oList.close()
                uJS = {
                    self.nG: {
                        "type": self.typeSel.get(), 
                        "capabilities": {
                            "fullbright": self.fbBool.get(),
                            "1024px": self.hrBool.get(),
                            "unlockedChrome": self.ucBool.get()
                        }
                    }
                }
                js = open(f"save/user/game{self.nG}.json", "w")
                js.write(json.dumps(uJS, sort_keys=True, indent=5))
                js.close()
                self.games = GamesHandler(self.gOptions)
                self.gameSel["values"] = self.games.gNames
                self.updFunc(self.games)
    
    def changeTheme(self, newTheme):
        self.thme = newTheme
        self.applyTheme(self.master)
        self.applyTheme(self.advOpt)
        self.applyTheme(self.top)
        self.highResTT.changeTheme(self.thme["tt"], self.thme["txt"])
        self.typeTT.changeTheme(self.thme["tt"], self.thme["txt"])
        self.unlockChromeTT.changeTheme(self.thme["tt"], self.thme["txt"])
        self.fullBrightTT.changeTheme(self.thme["tt"], self.thme["txt"])
    
    def chGame(self, e):
        self.newGame = False
        self.selComp = self.gameSel.get()
        self.name.set(self.selComp)
        if not self.games.checkCustom(self.gameSel.get()):
            self.typeSel.set(self.gamePFs[self.selComp]["type"])
            self.hrBool.set(self.gamePFs[self.selComp]["capabilities"]["1024px"])
            self.ucBool.set(self.gamePFs[self.selComp]["capabilities"]["unlockedChrome"])
            # self.fsBool.set(self.gamePFs[self.selComp]["capabilities"]["flatshade"])
            self.fbBool.set(self.gamePFs[self.selComp]["capabilities"]["fullbright"])
        else:
            js = open(f"save/user/game{self.gameSel.get()}.json", 'r')
            gJS = json.loads(js.read())
            gameDat = gJS[self.gameSel.get()]
            self.typeSel.set(gameDat["type"])
            self.hrBool.set(gameDat["capabilities"]["1024px"])
            self.ucBool.set(gameDat["capabilities"]["unlockedChrome"])
            # self.fsBool.set(gameDat["capabilities"]["flatshade"])
            self.fbBool.set(gameDat["capabilities"]["fullbright"])
        """# If editing options were removed and the compiler doesn't have editing disabled
        if self.hiddenEdit and not self.compDat[self.selComp]["disableEdit"]:
            self.hiddenEdit = False
            self.nameLabel.grid(column=1, row=4, sticky=(W))
            self.nameEntry.grid(column=2, row=4, sticky=(W))
            self.pathLabel.grid(column=1, row=5, sticky="w")
            self.csPathEntry.grid(column=2, row=5, sticky="w")
        # If editing options were available and the compiler has editing disabled
        elif not self.hiddenEdit and self.compDat[self.selComp]["disableEdit"]:
            self.hiddenEdit = True
            self.nameLabel.grid_remove()
            self.nameEntry.grid_remove()
            self.pathLabel.grid(column=1, row=4, sticky="w")
            self.csPathEntry.grid(column=2, row=4, sticky="w")"""
    
    def updateOpt(self, key, value):
        if not key.startswith("gsMV"):
            self.options[key] = value
        else:
            self.options["gsMV"][key.replace("gsMV", "")] = value

    def hide(self):
        self.hidden = True
        for w in self.master.winfo_children():
            w.grid_remove()

    def show(self):
        self.hidden = False
        self.top.grid(column=1, row=2, sticky="w", columnspan=10)
        self.gameSel.grid(column=0, row=0)
        self.setupLabel.grid(column=1, row=3, sticky=(W), padx=(10, 0))
        self.nameLabel.grid(column=1, row=4, sticky=(W))
        self.nameEntry.grid(column=2, row=4, sticky=(W))
        self.typeLabel.grid(column=1, row=5, sticky=(W))
        self.typeSel.grid(column=2, row=5, sticky=(W))
        self.advOpt.grid(column=1, row=6, sticky="nsew", columnspan=10, pady=(20,0))
        self.highRes.grid(column=0, row=0, sticky="w")
        self.unlockChrome.grid(column=1,row=0,sticky="w")
        self.fullBright.grid(column=3,row=0,sticky="w")
        self.addGame.grid(column=1, row=0, sticky="w", padx=(10,0))
        self.saveGame.grid(column=2,row=0,sticky="w", padx=(10,0))

class CompSetupMenu():
    def __init__(self, template, master, updFunc, startHidden:bool=False):
        self.hidden = startHidden
        self.master = master
        thme = template.thme
        self.thme, self.safeWidth = thme, template.safeWidth
        self.top = Frame(master, borderwidth=2, bg=thme["bg"])
        self.hiddenEdit = True
        self.updFunc = updFunc
        # Setting up options
        js = open("save/options.json", 'r')
        self.options = json.loads(js.read())
        js.close()
        js = open("save/compilers.jsonc", 'r')
        self.fullCJS = jsonc.load(js)
        self.compDat = self.fullCJS["compilers"]
        js.close()
        js = open("save/paths.json", 'r')
        self.csPaths = json.loads(js.read())
        js.close()
        cList = open("save/compilers.txt", "r")
        cOptions = cList.read().split('\n')
        cOptions.pop(len(cOptions)-1)
        self.selComp = "GoldSRC"
        self.gameSel = ttk.Combobox(master, values=cOptions)
        self.gameSel.current(0)
        self.gameSel.bind("<<ComboboxSelected>>", self.chComp)
        self.setupLabel = Label(master, text="Compiler Setup", background=thme["bg"], foreground=thme["txt"])
        self.nameLabel = Label(self.top, text="Name: ", background=thme["bg"], foreground=thme["txt"])
        self.pathLabel = Label(self.top, text="Custom path: ", background=thme["bg"], foreground=thme["txt"])
        self.name = StringVar()
        self.name.set(cOptions[0])
        self.nameEntry = Entry(self.top, textvariable=self.name, width=50)
        self.csPath = StringVar()
        self.csPath.set(self.csPaths["GoldSRC"])
        self.csPathEntry = Entry(self.top, textvariable=self.csPath, width=40)
        self.csPathEntry.bind("<FocusOut>", self.inputHandler)
        self.csPathButton = Button(self.top, text="Save Path", command=self.savePath)
        if not startHidden:
            self.show()
        
        # Applying theme
        self.applyTheme(master)
        self.applyTheme(self.top)
    
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
    
    def inputHandler(self, e=False):
        self.csPath.set(self.csPathEntry.get())
        self.csPaths[self.gameSel.get()] = self.csPath.get()
        js = open("save/paths.json", 'w')
        nJS = json.dumps(self.csPaths, sort_keys=True, indent=5)
        js.write(nJS)
        js.close()
        self.updFunc(self.gameSel.get(), self.csPath.get())
    
    def savePath(self):
        self.csPath.set(self.csPathEntry.get())
        self.csPaths[self.gameSel.get()] = self.csPath.get()
        js = open("save/paths.json", 'w')
        nJS = json.dumps(self.csPaths, sort_keys=True, indent=5)
        js.write(nJS)
        js.close()
        self.updFunc(self.gameSel.get(), self.csPath.get())
    
    def changeTheme(self, newTheme):
        self.thme = newTheme
        self.applyTheme(self.master)
        self.applyTheme(self.top)
    
    def updateOpt(self, key, value):
        if not key.startswith("gsMV"):
            self.options[key] = value
        else:
            self.options["gsMV"][key.replace("gsMV", "")] = value
    
    def chComp(self, e):
        self.selComp = self.gameSel.get()
        self.name.set(self.selComp)
        self.csPath.set(self.csPaths[self.selComp])
        # If editing options were removed and the compiler doesn't have editing disabled
        if self.hiddenEdit and not self.compDat[self.selComp]["disableEdit"]:
            self.hiddenEdit = False
            self.nameLabel.grid(column=1, row=4, sticky=(W))
            self.nameEntry.grid(column=2, row=4, sticky=(W))
            self.pathLabel.grid(column=1, row=5, sticky="w")
            self.csPathEntry.grid(column=2, row=5, sticky="w")
            self.csPathButton.grid(column=3,row=5,sticky="w", padx=(5,0))
        # If editing options were available and the compiler has editing disabled
        elif not self.hiddenEdit and self.compDat[self.selComp]["disableEdit"]:
            self.hiddenEdit = True
            self.nameLabel.grid_remove()
            self.nameEntry.grid_remove()
            self.pathLabel.grid(column=1, row=4, sticky="w")
            self.csPathEntry.grid(column=2, row=4, sticky="w")
            self.csPathButton.grid(column=3,row=4,sticky="w", padx=(5,0))

    def hide(self):
        self.hidden = True
        for w in self.master.winfo_children():
            w.grid_remove()
    def show(self):
        self.hidden = False
        self.gameSel.grid(column=1, row=2, sticky="w")
        self.setupLabel.grid(column=1, row=3, sticky=(W), padx=(10, 0))
        if not self.compDat[self.selComp]["disableEdit"]:
            self.hiddenEdit = False
            self.top.grid(column=1, row=4, sticky="nsew")
            self.nameLabel.grid(column=1, row=0, sticky=(W))
            self.nameEntry.grid(column=2, row=0, sticky=(W))
            self.pathLabel.grid(column=1, row=1, sticky="w")
            self.csPathEntry.grid(column=2, row=1, sticky="w", padx=(15,0))
            self.csPathButton.grid(column=3,row=1,sticky="w", padx=(5,0))
        else:
            self.hiddenEdit = True
            self.top.grid(column=1, row=4, sticky="nsew")
            self.pathLabel.grid(column=1, row=0, sticky="w")
            self.csPathEntry.grid(column=2, row=0, sticky="w", padx=(15,0))
            self.csPathButton.grid(column=3,row=0,sticky="w", padx=(5,0))

class DecompMenu():
    def __init__(self, template, master, startHidden:bool=False):
        self.curFont = font.nametofont('TkDefaultFont').actual()
        self.widthFix = 51
        self.conFix = 46
        self.logOutput = False
        if self.curFont["family"].lower() == "nimbus sans l" or sys.platform == "win32":
            self.widthFix = 58
            self.conFix = 53
        else:
            pass
        self.hidden = startHidden
        self.master = master
        thme = template.thme
        self.thme, self.safeWidth = thme, template.safeWidth
        if self.safeWidth > 609:
            n = 2
            self.widthFix, self.conFix = self.widthFix-n, self.conFix-n
        self.quick = Frame(master, borderwidth=2, bg=thme["bg"])
        self.advOpt = Frame(master, borderwidth=2, bg=thme["bg"], relief="sunken")
        self.advOptR2 = Frame(self.advOpt, borderwidth=2, bg=thme["bg"])
        # Setting up options
        js = open("save/options.json", 'r')
        self.options = json.loads(js.read())
        js.close()
        self.presets = {
            "presets": {
                # For most compilers
                "GoldSRC": {
                    "-u": False,
                    "-V": False,
                    "-m": True
                },
                # For Sven Co-op's StudioMDL
                "Svengine": {
                    "-u": True,
                    "-V": False,
                    "-m": True
                },
                # For the DoomMusic StudioMDL compiler
                "DoomMusic": {
                    "-u": True,
                    "-V": False,
                    "-m": True
                },
                # For Xash3D engine mods
                "Xash3D": {
                    "-u": False,
                    "-V": False,
                    "-m": False
                }
            }
        }
        presetNames = list(self.presets["presets"].keys())
        self.quickStpLbl = Label(self.quick, text="Quick Setup Presets: ")
        self.setupLabel = Label(master, text="MDL Input: ")
        self.nameLabel = Label(master, text="Output: ")
        self.presetSel = ttk.Combobox(self.quick, values=presetNames)
        self.presetSel.current(self.options["defDPreset"])
        self.presetDat = self.presets["presets"][self.presetSel.get()]
        self.presetSel.bind("<<ComboboxSelected>>", self.chPreset)
        self.name = StringVar()
        self.nameEntry = Entry(master, textvariable=self.name, width=self.widthFix)
        self.nameEntry.bind("<FocusOut>", self.inputHandler)
        self.out = StringVar()
        self.outputEntry = Entry(master, textvariable=self.out, width=self.widthFix)
        self.mdlBrowse = Button(master, text='Browse', command=self.findMDL, cursor="hand2")
        self.outBrowse = Button(master, text='Browse', command=self.output, cursor="hand2")
        self.advOptLabel = Label(self.advOpt, text="Advanced Options")
        self.decomp = Button(master, text='Decompile', command=self.startDecomp, cursor="hand2")
        self.hlmv = Button(master, text='Open model in HLMV', command=self.openHLAM, cursor="hand2")
        self.console = Console(master, 'Start a decompile and the terminal output will appear here!', 0, 5, self.conFix, 12)
        # Advanced options
        self.logVal = BooleanVar(self.advOpt, value=False)
        self.logChk = Checkbutton(self.advOpt, text="Write log to file", variable=self.logVal, command=self.setLog)
        self.mVal = BooleanVar(self.advOpt, value=self.presetDat["-m"])
        self.mChk = Checkbutton(self.advOpt, text="GoldSRC compatability", variable=self.mVal)
        self.uVal = BooleanVar(self.advOpt, value=self.presetDat["-u"])
        self.uChk = Checkbutton(self.advOpt, text="Fix UV shifts", variable=self.uVal)
        self.vVal = BooleanVar(self.advOpt, value=self.presetDat["-V"])
        self.vChk = Checkbutton(self.advOpt, text="Ignore checks", variable=self.vVal)
        self.tVal = BooleanVar(self.advOpt, value=True)
        self.tChk = Checkbutton(self.advOptR2, text="Place textures in subfolder", variable=self.tVal)
        if not startHidden:
            self.show()
        
        # Tooltips
        self.logChkTT = ToolTip(self.logChk, "Writes the log in the terminal below as a text file inside the logs folder.", background=thme["tt"], foreground=thme["txt"])
        self.mChkTT = ToolTip(self.mChk, "By default, the decompiler outputs .qc files with features for Xash3D that GoldSRC does not support, enabling this makes the output GoldSRC compatible.", background=thme["tt"], foreground=thme["txt"])
        self.uChkTT = ToolTip(self.uChk, "Enabling this flag will make the decompiler output a model with UVs that are accurate to the OG model, RECOMMENDED FOR SC STUDIOMDL AND OTHERS THAT HAVE NO UV SHIFTING ISSUES!", background=thme["tt"], foreground=thme["txt"])
        self.vChkTT = ToolTip(self.vChk, "Enabling this will make the decompiler ignore validity checks, which might allow you to decompile some broken models", background=thme["tt"], foreground=thme["txt"])
        self.tChkTT = ToolTip(self.tChk, "Disabling this will make the decompiler place textures in the same location as your models, this can fix issues with importing the model in MilkShape3D or Fragmotion.", background=thme["tt"], foreground=thme["txt"])
        self.mdlTT = ToolTip(self.mdlBrowse, "REQUIRED, specifies the MDL file used to decompile a model, you cannot leave this blank.", background=thme["tt"], foreground=thme["txt"])
        self.outputTT = ToolTip(self.outBrowse, "OPTIONAL, if an output folder is not specified, then it will place the decompiled model in a subfolder of where the MDL file is located.", background=thme["tt"], foreground=thme["txt"])
        
        # Applying theme
        self.applyTheme(master)
        self.applyTheme(self.advOpt)
        self.applyTheme(self.advOptR2)
        self.applyTheme(self.quick)
    def setLog(self):
        self.logOutput = self.logVal.get()
    
    def openHLAM(self):
        print("Opening model in HLMV")
        # If "Half-Life Asset Manager" is selected
        if self.options["gsMV"]["selectedMV"] == 1:
            if sys.platform == "linux":
                print("Opening using \'hlam\' command")
                a = subprocess.getoutput(f"XDG_SESSION_TYPE=x11 hlam \"{self.name.get()}\"")
            else:
                print("Opening using the direct path of the HLAM executable")
                a = subprocess.getoutput(f"\"C:/Program Files (x86)/Half-Life Asset Manager/hlam.exe\" \"{self.name.get()}\"")
        # If "Other" option is selected
        elif self.options["gsMV"]["selectedMV"] > 1:
            if sys.platform == "linux":
                path = self.options["gsMV"]["csPath"]
                path = os.path.expanduser(path)
                print("Executing user-specified HLMV executable with Wine")
                if path.endswith(".exe"):
                    a = subprocess.getoutput(f"wine \"{path}\" \"{self.name.get()}\"")
                else:
                    a = subprocess.getoutput(f"\"{path}\" \"{self.name.get()}\"")
            else:
                print("Executing user-specified HLMV executable (Native binary)")
                path = self.options["gsMV"]["csPath"]
                a = subprocess.getoutput(f"\"{path}\" \"{self.name.get()}\"")
    
    def inputHandler(self, e=False):
        self.name.set(self.nameEntry.get())
        if not self.name.get() == "" and self.options["gsMV"]["selectedMV"] > 0:
            self.hlmv.grid(column=1, row=4, pady=(10,0), sticky="w")
    
    def chPreset(self, e=False):
        self.presetDat = self.presets["presets"][self.presetSel.get()]
        self.mVal.set(self.presetDat["-m"])
        self.uVal.set(self.presetDat["-u"])
        self.vVal.set(self.presetDat["-V"])

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
        self.applyTheme(self.advOptR2)
        self.applyTheme(self.quick)
        self.mdlTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.outputTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.logChkTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.mChkTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.uChkTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.vChkTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.tChkTT.changeTheme(newTheme["tt"], newTheme["txt"])
    
    def updateOpt(self, key, value):
        if not key.startswith("gsMV"):
            self.options[key] = value
            if key == "defDPreset":
                self.presetSel.current(value)
                self.chPreset()
        else:
            self.options["gsMV"][key.replace("gsMV", "")] = value

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
        self.quick.grid(column=0,row=2,sticky="nsew", columnspan=10)
        self.quickStpLbl.grid(column=0, row=2, sticky="w")
        self.presetSel.grid(column=1,row=2)
        self.advOpt.grid(column=0, row=3, sticky="nsew", columnspan=10, pady=(20,0))
        self.advOptR2.grid(column=0, row=2, sticky="nsew", columnspan=10)
        self.advOptLabel.grid(column=0, row=0, sticky="w")
        self.logChk.grid(column=0, row=1, sticky="w")
        self.mChk.grid(column=1, row=1, sticky="w")
        self.uChk.grid(column=2, row=1, sticky="w")
        self.vChk.grid(column=3, row=1, sticky="w")
        self.tChk.grid(column=0, row=1, sticky="w")
        self.decomp.grid(column=0, row=4, pady=(10,0))
        if not self.name.get() == "" and self.options["gsMV"]["selectedMV"] > 0:
            self.hlmv.grid(column=1, row=4, pady=(10,0), sticky="w")
        self.console.show()
    
    def findMDL(self):
        startDir = self.options["startFolder"]
        if startDir.startswith("~"):
            startDir = os.path.expanduser(startDir)
        fileTypes = [("GoldSRC Model", "*.mdl"), ("All Files", "*.*")]
        self.name.set(askopenfilename(title="Select MDL", initialdir=startDir, filetypes=fileTypes))
        if not self.name.get() == "" and self.options["gsMV"]["selectedMV"] > 0:
            self.hlmv.grid(column=1, row=4, pady=(10,0), sticky="w")
    def output(self):
        startDir = self.options["startFolder"]
        if startDir.startswith("~"):
            startDir = os.path.expanduser(startDir)
        self.out.set(askdirectory(title="Select Output Folder", initialdir=startDir))
    
    def getArgs(self):
        args = []
        if self.mVal.get():
            args.append("-m")
        if self.uVal.get():
            args.append("-u")
        if self.vVal.get():
            args.append("-V")
        if self.tVal.get():
            args.append("-t")
        cmdArgs = " ".join(args)
        print(cmdArgs)
        return(cmdArgs)
    
    def startDecomp(self):
        mdl = self.name.get()
        output = self.out.get()
        gotArgs = False
        cmdArgs = self.getArgs()
        if not cmdArgs == "" or not cmdArgs == " ":
            gotArgs = True
        if output == "" or output == None:
            output = os.path.join(os.path.dirname(mdl), "Decompile/")
            if not os.path.exists(output):
                os.mkdir(output)
        tOutput = ''
        if sys.platform == 'linux':
            if gotArgs:
                tOutput = subprocess.getoutput(f'./third_party/mdldec -a {cmdArgs} \"{mdl}\"')
            else:
                tOutput = subprocess.getoutput(f'./third_party/mdldec -a \"{mdl}\"')
        elif sys.platform == 'win32':
            if gotArgs:
                tOutput = subprocess.getoutput(f'\"{os.getcwd()}/third_party/mdldec.exe\" -a {cmdArgs} \"{mdl}\"')
            else:
                tOutput = subprocess.getoutput(f'\"{os.getcwd()}/third_party/mdldec.exe\" -a \"{mdl}\"')
        # I don't have a Mac so I can't compile mdldec to Mac targets :(
        # So instead I have to use wine for Mac systems
        """elif sys.platform == 'darwin':
            tOutput = subprocess.getoutput(f'wine third_party/mdldec_win32.exe \"{mdl}\"')"""
        print(tOutput)
        self.console.setOutput(tOutput)
        if self.logVal.get():
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
            elif f.endswith("bmp") and not self.tVal.get():
                shutil.copy(f"{mdlFolder}/{f}", os.path.join(output, f))
                os.remove(f"{mdlFolder}/{f}")
        shutil.copytree(anims, os.path.join(output, 'anims/'))
        if self.tVal.get():
            shutil.copytree(texFolder, os.path.join(output, 'textures/'))
            try:
                shutil.rmtree(texFolder)
            except:
                pass
        try:
            shutil.rmtree(anims)
        except:
            pass

class CompMenu():
    def __init__(self, template, master, startHidden:bool=False):
        self.curFont = font.nametofont('TkDefaultFont').actual()
        self.widthFix = 52
        self.conFix = 47
        thme = template.thme
        self.thme, self.safeWidth = thme, template.safeWidth
        self.advOptFix = True
        if self.curFont["family"].lower() == "nimbus sans l" or sys.platform == "win32":
            self.widthFix = 58
            self.conFix = 40
            self.advOptFix = False
        elif self.safeWidth > 609:
            self.advOptFix = False
        else:
            pass
        self.hidden = startHidden
        self.master = master
        self.svengine, logOutput = False, False
        self.mdlPath = ""
        # Setting up JSON stuff
        js = open("save/compilers.jsonc", 'r')
        self.fullCJS = jsonc.load(js)
        js.close()
        js = open("save/paths.json", 'r')
        self.csPaths = json.loads(js.read())
        js.close()
        js = open("save/profiles.json", 'r')
        self.profiles = json.loads(js.read())
        js.close()
        js = open("save/options.json", 'r')
        self.options = json.loads(js.read())
        js.close()
        if self.safeWidth > 609:
            n = 2
            self.widthFix, self.conFix = self.widthFix-n, self.conFix-n
        self.selects = Frame(master, borderwidth=2, bg=thme["bg"])
        self.advOpt = Frame(master, borderwidth=2, bg=thme["bg"], relief="sunken")
        self.advOpt2 = Frame(self.advOpt, borderwidth=2, bg=thme["bg"])
        self.setupLabel = Label(master, text="QC Input: ")
        self.nameLabel = Label(master, text="Output: ")
        self.name = StringVar()
        self.nameEntry = Entry(master, textvariable=self.name, width=self.widthFix)
        self.nameEntry.bind("<FocusOut>", self.inputHandler)
        self.out = StringVar()
        self.outputEntry = Entry(master, textvariable=self.out, width=self.widthFix)
        self.mdlBrowse = Button(master, text='Browse', command=self.findMDL, cursor="hand2")
        self.outBrowse = Button(master, text='Browse', command=self.output, cursor="hand2")
        self.compLabel = Label(self.selects, text="Compiler: ")
        self.hlmv = Button(master, text='Open model in HLMV', command=self.openHLAM, cursor="hand2")
        cList = open("save/compilers.txt", "r")
        cOptions = cList.read().split('\n')
        cOptions.pop(len(cOptions)-1)
        self.compSel = ttk.Combobox(self.selects, values=cOptions, width=8)
        self.compSel.current(self.options["defComp"])
        self.compSel.bind("<<ComboboxSelected>>", self.compilerStuff)
        self.gameLabel = Label(self.selects, text="Game Profile: ")
        gList = open("save/games.txt", "r")
        gOptions = gList.read().split('\n')
        gOptions.pop(len(gOptions)-1)
        gOptions = GamesHandler(gOptions)
        self.games = gOptions
        self.gameSel = ttk.Combobox(self.selects, values=gOptions.gNames, width=10)
        self.gameSel.current(self.options["defGame"])
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
        if self.advOptFix:
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
            self.keepBonesChk = Checkbutton(self.advOpt, text="-k", variable=self.keepBonesB)
        else:
            self.ignoreB = BooleanVar(self.advOpt, value=False)
            self.ignoreChk = Checkbutton(self.advOpt, text="-i", variable=self.ignoreB)
            self.bNormB = BooleanVar(self.advOpt2, value=False)
            self.bNormChk = Checkbutton(self.advOpt2, text="-n", variable=self.bNormB)
            self.flipB = BooleanVar(self.advOpt2, value=False)
            self.flipChk = Checkbutton(self.advOpt2, text="-f", variable=self.flipB)
            self.groupB = BooleanVar(self.advOpt2, value=False)
            self.groupChk = Checkbutton(self.advOpt2, text="-g", variable=self.groupB, command=self.groupSBhandler)
            self.groupSB = BoolSpinbox(self.advOpt2, range=[0,4096], bg=thme["ent"], bBG=thme["btn"][0], fg=thme["txt"], increment=16)
            self.groupSB.entry.config(width=4)
            self.pf2B = BooleanVar(self.advOpt2, value=False)
            self.pf2Chk = Checkbutton(self.advOpt2, text="-p", variable=self.pf2B)
            self.keepBonesChk = Checkbutton(self.advOpt2, text="-k", variable=self.keepBonesB)
        # Tooltips
        self.logChkTT = ToolTip(self.logChk, "Writes the log in the terminal below as a text file inside the logs folder.", background=thme["tt"], foreground=thme["txt"])
        self.dashTChkTT = ToolTip(self.dashTChk, "Specify a texture to replace while compiling, you can globally replace all textures by specifying one bitmap or replace a single texture by following this format: \'tex1.bmp,tex2.bmp\'.", background=thme["tt"], foreground=thme["txt"])
        self.rNormalTT = ToolTip(self.rNormalChk, "Tags flipped normals in the console when enabled, useful for finding issues with backface culling.", background=thme["tt"], foreground=thme["txt"])
        self.angleSBtt = ToolTip(self.angleChk, "Overrides the blend angle of vertex normals, Valve recommends keeping this value at 2 (the default) according to the HLSDK docs.", background=thme["tt"], foreground=thme["txt"])
        self.angleChkTT = ToolTip(self.hitboxChk, "Dumps hitbox information to the console when enabled.", background=thme["tt"], foreground=thme["txt"])
        self.keepBonesChkTT = ToolTip(self.keepBonesChk, "Tells the compiler to keep all bones, including unweighted bones.", background=thme["tt"], foreground=thme["txt"])
        self.ignoreChkTT = ToolTip(self.ignoreChk, "Tells the compiler to ignore all warnings, useful for when you want to quickly test a model that isn't complete yet.", background=thme["tt"], foreground=thme["txt"])
        self.bNormChkTT = ToolTip(self.bNormChk, "Tags bad normals in the console.", background=thme["tt"], foreground=thme["txt"])
        self.flipChkTT = ToolTip(self.flipChk, "Tells the compiler to flip all triangles in the model.", background=thme["tt"], foreground=thme["txt"])
        self.groupChkTT = ToolTip(self.groupChk, "Sets the maximum group size for sequences in KB", background=thme["tt"], foreground=thme["txt"])
        self.pf2ChkTT = ToolTip(self.pf2Chk, "Forces power of 2 textures when enabled", background=thme["tt"], foreground=thme["txt"])
        self.mdlTT = ToolTip(self.mdlBrowse, "REQUIRED, specifies the QC file used to compile your model, you cannot leave this blank.", background=thme["tt"], foreground=thme["txt"])
        self.outputTT = ToolTip(self.outBrowse, "OPTIONAL, if an output folder is not specified, then it will place the compiled model in a subfolder of where the QC file is located.", background=thme["tt"], foreground=thme["txt"])

        # Checking if the default compiler has the engine type Svengine.
        self.compilerStuff()
        
        self.decomp = Button(master, text='Compile', command=self.startCompile, cursor="hand2")
        self.console = Console(master, 'Currently no warnings or errors!', 0, 5, self.conFix, 12)
        if not startHidden:
            self.show()
        
        # Applying theme
        self.applyTheme(master)
        self.applyTheme(self.advOpt)
        self.applyTheme(self.selects)
        if not self.advOptFix:
            self.applyTheme(self.advOpt2)
        self.angleSB.changeTheme(thme["ent"], thme["btn"][0], thme["txt"])
        self.groupSB.changeTheme(thme["ent"], thme["btn"][0], thme["txt"])
    def setLog(self):
        self.logOutput = self.logVal.get()
    
    def inputHandler(self, e=False):
        self.name.set(self.nameEntry.get())
        self.compatChk()
        mdlPath = os.path.dirname(self.name.get())
        mdlPath = os.path.join(mdlPath, "models")
        if os.path.exists(mdlPath):
            count = -1
            files = os.listdir(mdlPath)
            while count < len(files)-1:
                count += 1
                f = files[count]
                if f.endswith(".mdl"):
                    # Checking if the mdl file that has been found is an external texture model or sequence model and skipping if so
                    if f.endswith("T.mdl"):
                        continue
                    elif f.find("0") != -1:
                        thresh = f.find(".mdl")
                        print(thresh)
                        count = -1
                        for c in f:
                            count += 1
                            if count == thresh-2 and c.isnumeric():
                                f = f.replace(c, "")
                            if count == thresh-1 and c.isnumeric():
                                f = f.replace(c, "")
                        print(f)
                    break
            if os.path.exists(f"{mdlPath}/{f}") and self.options["gsMV"]["selectedMV"] > 0:
                self.mdlPath = os.path.join(mdlPath, f)
                self.hlmv.grid(column=1, row=4, pady=(10,0), sticky="w")
    
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
    
    def compilerStuff(self, event=None):
        self.compJS = self.fullCJS["compilers"][self.compSel.get()]
        if self.compJS["type"].lower() == "svengine":
            self.svengine = True
            if self.advOptFix:
                self.keepBonesChk.grid(column=1, row=2, sticky="w")
            else:
                self.keepBonesChk.grid(column=5, row=2, sticky="w")
            self.pf2Chk.grid_remove()
        else:
            self.svengine = False
            self.keepBonesChk.grid_remove()
            if self.advOptFix:
                self.pf2Chk.grid(column=1, row=2, sticky="w")
            else:
                self.pf2Chk.grid(column=5, row=2, sticky="w")
        self.compatChk()
    
    def openHLAM(self):
        # If "Half-Life Asset Manager" is selected
        if self.options["gsMV"]["selectedMV"] == 1:
            if sys.platform == "linux":
                a = subprocess.getoutput(f"XDG_SESSION_TYPE=x11 hlam \"{self.mdlPath}\"")
            else:
                a = subprocess.getoutput(f"\"C:/Program Files (x86)/Half-Life Asset Manager/hlam.exe\" \"{self.mdlPath}\"")
        # If "Other" option is selected
        elif self.options["gsMV"]["selectedMV"] > 1:
            if sys.platform == "linux":
                path = self.options["gsMV"]["csPath"]
                path = os.path.expanduser(path)
                if path.endswith(".exe"):
                    a = subprocess.getoutput(f"wine \"{path}\" \"{self.mdlPath}\"")
                else:
                    a = subprocess.getoutput(f"\"{path}\" \"{self.mdlPath}\"")
            else:
                path = self.options["gsMV"]["csPath"]
                a = subprocess.getoutput(f"\"{path}\" \"{self.mdlPath}\"")

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
        if not self.advOptFix:
            self.applyTheme(self.advOpt2)
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
        if not key.startswith("gsMV"):
            self.options[key] = value
            # Doing specific things for specific options
            if key == "defComp":
                self.compSel.current(self.options[key])
                self.compilerStuff()
            elif key == "defGame":
                self.gameSel.current(self.options[key])
        # Doing this since the gsMV option needs two square bracket data things in order to update stuff properly,
        # and the function can only use strings.
        else:
            self.options["gsMV"][key.replace("gsMV", "")] = value
    
    def updateComp(self, comp, value):
        self.csPaths[comp] = value
    
    def updateGames(self, game):
        self.games = game
        self.gameSel["values"] = self.games.gNames
    
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
        if self.advOptFix or self.safeWidth > 609:
            self.dashT.grid(column=2, row=1, sticky="w")
            self.dashTChk.grid(column=1, row=1, sticky="w")
        else:
            self.dashT.grid(column=0, row=1, sticky="w",padx=(145,0))
            self.dashTChk.grid(column=0, row=1, sticky="w",padx=(110,0))
        self.rNormalChk.grid(column=3, row=1, sticky="w")
        self.angleChk.grid(column=4, row=1, sticky="w")
        self.angleSB.grid(column=5, row=1, sticky="w")
        self.hitboxChk.grid(column=6, row=1, sticky="w")
        if self.advOptFix:
            self.ignoreChk.grid(column=7, row=1, sticky="w")
        else:
            self.advOpt2.grid(column=0, row=2, sticky="nsew", columnspan=20)
            self.ignoreChk.grid(column=7, row=1, sticky="w")
        if self.advOptFix:
            self.bNormChk.grid(column=8, row=1, sticky="w")
        else:
            self.bNormChk.grid(column=1, row=2, sticky="w")
        if self.advOptFix:
            self.flipChk.grid(column=0, row=2, sticky="w")
        else:
            self.flipChk.grid(column=2, row=2, sticky="w")
        if self.advOptFix:
            self.groupChk.grid(column=0, row=2, sticky="w",padx=(40,0))
            self.groupSB.grid(column=0, row=2, sticky="w",padx=(81,0))
        else:
            self.groupChk.grid(column=3, row=2, sticky="w")
            self.groupSB.grid(column=4, row=2, sticky="w")
        if not self.svengine:
            if self.advOptFix:
                self.pf2Chk.grid(column=1, row=2, sticky="w")
            else:
                self.pf2Chk.grid(column=5, row=2, sticky="w")
        if self.svengine:
            if self.advOptFix:
                self.keepBonesChk.grid(column=1, row=2, sticky="w")
            else:
                self.keepBonesChk.grid(column=5, row=2, sticky="w")
        self.decomp.grid(column=0, row=4, pady=(10,0))
        if not self.mdlPath == "" and self.options["gsMV"]["selectedMV"] > 0:
            self.hlmv.grid(column=1, row=4, pady=(10,0), sticky="w")
        self.console.show()
    
    def findMDL(self):
        startDir = self.options["startFolder"]
        if startDir.startswith("~"):
            startDir = os.path.expanduser(startDir)
        fileTypes = [("Quake Compile Files", "*.qc"), ("All Files", "*.*")]
        self.name.set(askopenfilename(title="Select QC", initialdir=startDir, filetypes=fileTypes))
        self.compatChk()
        mdlPath = os.path.dirname(self.name.get())
        mdlPath = os.path.join(mdlPath, "models")
        if os.path.exists(mdlPath):
            count = -1
            files = os.listdir(mdlPath)
            file = ".mdl"
            while count < len(files)-1:
                count += 1
                f = files[count]
                if f.endswith(".mdl"):
                    # Checking if the mdl file that has been found is an external texture model or sequence model and skipping if so
                    if f.endswith("T.mdl"):
                        continue
                    elif f.find("0") != -1:
                        thresh = f.find(".mdl")
                        print(thresh)
                        count = -1
                        for c in f:
                            count += 1
                            if count == thresh-2 and c.isnumeric():
                                f = f.replace(c, "")
                            if count == thresh-1 and c.isnumeric():
                                f = f.replace(c, "")
                        print(f)
                    file = f
                    break
            if os.path.exists(f"{mdlPath}/{file}") and self.options["gsMV"]["selectedMV"] > 0:
                self.mdlPath = os.path.join(mdlPath, file)
                self.hlmv.grid(column=1, row=4, pady=(10,0), sticky="w")
    
    def compatChk(self, e=False):
        if not self.name.get() == "":
            handler = QCHandler(self.name.get())
            if not self.games.checkCustom(self.gameSel.get()):
                gameDat = self.profiles["profiles"][self.gameSel.get()]
            else:
                js = open(f"save/user/game{self.gameSel.get()}.json", 'r')
                gJS = json.loads(js.read())
                gameDat = gJS[self.gameSel.get()]
            compDat = self.fullCJS["compilers"][self.compSel.get()]
            warnings = []
            if compDat["capabilities"]["1024px"]:
                # If the game doesn't support higher resolution textures, then give a warning in the console.
                if not gameDat["capabilities"]["1024px"] and handler.check1024px():
                    warnings.append("WARNING: The selected game does not support textures higher than 512x512, please downscale the offending textures!")
            else:
                if handler.check1024px() and gameDat["capabilities"]["unlockedChrome"]:
                    warnings.append("WARNING: The selected compiler does not support textures higher than 512x512, please downscale the offending textures!")
                elif handler.check1024px():
                    warnings.append("WARNING: The selected compiler and game does not support textures higher than 512x512, please downscale the offending textures!")
            
            if compDat["capabilities"]["unlockedChrome"]:
                # If the game doesn't support chrome textures that aren't 64x64, then give a warning in the console.
                if not gameDat["capabilities"]["unlockedChrome"] and handler.checkCHROME():
                    warnings.append("WARNING: There are one or more chrome textures that aren't at a fixed resolution of 64x64, please fix that as the selected game does not support this!")
            else:
                if handler.checkCHROME() and gameDat["capabilities"]["unlockedChrome"]:
                    warnings.append("WARNING: There are one or more chrome textures that aren't at a fixed resolution of 64x64, please fix that as the selected compiler does not support this!")
                elif handler.checkCHROME():
                    warnings.append("WARNING: There are one or more chrome textures that aren't at a fixed resolution of 64x64, please fix that as the selected compiler and game does not support this!")
            
            if compDat["capabilities"]["fullbright"]:
                # If the game doesn't support fullbright, then give a warning in the console.
                if not gameDat["capabilities"]["fullbright"] and handler.checkTRM(0):
                    warnings.append("WARNING: Model uses a $texrendermode that isn't supported by the game: fullbright")
            else:
                if handler.checkTRM(0) and gameDat["capabilities"]["fullbright"]:
                    warnings.append("WARNING: Model uses a $texrendermode that isn't supported by the compiler: fullbright")
                elif handler.checkTRM(0):
                    warnings.append("WARNING: Model uses a $texrendermode that isn't supported by the game and the compiler: fullbright")
            
            if not compDat["capabilities"]["flatshade"] and handler.checkTRM(1):
                # If the compiler doesn't support the flatshade $texrendermode, then give a warning in the console.
                warnings.append("WARNING: Model uses a $texrendermode that isn't supported by the compiler: flatshade")
            
            if not compDat["capabilities"]["chromeTRM"] and handler.checkTRM(2):
                # If the compiler doesn't support the chrome $texrendermode, then give a warning in the console.
                warnings.append("WARNING: Compiler doesn't support the chrome $texrendermode, please add the \"CHROME\" prefix to your texture name if you want this effect!")
            
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
                    paths = self.csPaths[self.compSel.get()]
                    if os.path.exists(paths):
                        compilerPath = paths
                        compilerFound = True
            else:
                paths = self.csPaths[self.compSel.get()]
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
            if self.logVal.get():
                date = datetime.datetime.now()
                curDate = f"{date.strftime('%d')}-{date.strftime('%m')}-{date.strftime('%Y')}-{date.strftime('%H')}-{date.strftime('%M')}-{date.strftime('%S')}"
                log = open(f"logs/compile-{curDate}.txt", 'w')
                log.write(tOutput)
                log.close()
            # Moving the compiled MDL file to the output folder
            mdlFolder = ""
            if output == "" or output == None:
                mdlFolder = qcRelChk.qcLoc
                mdlFolder = os.path.join(mdlFolder, "models/")\
                # If there is no models folder, make one!
                if not os.path.exists(mdlFolder):
                    os.mkdir(mdlFolder)
            else:
                mdlFolder = output
            mdlF = qcRelChk.getMDLname()
            self.mdlPath = os.path.join(mdlFolder, mdlF)
            if not self.mdlPath == "" and self.options["gsMV"]["selectedMV"] > 0:
                self.hlmv.grid(column=1, row=4, pady=(10,0), sticky="w")
            # I'm doing this instead of directly copying the mdl file because depending on the options used (e.g. $externaltextures),
            # the compiler will output more than one .mdl file which is needed in order for the compiled model to work.
            # If you are using $externaltextures, the compiler will output a (mdlname).mdl file and (mdlname)T.mdl file,
            # both of them are needed as one has the textures for the model and the other contains the model itself.
            for f in os.listdir(os.getcwd()):
                if f.find(".mdl") != -1:
                    shutil.copy(f, os.path.join(mdlFolder, f))
                    os.remove(os.path.join(os.getcwd(), f))
            # shutil.copy(mdlF, os.path.join(mdlFolder, mdlF))
            # os.remove(mdlF)

class AboutMenu():
    def __init__(self, template, master, startHidden:bool=False):
        self.hidden = startHidden
        self.master = master
        thme = template.thme
        self.thme, self.safeWidth = thme, template.safeWidth
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
        credits = ["PostScript", "\nusing:", "MDLDec by Flying With Gauss", "get_image_size by Paulo Scardine", "TkTooltip by DaedalicEntertainment",
            "JSONC by John Carter"
        ]
        self.nameLabel = Label(master, text="\n".join(credits), background=thme["bg"], fg=thme["txt"])
        # Tooltips
        self.githubTT = ToolTip(self.githubLogo.link, "Source Code and Releases on Github", background=thme["tt"], foreground=thme["txt"])
        self.gameBtt = ToolTip(self.gameBLogo.link, "Official Download page on Gamebanana", background=thme["tt"], foreground=thme["txt"])
        if not startHidden:
            self.show()
        
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
        if not key.startswith("gsMV"):
            self.options[key] = value
        else:
            self.options["gsMV"][key.replace("gsMV", "")] = value
    
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
    def __init__(self, template, master, thmecallback, updFunc, startHidden:bool=False):
        self.curPage = 0
        self.hidden = startHidden
        self.master = master
        thme = template.thme
        self.thme, self.safeWidth = thme, template.safeWidth
        print(self.thme["bg"])
        self.updFunc = updFunc
        # Grabbing options
        jsf = open('save/options.json', 'r')
        js = jsf.read()
        jsf.close()
        self.options = json.loads(js)
        # Checking if options JSON is from a previous version...
        if not self.options["version"] == 4:
            self.upgradeJSON()
        # Pages
        self.pageButtons = Frame(master, borderwidth=2, bg=thme["bg"])
        self.generalButton = Button(self.pageButtons, text="General", cursor="hand2", command=self.genPg)
        self.hlmvButton = Button(self.pageButtons, text="Model Viewers", cursor="hand2", command=self.hlmvPg)
        # General options
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
        # Model Viewer Options
        self.hlmvLabel = Label(master, text="Model Viewer: ")
        hlmvValues = ["None", "Half-Life Asset Manager", "Other"]
        self.hlmvCBox = ttk.Combobox(master, cursor="hand2", values=hlmvValues)
        self.hlmvCBox.current(self.options["gsMV"]["selectedMV"])
        self.hlmvCBox.bind("<<ComboboxSelected>>", self.setMV)
        self.mvPathLabel = Label(master, text="Path to model viewer: ")
        self.mvPathVar = StringVar(master, value="Path to model viewer (if \"Other\" is selected)")
        self.mvPathEnt = BoolEntry(master, textvariable=self.mvPathVar, placeholder="Path to model viewer (if \"Other\" is selected)")
        self.setMVP = Button(master, text="Set Model Viewer Executable", cursor="hand2", command=self.chMVP)
        if self.options["gsMV"]["selectedMV"] > 1:
            self.mvPathEnt.unlock()
            self.mvPathVar.set(self.options["gsMV"]["csPath"])
        # Options for setting defaults for profiles
        self.defCLabel = Label(master, text=f"Default Compiler: ", background=thme["bg"], foreground=thme["txt"])
        self.defGLabel = Label(master, text="Default Game: ", background=thme["bg"], fg=thme["txt"])
        self.defPLabel = Label(master, text="Default Decompile Preset:")
        cList = open("save/compilers.txt", "r")
        cOptions = cList.read().split('\n')
        cOptions.pop(len(cOptions)-1)
        self.compSel = ttk.Combobox(master, values=cOptions)
        self.compSel.bind("<<ComboboxSelected>>", self.setCmp)
        self.compSel.current(self.options["defComp"])
        gList = open("save/games.txt", "r")
        self.gOptions = gList.read().split('\n')
        self.gOptions.pop(len(self.gOptions)-1)
        gList.close()
        self.games = GamesHandler(self.gOptions)
        self.gameSel = ttk.Combobox(master, values=self.games.gNames)
        self.gameSel.bind("<<ComboboxSelected>>", self.setGame)
        self.gameSel.current(self.options["defGame"])
        self.presets = {
            "presets": {
                # For most compilers
                "GoldSRC": {
                    "-u": False,
                    "-V": False,
                    "-m": True
                },
                # For Sven Co-op's StudioMDL
                "Svengine": {
                    "-u": True,
                    "-V": False,
                    "-m": True
                },
                # For the DoomMusic StudioMDL compiler
                "DoomMusic": {
                    "-u": True,
                    "-V": False,
                    "-m": True
                },
                # For Xash3D engine mods
                "Xash3D": {
                    "-u": False,
                    "-V": False,
                    "-m": False
                }
            }
        }
        presetNames = list(self.presets["presets"].keys())
        self.presetSel = ttk.Combobox(master, values=presetNames)
        self.presetSel.current(self.options["defDPreset"])
        self.presetDat = self.presets["presets"][self.presetSel.get()]
        self.presetSel.bind("<<ComboboxSelected>>", self.setDP)
        # Checking if anything is exceeding the width of the "safe zone"
        """self.show()
        self.checkWidth()
        self.hide()"""
        # Tooltips
        self.themeTT = ToolTip(self.themeCBox, "Changes the program's theme, the built-in themes are: Freeman, Shephard, Calhoun and Cross.", background=thme["tt"], foreground=thme["txt"])
        self.startFolderTT = ToolTip(self.startFent, "Sets the directory that the built-in file explorer will start in, the default is the documents folder.", background=thme["tt"], foreground=thme["txt"])
        self.startFolderTT2 = ToolTip(self.setSF, "Sets the directory that the built-in file explorer will start in, the default is the documents folder.", background=thme["tt"], foreground=thme["txt"])
        self.forceDefTT = ToolTip(self.forceDefault, "By default, Snark prioritises the custom path you set over the default paths for compilers, enabling this will prioritise the default paths instead, meaning that Snark won't use the custom path if it finds the compiler in its default path.", background=thme["tt"], foreground=thme["txt"])
        self.hlmvTT = ToolTip(self.hlmvCBox, "Sets the model viewer you want to use when clicking the \"Open model in HLMV\" button, if this is set to None, the button will not show up!", background=thme["tt"], foreground=thme["txt"])
        self.setMVPtt = ToolTip(self.setMVP, "Sets the path to the model viewer you want to use if you select \"Other\"", background=thme["tt"], foreground=thme["txt"])
        if not startHidden:
            self.show()
        
        # Applying theme
        self.applyTheme(master)
        self.applyTheme(self.pageButtons)
    
    def checkWidth(self):
        curWidth = self.master.winfo_reqwidth()
        print(curWidth)
    
    def upgradeJSON(self):
        # Upgrade from version 1 to 4
        if self.options["version"] == 1:
            newOptions = {
                "defComp": 0,
                "defGame": 0,
                "defDPreset": 0,
                "forceDefPaths": self.options["forceDefPaths"],
                "save_paths": False,
                "startFolder": self.options["startFolder"],
                "theme": self.options["theme"],
                "gsMV": {
                    "selectedMV": 0,
                    "csPath": ""
                },
                "version": 4
            }
        # Upgrade from version 2 to 4
        elif self.options["version"] == 2:
            newOptions = {
                "defComp": 0,
                "defGame": 0,
                "defDPreset": 0,
                "forceDefPaths": self.options["forceDefPaths"],
                "save_paths": False,
                "startFolder": self.options["startFolder"],
                "theme": self.options["theme"],
                "gsMV": {
                    "selectedMV": self.options["gsMV"]["selectedMV"],
                    "csPath": self.options["gsMV"]["csPath"]
                },
                "version": 4
            }
        # Upgrade from version 3 to 4
        elif self.options["version"] == 3:
            newOptions = {
                "defComp": self.options["defComp"],
                "defGame": self.options["defGame"],
                "defDPreset": 0,
                "forceDefPaths": self.options["forceDefPaths"],
                "save_paths": False,
                "startFolder": self.options["startFolder"],
                "theme": self.options["theme"],
                "gsMV": {
                    "selectedMV": self.options["gsMV"]["selectedMV"],
                    "csPath": self.options["gsMV"]["csPath"]
                },
                "version": 4
            }
        # Save the JSON data of the new options
        self.options = newOptions
        self.save_options()
    
    def checkNewThemes(self):
        tList = os.listdir("themes/")
        tList.remove("template.jsonc")
        if len(tList) >= 1:
            return tList
        return False
    
    def genPg(self):
        self.curPage = 0
        self.setupLabel.grid(column=1, row=1, sticky="w")
        self.themeCBox.grid(column=2, row=1, sticky="w")
        self.nameLabel.grid(column=1, row=2, sticky="w")
        self.startFent.grid(column=2, row=2, sticky="w")
        self.setSF.grid(column=3, row=2, sticky="w")
        self.fdLabel.grid(column=1, row=3, sticky="w")
        self.forceDefault.grid(column=2, row=3, sticky="w")
        self.defCLabel.grid(column=1, row=4, sticky="w")
        self.compSel.grid(column=2, row=4, sticky="w")
        self.defGLabel.grid(column=1, row=5, sticky="w")
        self.defPLabel.grid(column=1, row=6, sticky="w")
        self.gameSel.grid(column=2, row=5, sticky="w")
        self.presetSel.grid(column=2, row=6, sticky="w")
        self.hlmvLabel.grid_remove()
        self.hlmvCBox.grid_remove()
        self.mvPathLabel.grid_remove()
        self.mvPathEnt.grid_remove()
        self.setMVP.grid_remove()
    
    def hlmvPg(self):
        self.curPage = 1
        self.setupLabel.grid_remove()
        self.themeCBox.grid_remove()
        self.nameLabel.grid_remove()
        self.startFent.grid_remove()
        self.setSF.grid_remove()
        self.fdLabel.grid_remove()
        self.forceDefault.grid_remove()
        self.defCLabel.grid_remove()
        self.compSel.grid_remove()
        self.defGLabel.grid_remove()
        self.defPLabel.grid_remove()
        self.gameSel.grid_remove()
        self.presetSel.grid_remove()
        self.hlmvLabel.grid(column=1, row=1, sticky="w")
        self.hlmvCBox.grid(column=2, row=1, sticky="w")
        self.mvPathLabel.grid(column=1, row=2, sticky="w")
        self.mvPathEnt.grid(column=2, row=2, sticky="w")
        self.setMVP.grid(column=3, row=2, sticky="w")
    
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
        self.applyTheme(self.pageButtons)
        self.themeTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.startFolderTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.startFolderTT2.changeTheme(newTheme["tt"], newTheme["txt"])
        self.forceDefTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.hlmvTT.changeTheme(newTheme["tt"], newTheme["txt"])
        self.setMVPtt.changeTheme(newTheme["tt"], newTheme["txt"])
    
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
    
    def chMVP(self):
        startDir = self.options["startFolder"]
        if startDir.startswith("~"):
            startDir = os.path.expanduser(startDir)
        if sys.platform == "win32":
            fileTypes = [("Windows Executable", "*.exe"), ("All Files", "*.*")]
        else:
            fileTypes = [("Executable Program", "*"), ("Windows Executable", "*.exe"), ("All Files", "*.*")]
        path = askopenfilename(title="Set executable for model viewer", initialdir=startDir, filetypes=fileTypes)
        if not path == "":
            if path.startswith("/home") and sys.platform == "linux":
                path = path[1:]
                pos = path.find("/", 5)
                tarLen = len(path) - pos
                while len(path) > tarLen:
                    path = path[1:]
                path = "~" + path
            print(path)
            self.mvPathVar.set(path)
            self.options["gsMV"]["csPath"] = path
            self.save_options()
            self.updFunc("gsMVcsPath", path)
    
    def setMV(self, e=False):
        opt = self.hlmvCBox.current()
        if opt > 1:
            self.mvPathEnt.unlock()
            self.mvPathVar.set(self.options["gsMV"]["csPath"])
        else:
            self.mvPathEnt.lock()
        self.options["gsMV"]["selectedMV"] = opt
        self.save_options()
        self.updFunc("gsMVselectedMV", opt)
    
    def setCmp(self, e=False):
        opt = self.compSel.current()
        self.options["defComp"] = opt
        self.save_options()
        self.updFunc("defComp", opt)
    
    def setGame(self, e=False):
        opt = self.gameSel.current()
        self.options["defGame"] = opt
        self.save_options()
        self.updFunc("defGame", opt)
    
    def setDP(self, e=False):
        opt = self.presetSel.current()
        self.options["defDPreset"] = opt
        self.save_options()
        self.updFunc("defDPreset", opt)
    
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
        if not key.startswith("gsMV"):
            self.options[key] = value
        else:
            self.options["gsMV"][key.replace("gsMV", "")] = value

    def hide(self):
        self.hidden = True
        for w in self.master.winfo_children():
            w.grid_remove()
    def show(self):
        self.hidden = False
        self.pageButtons.grid(row=0, column=1, sticky="nsew", columnspan=10)
        self.generalButton.grid(row=0, column=1, sticky="w")
        self.hlmvButton.grid(row=0, column=2, sticky="w")
        if self.curPage == 0:
            self.setupLabel.grid(column=1, row=1, sticky="w")
            self.themeCBox.grid(column=2, row=1, sticky="w")
            self.nameLabel.grid(column=1, row=2, sticky="w")
            self.startFent.grid(column=2, row=2, sticky="w")
            self.setSF.grid(column=3, row=2, sticky="w")
            self.fdLabel.grid(column=1, row=3, sticky="w")
            self.forceDefault.grid(column=2, row=3, sticky="w")
            self.defCLabel.grid(column=1, row=4, sticky="w")
            self.compSel.grid(column=2, row=4, sticky="w")
            self.defGLabel.grid(column=1, row=5, sticky="w")
            self.defPLabel.grid(column=1, row=6, sticky="w")
            self.gameSel.grid(column=2, row=5, sticky="w")
            self.presetSel.grid(column=2, row=6, sticky="w")
        elif self.curPage == 1:
            self.hlmvLabel.grid(column=1, row=1, sticky="w")
            self.hlmvCBox.grid(column=2, row=1, sticky="w")
            self.mvPathLabel.grid(column=1, row=2, sticky="w")
            self.mvPathEnt.grid(column=2, row=2, sticky="w")
            self.setMVP.grid(column=3, row=2, sticky="w")

class ScriptMenu():
    def __init__(self, template, master, startHidden:bool=False):
        self.curFont = font.nametofont('TkDefaultFont').actual()
        self.widthFix = 74
        self.conFix = 46
        self.conHeight = 11
        self.logOutput = False
        if self.curFont["family"].lower() == "nimbus sans l" or sys.platform == "win32":
            self.widthFix = 81
            self.conFix = 59
            self.conHeight = 13
        else:
            pass
        self.hidden = startHidden
        self.master = master
        thme = template.thme
        self.thme, self.safeWidth = thme, template.safeWidth
        if self.safeWidth > 609:
            n = 3
            self.widthFix, self.conFix = self.widthFix-n, self.conFix-n
        # Setting up options
        js = open("save/options.json", 'r')
        self.options = json.loads(js.read())
        js.close()
        self.scripts = []
        if getattr(sys, 'frozen', False):
            EXE_LOCATION = os.path.dirname( sys.executable )
        else:
            EXE_LOCATION = os.path.dirname( os.path.realpath( __file__ ) )
        self.scr_dir = os.path.join(EXE_LOCATION, "scripts")
        for s in os.listdir(self.scr_dir):
            if not s.startswith("template"):
                self.scripts.append(s)
        
        self.scr_list = Listbox(master, width=self.widthFix, selectmode=SINGLE)
        count = -1
        while count < len(self.scripts)-1:
            count += 1
            self.scr_list.insert(count, self.scripts[count])
        self.runBtn = Button(master, text="Run script", cursor="hand2", command=self.readScript)
        self.console = Console(master, 'Run a script and an output of the script\'s progress will appear here!', 0, 2, self.conFix, self.conHeight)
        if not startHidden:
            self.show()
        
        # Applying theme
        self.applyTheme(master)
    
    def readScript(self):
        selected_scr = self.scripts[int(self.scr_list.curselection()[0])]
        a = SSTReader(os.path.join(self.scr_dir, selected_scr), self.options, self.console)

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
    
    def updateOpt(self, key, value):
        if not key.startswith("gsMV"):
            self.options[key] = value
        else:
            self.options["gsMV"][key.replace("gsMV", "")] = value

    def hide(self):
        self.hidden = True
        for w in self.master.winfo_children():
            w.grid_remove()
    
    def show(self):
        self.hidden = False
        self.scr_list.grid(column=0, row=0, sticky=(W))
        self.runBtn.grid(column=0, row=1)
        self.console.show()