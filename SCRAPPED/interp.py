import json
import jsonc
from tkinter.filedialog import askopenfilename, askdirectory
import os
import sys
import subprocess
# import yaml

# Class that gets information from the script header (the lines of text sandwiched inbetween the dashes)
class SSTVer:

    def __init__(self, dat:list):
        self.version = 0
        self.format = 'json'
        count = -1
        end = dat.index('-', 2)
        print(end)
        for l in dat:
            count += 1
            if count == 0:
                continue
            elif l.startswith('version'):
                # Getting the last letter in the line, which is the version number.
                self.version = int(l[len(l)-1:])
            elif l.startswith('format'):
                frmt = l.replace('format ', '')
                self.format = frmt
            elif l == '-':
                break
        self.script = dat[end+1:]
        # Converting the list into a readable string
        self.script = "\n".join(self.script)

# Class for reading the non-functional part of the script, the 'Global variables'.
class SSTGlobal:

    def __init__(self, dat:dict, opt:dict):
        self.name = dat["name"]
        self.defProf = dat.get("defComp", None)
        self.defDec = dat.get("defDecPreset", None)
        self.globalOut = dat.get("globalOutput", None)
        if self.globalOut.startswith('askFolder'):
            # Getting start directory
            startDir = opt["startFolder"]
            if startDir.startswith("~"):
                startDir = os.path.expanduser(startDir)
            # Checking if user has specified a title
            oTitle = "Select Output Folder"
            if self.globalOut.find(',') != -1:
                oTitle = self.globalOut.split(',')[1]
            self.globalOut = askdirectory(title=oTitle, initialdir=startDir)

# Reader for SST (Snark ScripT) files
class SSTReader:

    def __init__(self, sst:str, opt:dict, logger, options:dict):
        sstf = open(sst, 'r')
        scr = sstf.readlines()
        count = -1
        error = False
        for l in scr:
            count += 1
            scr[count] = l.replace('\n', '')
        header = SSTVer(scr)
        parsedSCR = None
        if header.format == 'jsonc':
            print(header.script)
            parsedSCR = jsonc.loads(header.script)
        elif header.format == 'json':
            print(header.script)
            parsedSCR = json.loads(header.script)
        elif header.format == 'yaml' or header.format == 'yml':
            print(header.script)
            parsedSCR = yaml.safe_load(header.script)
        else:
            logger.append("Fatal error: Format specified in header is not json, jsonc, or yaml/yml.")
            error = True
        if not error:
            scrG = SSTGlobal(parsedSCR, opt)
            print("Data from SST file: ")
            print(f"Version: {header.version}")
            print(f"Format: {header.format}")
            print(f"Name: {scrG.name}")
            suffix = ""
            if parsedSCR["globalOutput"].startswith("askFolder"):
                suffix = "(generated path from askFolder)"
            print(f"Global Output Folder: {scrG.globalOut} {suffix}")
            intrp = SSTInterp(logger, parsedSCR["tasks"], scrG, header, options)


class SSTInterp:

    def __init__(self, logger, dat, globalVs, header, options):
        self.logger = logger
        self.dat = dat
        self.globalVs = globalVs
        self.header = header
        self.options = options
        self.tskCnt = 0
        # This variable stores all available tasks and tells the Interpreter how to handle them
        self.cmds = {
            # This command is for compiling models
            "compile": {
                "func": self.cmpHnd,
                # First array: Type?, Accepted inputs, Options
                # Second array: 
                "args": [["file", "file", ".mdl"], ["output", "folder"]]
            },
            # This command is for decompiling models
            "decompile": {
                "func": self.dCMPHnd,
                "args": [["file", "file", ".mdl"], ["output", "folder"]]
            },
            "view": {
                "func": self.hlmvHnd,
                "args": [["file", "file+task", ".mdl"]]
            }
        }
        logger.append(f"Starting Script \'{globalVs.name}\'")
    
    def taskToValue(self, tsk:str, grab:str):
        for t in self.dat:
            if t["name"] == tsk:
                return t[grab]
        # If a value could not be found, return nothing.
        return None
    
    # Functions for each instruction defined in self.cmds
    def cmpHnd(self):
        # This is a stub for now.
        pass
    
    def dCOMPHnd(self):
        # This is a stub for now.
        pass

    def hlmvHnd(self, dat):
        file = ""
        genByTask = False
        if dat["file"].endswith(".mdl"):
            file = dat["file"]
        else:
            file = self.taskToValue(dat["file"], "output")
            genByTask = True
        
        if file != None:
            if not genByTask:
                self.hlmvTsk(file, False)
            else:
                self.hlmvTsk(file, True, dat["file"])
        else:
            self.logger.append(f"Error: Couldn't find model generated by compile task \'{dat["file"]}\'")
            self.logger.append(f"From: view task \'{dat["name"]}\' (index {self.tskCnt})")
    
    def hlmvTsk(self, f, genByTask:bool, task=""):
        if genByTask:
            self.logger.append(f"Viewing model generated by compile task: \'{task}\'")
        else:
            self.logger.append(f"Viewing model \'{os.path.basename(f)}\'")
        # If "Half-Life Asset Manager" is selected
        if self.options["gsMV"]["selectedMV"] == 1:
            if sys.platform == "linux":
                a = subprocess.getoutput(f"XDG_SESSION_TYPE=x11 hlam \"{f}\"")
            else:
                a = subprocess.getoutput(f"\"C:/Program Files (x86)/Half-Life Asset Manager/hlam.exe\" \"{f}\"")
        # If "Other" option is selected
        elif self.options["gsMV"]["selectedMV"] > 1:
            if sys.platform == "linux":
                path = self.options["gsMV"]["csPath"]
                path = os.path.expanduser(path)
                if path.endswith(".exe"):
                    a = subprocess.getoutput(f"wine \"{path}\" \"{f}\"")
                else:
                    a = subprocess.getoutput(f"\"{path}\" \"{f}\"")
            else:
                path = self.options["gsMV"]["csPath"]
                a = subprocess.getoutput(f"\"{path}\" \"{f}\"")