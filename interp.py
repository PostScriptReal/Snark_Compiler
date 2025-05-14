import json
import jsonc
from tkinter.filedialog import askopenfilename, askdirectory
import os
from menus import CompMenu, DecompMenu

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
        self.globalOut = dat["globalOutput"]
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

    def __init__(self, sst:str, opt:dict, logger):
        sstf = open(sst, 'r')
        scr = sstf.readlines()
        count = -1
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
        scrG = SSTGlobal(parsedSCR, opt)
        print("Data from SST file: ")
        print(f"Version: {header.version}")
        print(f"Format: {header.format}")
        print(f"Name: {scrG.name}")
        suffix = ""
        if parsedSCR["globalOutput"].startswith("askFolder"):
            suffix = "(generated path from askFolder)"
        print(f"Global Output Folder: {scrG.globalOut} {suffix}")


class SSTInterp:

    def __init__(self, logger, dat, globalVs, header):
        self.logger = logger
        self.dat = dat
        self.globalVs = globalVs
        self.header = header
        # This variable stores all available tasks and tells the Interpreter how to handle them
        self.cmds = {
            # This command is for compiling models
            "compile": {
                "func": self.cmpHnd,
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
    
    def cmpHnd(self):
        # This is a stub for now.
        pass
    
    def dCOMPHnd(self):
        # This is a stub for now.
        pass

    def hlmvHnd(self):
        # This is a stub for now.
        pass