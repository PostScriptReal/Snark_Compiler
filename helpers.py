from tkinter import *
from tkinter import ttk
import os
from tkinter.filedialog import askopenfilename, askdirectory
import subprocess
import shutil

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
        self.decomp = Button(master, text='Decompile', command=self.startDecomp)
        self.console = Console(master, 'Start a decompile and the terminal output will appear here!', 0, 3, 50, 10)
        if not startHidden:
            self.setupLabel.grid(column=0, row=0, sticky=(W))
            self.nameLabel.grid(column=0, row=1, sticky=(W))
            self.nameEntry.grid(column=1, row=0, padx=(5, 0))
            self.outputEntry.grid(column=1, row=1, padx=(5,0))
            self.mdlBrowse.grid(column=2, row=0, padx=(6,0))
            self.outBrowse.grid(column=2, row=1, padx=(6,0))
            self.decomp.grid(column=0, row=2, pady=(20,0))
            self.console.show()
        
        # Applying theme
        for w in master.winfo_children():
            if w.winfo_class() == "Button":
                w.configure(bg=thme["btn"][0])
                w.configure(highlightbackground=thme["btn"][1])
                w.configure(activebackground=thme["btn"][2])
                w.configure(fg=thme["txt"])
            elif w.winfo_class() == "Entry":
                pass
                # w.configure(bg=thme["ent"])
            elif isinstance(w, ttk.Combobox):
                pass
                w.configure(foreground='black')
                # w["menu"].config(bg=thme["btn"][1])
            elif isinstance(w, Text):
                w.configure(bg=thme["ent"])
                w.configure(fg=thme["txt"])
            else:
                w.configure(bg=thme["bg"])
                try:
                    w.configure(fg=thme["txt"])
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
        self.nameEntry.grid(column=1, row=0, padx=(5, 0))
        self.outputEntry.grid(column=1, row=1, padx=(5,0))
        self.mdlBrowse.grid(column=2, row=0, padx=(6,0))
        self.outBrowse.grid(column=2, row=1, padx=(6,0))
        self.decomp.grid(column=0, row=2, pady=(20,0))
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
        tOutput = subprocess.getoutput(f'./third_party/mdldec \"{mdl}\"')
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
        