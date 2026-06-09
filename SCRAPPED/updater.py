from tkinter import *
import json
import os
from tkinter import ttk
from tkinter.filedialog import askopenfilename, askdirectory
from datetime import datetime as date
import calendar
from py7zr import SevenZipFile
import shutil

class ChangelogViewer(Tk):

    def get_options(self):
        try:
            jsf = open('save/options.json', 'r')
            js = jsf.read()
            jsf.close()
            self.options = json.loads(js)
        except:
            print("UH OH!")
    
    def getVersion(self):
        url = "https://github.com/PostScriptReal/Snark_Compiler/raw/refs/heads/main/version.txt"
        if CheckThereIsConnection():
            webVer = urlopen(url, context=ssl.create_default_context(cafile=certifi.where())).read().decode('utf-8')
            print(webVer)

            # Don't you dare make a Fortnite joke
            vFile = open("version.txt", "r")
            curVer = vFile.read()
            ver = curVer.split('-')
            curVer = ver[0]
            return curVer

    def __init__(self, theme):
        super().__init__()
        self.devMode = True
        self.title("What's New!")
        self.get_options()
        try:
            self.selTheme = self.options["theme"]
        except:
            self.selTheme = 'Freeman'
		
        thCol = theme
        self.thme = thCol
        self.frame = Frame(self, borderwidth=2, relief="sunken", bg=thCol["bg"])
        self.frame.grid(column=0, row=0, sticky=(N, E, S, W))
        self.config(background=thCol["bg"])
        with open('changelog.txt', 'r') as changelog:
            self.changelog = changelog.readlines()
        self.patchNotes = ""
        try:
            verCheck = self.changelog.index(f"[{self.getVersion}]\n")
            count = verCheck
            for l in self.changelog:
                count += 1
                if l.startswith('['):
                    break
                else:
                    self.patchNotes += l
        except:
            try:
                verCheck = self.changelog.index('[unreleased]\n')
                count = verCheck
                for l in self.changelog:
                    count += 1
                    if l.startswith('[') and count > 1:
                        break
                    else:
                        self.patchNotes += l
            except:
                print('Can\'t get the latest version, stopping...')
                return
        self.viewer = Text(self.frame, width=90, height=20)
        self.viewer.insert('1.0', self.patchNotes)
        self.viewer['state'] = 'disabled'
        self.viewer.grid(column=0, row=0, sticky="nsew")

        # Applying theme
        self.applyTheme(self.frame)
    
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
    
    def viewChangelog(self):
        pass
    
    def startOnlineInstall(self):
        pass
    
    def startOfflineInstall(self):
        pass

class Updater(Tk):

    # Checking the date for events such as: Snark's Anniversary and my birthday.
    def checkDate(self, event:str):
        day = '%d'
        month = '%m'
        year = '%Y'
        dateObj = date.now()
        curDate = {
            "day": int(dateObj.strftime(day)), 
            "month": int(dateObj.strftime(month)), 
            "year": int(dateObj.strftime(year))
        }
        age = 0
        # Btw there is no check if the number is under 1, so have fun with that nugget of information!
        if event.lower() == "birthday":
            age = curDate["year"] - 2006
        elif event.lower() == "anniversary":
            age = curDate["year"] - 2025
        
        numSuffix = "th"
        if str(age).endswith("1"):
            numSuffix = 'st'
        elif str(age).endswith("2"):
            numSuffix = 'nd'
        elif str(age).endswith("3"):
            numSuffix = 'rd'

        if event.lower() == "birthday":
            if curDate["day"] >= 11 and curDate["day"] < 18 and curDate["month"] == 9:
                return True
        elif event.lower() == "anniversary":
            if calendar.isleap(curDate["year"]):
                if curDate["day"] >= 26 and curDate["month"] == 2 or curDate["day"] < 3 and curDate["month"] == 3:
                    return True
            else:
                if curDate["day"] >= 26 and curDate["month"] == 2 or curDate["day"] < 4 and curDate["month"] == 3:
                    return True
        return False

    def get_options(self):
        try:
            jsf = open('save/options.json', 'r')
            js = jsf.read()
            jsf.close()
            self.options = json.loads(js)
        except:
            print("UH OH!")
    
    def snarkAnimLoop(self):
        self.animCount += 1
        if self.animCount >= len(self.snarkAnim):
            self.animCount = 0
        self.snark.config(image=self.snarkAnim[self.animCount])
        if self.animateSnark:
            self.frame.after(400, self.snarkAnimLoop)
        else:
            self.snark.config(image=self.snarkAnim[0])
            self.animCount = -1

    def __init__(self):
        super().__init__()
        self.devMode = True
        self.title("Snark Updater")
        self.get_options()
        try:
            self.selTheme = self.options["theme"]
        except:
            self.selTheme = 'Freeman'
        
        # Loading in window icon
        ico = PhotoImage(file="icon-linux.png")
        self.iconphoto(True, ico)
		
        thCol = {}
        # Defining colours for the theme
        if self.selTheme == "Freeman":
            thCol = {
                "bg": "#ff862d",
                # First value is inactive colour, 2nd hover and 3rd being the active colour
                "btn": ["#eb6524", "#ed763c", "#ee8d5e"],
                "ent": "#e3573d",
                "txt": "white",
                "tt": "#dc5200"
            }
        elif self.selTheme == "Shephard":
            thCol = {
                "bg": "#11da00",
                # First value is inactive colour, 2nd hover and 3rd being the active colour
                "btn": ["#27be07", "#2ad008", "#31e50c"],
                "ent": "#4dc011",
                "txt": "white",
                "tt": "#14a000"
            }
        elif self.selTheme == "Calhoun":
            thCol = {
                "bg": "#4741ff",
                # First value is inactive colour, 2nd hover and 3rd being the active colour
                "btn": ["#1f2deb", "#333fec", "#4f5aed"],
                "ent": "#5074e6",
                "txt": "white",
                "tt": "#0006f8"
            }
        elif self.selTheme == "Cross":
            thCol = {
                "bg": "#ff362d",
                # First value is inactive colour, 2nd hover and 3rd being the active colour
                "btn": ["#eb242f", "#ed3c46", "#ee5e66"],
                "ent": "#e33d63",
                "txt": "white",
                "tt": "#dc0002"
            }
        else:
            if os.path.exists(f'themes/{self.selTheme}.jsonc'):
                fp = open(f'themes/{self.selTheme}.jsonc', 'r')
                thCol = jsonc.load(fp)
            elif os.path.exists(f'themes/{self.selTheme}.json'):
                fp = open(f'themes/{self.selTheme}.json', 'r')
                thCol = json.loads(fp.read())
            else:
                print('Cannot find the theme, is it a .json or .jsonc file?')
                print('Defaulting to the Freeman theme.')
                thCol = {
                    "bg": "#ff862d",
                    # First value is inactive colour, 2nd hover and 3rd being the active colour
                    "btn": ["#eb6524", "#ed763c", "#ee8d5e"],
                    "ent": "#e3573d",
                    "txt": "white",
                    "tt": "#dc5200"
                }
        self.thme = thCol
        self.frame = Frame(self, borderwidth=2, relief="sunken", bg=thCol["bg"])
        self.frame.grid(column=0, row=0, sticky=(N, E, S, W))
        self.config(background=thCol["bg"])
        self.animCount = -1
        if self.checkDate('Birthday'):
            self.snarkAnim = [PhotoImage(file="images/UpdaterSnark/birthday1.png"), PhotoImage(file="images/UpdaterSnark/birthday2.png")]
            self.snark = Label(self.frame, image=self.snarkAnim[0], width=128, height=128)
        elif self.checkDate('Anniversary'):
            self.snarkAnim = [PhotoImage(file="images/UpdaterSnark/anniversary1.png"), PhotoImage(file="images/UpdaterSnark/anniversary2.png")]
            self.snark = Label(self.frame, image=self.snarkAnim[0], width=136, height=128)
        else:
            self.snarkAnim = [PhotoImage(file="images/UpdaterSnark/normal1.png"), PhotoImage(file="images/UpdaterSnark/normal2.png")]
            self.snark = Label(self.frame, image=self.snarkAnim[0], width=128, height=128)
        self.snark.image = self.snarkAnim[0]
        self.snark.grid(column=0,row=0, sticky=(N))
        self.animateSnark = False
        self.welcome = Label(self.frame, text="Welcome to the Snark Updater!\nTo update, click one of the two options below \'View Changelog\'.")
        self.welcome.grid(column=0,row=1,padx=5)
        self.changelogViewer = Button(self.frame, text="View Changelog", command=self.viewChangelog, bg=thCol["btn"][0], cursor="hand2")
        self.changelogViewer.grid(column=0, row=2, sticky="we", padx=5, pady=5)
        self.installOnline = Button(self.frame, text="Update Online", command=self.startOnlineInstall, bg=thCol["btn"][0], cursor="hand2")
        self.installOnline.grid(column=0, row=3, sticky="we", padx=5, pady=5)
        self.installOffline = Button(self.frame, text="Update From File", command=self.startOfflineInstall, bg=thCol["btn"][0], cursor="hand2")
        self.installOffline.grid(column=0, row=4, sticky="we", padx=5, pady=5)
        self.menusToRemove = [self.welcome, self.changelogViewer, self.installOnline, self.installOffline]
        self.menusGridInfo = [1, 2, 3, 4]
        self.updatingText = Label(self.frame, text="Downloading patch file...", width=49)

        # Applying theme
        self.applyTheme(self.frame)
    
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
    
    def viewChangelog(self):
        v = ChangelogViewer(self.thme)
    
    def startOnlineInstall(self):
        pass
    
    def startOfflineInstall(self):
        fileType = [("Patch Archive", "*.7z")]
        path = askopenfilename(title="Please locate the patch file", initialdir=os.getcwd(), filetypes=fileType)
        print(path)
        self.updatingText.configure(text="Extracting patch file...")
        for m in self.menusToRemove:
            m.grid_remove()
        self.animateSnark = True
        self.snarkAnimLoop()
        self.updatingText.grid(column=0, row=1, padx=2)
        self.patchCount = -1
        self.extractionPath = os.path.join(os.getcwd(), 'UPDATE')
        if path == ():
            self.resetGUI()
        else:
            try:
                with SevenZipFile(path, 'r') as f:
                    f.extractall(path=self.extractionPath)
                self.updatingText.configure(text="Installing update...")
                for f in os.listdir(self.extractionPath):
                    if not os.path.isdir(f):
                        originalF = os.path.join(os.getcwd(), f)
                        if os.path.exists(originalF):
                            os.remove(originalF)
                        shutil.copy(os.path.join(self.extractionPath, f), originalF)
                    else:
                        originalDir = os.path.join(os.getcwd(), f)
                        # I WILL NEVER UNDERSTAND HOW PYTHON CAN'T TELL THAT A LINUX EXECUTABLE IS A FILE AND INSTEAD THINKS IT'S A DIRECTORY
                        # DO THE DEVELOPERS NOT USE LINUX, OR HAVE THEY NOT IMPLEMENTED THE PROPER CHECKS!? I DON'T GET IT!!
                        try:
                            for folderName, subfolders, filenames in os.walk(f):
                                for filename in filenames:
                                    filePath = os.path.join(folderName, filename)
                                    newPath = os.path.join(originalDir, filename)
                                    if not os.path.exists(originalDir):
                                        os.mkdir(originalDir)
                                    if os.path.exists(newPath):
                                        os.remove(newPath)
                                    shutil.copy(filePath, newPath)
                        except:
                            pass
                shutil.rmtree(self.extractionPath)
                self.updatingText.configure(text="Done!")
                print("Done!")
                self.frame.after(5000, self.resetGUI)
            except Exception as e:
                print(e)
                self.updatingText.configure(text=f"Update failed with error:\n{e}")
                self.frame.after(5000, self.resetGUI)
        # self.offlineUpdatingText()
    
    def resetGUI(self):
        self.updatingText.grid_remove()
        self.animateSnark = False
        for m in self.menusToRemove:
            item = self.menusToRemove.index(m)
            if item == 0:
                m.grid(column=0, row=self.menusGridInfo[item], padx=5)
            else:
                m.grid(column=0, row=self.menusGridInfo[item], padx=5, pady=5)
    
    def offlineUpdatingText(self):
        self.patchCount += 1
        if self.patchCount == 0:
            self.updatingText.configure(text="Extracting patch file...")
        elif self.patchCount == 1:
            self.updatingText.configure(text="Installing update...")
        elif self.patchCount == 2:
            self.updatingText.configure(text="Done!")
        elif self.patchCount >= 3:
            self.updatingText.grid_remove()
            self.animateSnark = False
            self.patchCount = -1
            for m in self.menusToRemove:
                item = self.menusToRemove.index(m)
                if item == 0:
                    m.grid(column=0, row=self.menusGridInfo[item], padx=5)
                else:
                    m.grid(column=0, row=self.menusGridInfo[item], padx=5, pady=5)
                
        self.frame.after(5000, self.offlineUpdatingText)

gui = Updater()
gui.mainloop()