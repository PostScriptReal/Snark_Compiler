import json
from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import font
import os
from os.path import *
import importlib.machinery
import importlib.util
from pathlib import Path
# OH MY GOD MARIO REFERENCE!!?!
import webbrowser as browser
import sys
from urllib.request import urlopen
from helpers import *
from menus import *

selected_scr = ''
scr_dat = ''

class Flags:

	def __init__(self):
		# Enables Developer mode, which disables automatic updates and enables extra logging
		self.devMode = True
		# Flag specifically for Snark, scripts are currently not implemented yet and is a copy of the scripting system from SMD Tools v1.1
		# This will allow me to disable the functionality for it until I come up with a proper implementation
		self.allowScripts = False

class Interp:

	def __init__(self, scr_ref):
		self.err = False
		self.scr_ref = "scripts/" + scr_ref + '.txt'
		if not os.path.exists(self.scr_ref):
			print("How did we get here?")
			self.err = True
		else:
			self.interp()

	def nl_clean(self, smd):
		count = -1
		for l in smd:
			count += 1
			smd[count] = l[:-l.count("\n")]
		return smd

	def interp(self):
		global scr_dat
		global guii
		scr_f = open(self.scr_ref, 'r')
		scr = self.nl_clean(scr_f.readlines())
		self.mode = ''
		if scr[0] == 'mode dupe':
			self.mode = 'd'
		elif scr[0] == 'mode mat':
			self.mode = 'm'
		elif scr[0] == 'mode bmp':
			self.mode = 'b'
		else:
			self.mode = None
		print("Before: "+ str(scr))
		scr.pop(0)
		scr.pop(len(scr) - 1)
		print("After: "+ str(scr))
		print(scr)
		scr_dat = [self.mode, scr]
		guii.exec_script(scr_dat)

class ScriptWin:

	def __init__(self):
		self.nroot = Tk()
		self.win()
		self.nroot.mainloop()

	def win(self):
		self.flags = Flags()
		self.nroot.title("Scripts")

		frame = Frame(self.nroot, borderwidth=2, relief="sunken")
		frame.grid(column=1, row=1, sticky=(N, E, S, W))
		self.nroot.columnconfigure(1, weight=1)
		self.nroot.rowconfigure(1, weight=1)

		if self.flags.allowScripts:
			self.scripts = []
			if getattr(sys, 'frozen', False):
				EXE_LOCATION = os.path.dirname( sys.executable )
			else:
				EXE_LOCATION = os.path.dirname( os.path.realpath( __file__ ) )
			scr_dir = os.path.join(EXE_LOCATION, "scripts")
			for s in os.listdir(scr_dir):
				self.scripts.append(s.replace('.txt', ''))
			print(self.scripts)

			self.scr_list = Listbox(frame)
			self.scr_list.grid(column=1, row=1, sticky=(N, S, E, W), padx=40, pady=(40, 0), rowspan=5)
			count = 0
			for n in self.scripts:
				count += 1
				self.scr_list.insert(count, n)

			select_scr = Button(frame, text="Select", command=self.select)
			select_scr.grid(column=1, row=6, sticky=(S))
		else:
			b_smd = Label(frame, text=f"Proper script functionality will be implemented in a future release,\nfor now though, the script button is here so I don't have to\ncompletely remodel the GUI with its removal.")
			b_smd.grid(column=1, row=1, sticky=(S), padx=25, pady=25)

			select_scr = Button(frame, text="I understand", command=self.close)
			select_scr.grid(column=1, row=6, sticky=(S))
	def close(self):
		self.nroot.destroy()

	def select(self):
		global selected_scr
		selected_scr = self.scripts[int(self.scr_list.curselection()[0])]
		print(selected_scr)
		scr_interp = Interp(selected_scr)
		self.nroot.destroy()

class OptWin:

	def __init__(self):
		self.nroot = Tk()
		self.win()
		self.nroot.mainloop()

	def win(self):
		self.nroot.title("Options")

		frame = Frame(self.nroot, borderwidth=2, relief="sunken")
		frame.grid(column=1, row=1, sticky=(N, E, S, W))
		self.nroot.columnconfigure(1, weight=1)
		self.nroot.rowconfigure(1, weight=1)

		jsf = open('save/options.json', 'r')
		js = jsf.read()
		self.options = json.loads(js)

		self.b_smd_val = BooleanVar(frame, value=self.options["backup_smd"])
		print(self.b_smd_val.get())
		b_smd = Checkbutton(frame, text="Backup SMDs", variable=self.b_smd_val, command=self.set_backup_smd)
		b_smd.grid(column=1, row=1, sticky=(S), padx=50, pady=40)

		"""self.s_vals_val = BooleanVar(frame, value=self.options["save_paths"])
		s_vals = Checkbutton(frame, text="Save User Inputs", variable=self.s_vals_val, command=self.set_save_values)
		s_vals.grid(column=1, row=1, sticky=(S), padx=50, pady=60)"""

		select_scr = Button(frame, text="Confirm", command=self.confirm_opts)
		select_scr.grid(column=1, row=6, sticky=(S))
	
	def set_backup_smd(self):
		self.options["backup_smd"] = self.b_smd_val.get()
		print(self.options["backup_smd"])
	
	def set_save_values(self):
		self.options["save_paths"] = self.s_vals_val.get()
		print(self.options["backup_smd"])
	
	def confirm_opts(self):
		newjson = json.dumps(self.options, sort_keys=True, indent=5)
		opts = open('save/options.json', 'w')
		opts.write(newjson)
		opts.close()
		self.nroot.destroy()

class GetNewVersion:

	def __init__(self, version):
		self.nroot = Tk()
		v = version.split("-")[0]
		self.win(v)
		self.nroot.mainloop()

	def win(self, ver):
		self.nroot.title(f"Version {ver} is out!")

		frame = Frame(self.nroot, borderwidth=2, relief="sunken")
		frame.grid(column=1, row=1, sticky=(N, E, S, W))
		self.nroot.columnconfigure(1, weight=1)
		self.nroot.rowconfigure(1, weight=1)
		buttons = Frame(frame, borderwidth=2)
		buttons.grid(column=1, row=1, sticky=(S), columnspan=10)

		text = Label(frame, text="A new version of Snark has been released,\n do you want to update to the new version?")
		text.grid(column=1, row=0, padx=50, pady=40)

		self.dlButton = Button(buttons, text="Yes", command=self.releasesPage)
		self.dlButton.grid(column=0, row=1, sticky=(S))
		self.noButton = Button(buttons, text="No", command=self.closeWin)
		self.noButton.grid(column=1, row=1, sticky=(S))
	
	def releasesPage(self):
		browser.open_new_tab("https://github.com/PostScriptReal/Snark_Compiler/releases/latest")
		self.nroot.destroy()
	
	def closeWin(self):
		self.nroot.destroy()
	
	def confirm_opts(self):
		newjson = json.dumps(self.options, sort_keys=True, indent=5)
		opts = open('save/options.json', 'w')
		opts.write(newjson)
		opts.close()
		self.nroot.destroy()

class About:

	def __init__(self, ver):
		self.nroot = Tk()
		self.win(ver)
		self.nroot.mainloop()

	def win(self, ver):
		self.nroot.title("About Snark")
		frame = Frame(self.nroot, borderwidth=2, relief="sunken")
		frame.grid(column=1, row=1, sticky=(N, E, S, W))
		self.nroot.columnconfigure(1, weight=1)
		self.nroot.rowconfigure(1, weight=1)

		b_smd = Label(frame, text=f"Snark {ver}")
		b_smd.grid(column=1, row=1, sticky=(S), padx=25, pady=25)

		select_scr = Button(frame, text="Close", command=self.close)
		select_scr.grid(column=1, row=6, sticky=(S))
	
	def close(self):
		self.nroot.destroy()

class GUI(Tk):
	def get_options(self):
		jsf = open('save/options.json', 'r')
		js = jsf.read()
		jsf.close()
		count = -1
		newjs = ''
		for l in js:
			if l.find('//') != -1:
				js.pop(count)
				continue
			newjs += l
		if not js[len(js)-1] == '}':
			newjs += '}'
		self.options = json.loads(newjs)
	
	def check_version(self):
		url = "https://github.com/PostScriptReal/PS-SMD-Tools/raw/refs/heads/main/version.txt"
		webVer = urlopen(url).read().decode('utf-8')
		print(webVer)

		# Don't you dare make a Fortnite joke
		vFile = open("version.txt", "r")
		curVer = vFile.read()

		if curVer != webVer:
			a = GetNewVersion(webVer)

	def __init__(self):
		super().__init__()
		self.flags = Flags()
		# Set Window title
		self.title("Snark")
		if sys.platform == 'linux':
			self.fixGUI = True
			self.geometry("609x491")
		else:
			self.fixGUI = False
			self.geometry("569x411")
		self.selTheme = "Cross"
		
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
		# Get Options
		self.get_options()
		if self.options["save_paths"]:
			self.save_paths = True
			js = open("save/paths.json", 'r')
			self.sPaths = json.loads(js.read())
			self.bonez = self.sPaths["bonez"]
			self.matfix = self.sPaths["matFix"]
		else:
			self.save_paths = False

		widgets = []
		buttons = []

		# Create Window
		frame = Frame(self, borderwidth=2, relief="sunken", bg=thCol["bg"])
		frame.grid(column=6, row=2, sticky=(N, E, S, W))
		header = Frame(frame, borderwidth=2, bg=thCol["bg"])
		header.grid(column=1, row=1, sticky=(N, W, E), columnspan=69)
		mtbtns = Frame(frame, borderwidth=2, bg=thCol["bg"])
		mtbtns.grid(column=1, row=9, sticky=(S), columnspan=10)
		menu = Frame(frame, borderwidth=2, bg=thCol["bg"])
		menu.grid(column=0, row=2, sticky=(W, S), columnspan=10)
		self.dumbFixMenu = Frame(frame, borderwidth=2, bg=thCol["bg"])
		self.columnconfigure(6, weight=1)
		self.rowconfigure(2, weight=1)

		# Create Header Buttons
		self.dupe_button = Button(header, text="Games", command=self.bd_menu, bg=thCol["btn"][0])
		self.dupe_button.grid(column=0, row=0, sticky=(N))

		self.cmpiler_button = Button(header, text="Compilers", command=self.bd_menu, bg=thCol["btn"][0])
		self.cmpiler_button.grid(column=1, row=0, sticky=(N))

		self.mat_button = Button(header, text="Decompile", command=self.mnc_menu, bg=thCol["btn"][0])
		self.mat_button.grid(column=2, row=0, sticky=(N))

		self.comp_button = Button(header, text="Compile", command=self.cmp_menu, bg=thCol["btn"][0])
		self.comp_button.grid(column=3, row=0, sticky=(N))

		self.scripts = Button(header, text="Scripts", command=self.scripts, bg=thCol["btn"][0])
		self.scripts.grid(column=4, row=0, sticky=(N))
		
		self.options = Button(header, text="Options", command=self.optionsMenu, bg=thCol["btn"][0])
		self.options.grid(column=6, row=0, sticky=(N))

		self.help = Button(header, text="Help", command=self.help, bg=thCol["btn"][0])
		self.help.grid(column=7, row=0, sticky=(N))
		
		self.aboutB = Button(header, text="About", command=self.about)
		self.aboutB.grid(column=5, row=0, sticky=(N))

		self.setupMenu = SetupMenu(menu, thCol)
		self.decMenu = DecompMenu(menu, thCol, True)
		self.cmpMenu = CompMenu(self.dumbFixMenu, thCol, True)

		"""self.tile_label = Label(frame, text="Path to SMDs")
		self.tile_label.grid(column=2, row=3)

		self.path = StringVar()
		if self.save_paths and not self.bonez["path"] == "":
			self.path.set(self.bonez["path"])
		self.tname_entry = Entry(frame, textvariable=self.path, width=50)
		self.tname_entry.grid(column=3, row=3, sticky=(E, W))

		self.save_button = Button(frame, text="Open QC", command=self.openfile)
		self.save_button.grid(column=5, row=3, sticky=(S))

		self.dir_button = Button(frame, text="Open Folder", command=self.opendir)
		self.dir_button.grid(column=7, row=3, sticky=(S))

		self.base_label = Label(frame, text="Select Base Bone")
		self.base_label.grid(column=2, row=5, sticky=(S))

		self.b_bone = StringVar()
		self.bname_entry = Entry(frame, textvariable=self.b_bone, width=50)
		self.bname_entry.grid(column=3, row=5, sticky=(N))

		self.new_label = Label(frame, text="Select New Bone")
		self.new_label.grid(column=2, row=6, sticky=(S))

		self.n_bone = StringVar()
		self.nname_entry = Entry(frame, textvariable=self.n_bone, width=50)
		self.nname_entry.grid(column=3, row=6, sticky=(N))

		self.parent_label = Label(frame, text="Select Parent Bone")
		self.parent_label.grid(column=2, row=7, sticky=(S))

		self.p_bone = StringVar()
		self.pname_entry = Entry(frame, textvariable=self.p_bone, width=50)
		self.pname_entry.grid(column=3, row=7, sticky=(N, E, W))

		self.action_button = Button(mtbtns, text="Dupe", command=self.dupe)
		self.action_button.grid(column=1, row=9, sticky=(S))

		self.bmp_button = Button(mtbtns, text="File Ext", command=self.bmp)
		self.matrn_button = Button(mtbtns, text="Fix Pointer", command=self.matrename)

		self.ref_label = Label(frame, text="Type Finder Value")

		self.ref = StringVar()
		self.ref_entry = Entry(frame, textvariable=self.ref, width=50)

		self.rename_label = Label(frame, text="String Part To Rename")

		self.rename = StringVar()
		self.rename_entry = Entry(frame, textvariable=self.rename, width=50)

		self.replace_label = Label(frame, text="String Part To Replace")

		self.replace = StringVar()
		self.replace_entry = Entry(frame, textvariable=self.replace, width=50)"""

		vnum = open('version.txt', "r")
		self.ver = vnum.read().replace("(OS)", sys.platform)
		version = Label(frame, text=self.ver, background=thCol["bg"], fg=thCol["txt"])
		version.grid(column=0, row=69, sticky=(W, S), columnspan=2)

		# Applying theme
		for w in header.winfo_children():
			w.configure(bg=thCol["btn"][0])
			w.configure(highlightbackground=thCol["btn"][1])
			w.configure(activebackground=thCol["btn"][2])
			try:
				w.configure(fg=thCol["txt"])
			except:
				pass

		if not self.flags.devMode:
			self.check_version()

	def help(self):
		browser.open_new_tab('https://github.com/PostScriptReal/Snark_Compiler/wiki')
	
	def about(self):
		a = About(self.ver)
	
	def openfile(self):
		# startdir = self.options["startFolder"]
		startDir = os.path.expanduser("~/Documents")
		fileTypes = [("Quake Compile Files", "*.qc"), ("All Files", "*.*")]
		self.path.set(askopenfilename(title="Select QC", initialdir=startDir, filetypes=fileTypes))
		self.qcDATA = QCHandler(self.path.get())
		self.qcDATA.get_bodygroups()
		self.qcDATA.getAnimFolder()
		self.mdls = self.qcDATA.bodies
		self.anims = self.qcDATA.animPath
	def opendir(self):
		# startdir = self.options["startFolder"]
		startDir = os.path.expanduser("~/Documents")
		self.path.set(askdirectory(title="Select Anims Folder", initialdir=startDir))

	def dupe(self):
		# Initialising Bone Duping function
		inst = Dupe()
		# Grabbing all values from input boxes
		qcSelect = QCWin(self.qcDATA, inst, 'd', [self.b_bone.get(),self.n_bone.get(),self.p_bone.get()])
		""""if qcSelect.finished:
			loc = self.path.get()
			base = self.b_bone.get()
			new = self.n_bone.get()
			parent = self.p_bone.get()
			# Checking if specified location is a folder or file, batch dupe is performed if a folder, otherwise a single dupe is performed
			if loc.endswith('.smd'):
				inst.single_dupe(loc, base, new, parent)
			else:
				inst.batch_dupe(loc, base, new, parent)"""
	def dupe_scr(self, base, new, parent, qc):
		# Alternate bone duping function for scripts
		qc.startScript(batch=qc.batch, values=[base, new, parent])

	""" Switches menu to the Game Setup Menu """
	def bd_menu(self):
		if self.setupMenu.hidden:
			self.dumbFixMenu.grid_remove()
			self.decMenu.hide()
			self.cmpMenu.hide()
			self.setupMenu.show()
		
	
	""" Switches menu to Decompile Menu """
	def mnc_menu(self):
		if self.decMenu.hidden:
			self.dumbFixMenu.grid_remove()
			self.setupMenu.hide()
			self.cmpMenu.hide()
			self.decMenu.show()
	
	""" Switches menu to Compile Menu """
	def cmp_menu(self):
		if self.cmpMenu.hidden:
			self.setupMenu.hide()
			self.dumbFixMenu.grid(column=0, row=2, sticky="nsew", columnspan=10)
			self.cmpMenu.show()
			self.decMenu.hide()
			print(f"width: {self.winfo_width()} height: {self.winfo_height()}")
	
	def bmp(self):
		# Initialising Pointer fix function
		# We're using it for the .bmp extension function
		inst = PointerFix()
		qcSelect = QCWin(self.qcDATA, inst, 'b', [self.ref.get()])
		"""loc = self.path.get()
		ref = self.ref.get()
		inst.add_bmp(loc, ref)"""
	
	def bmp_scr(self, ref, qc):
		# Alternate function for scripts
		qc.startScript(values=[ref])

	def matrename(self):
		# Material Pointer Fixing function
		inst = PointerFix()
		qcSelect = QCWin(self.qcDATA, inst, 'm', [self.ref.get(),self.rename.get(),self.replace.get()])
		"""loc = self.path.get()
		ref = self.ref.get()
		torename = self.rename.get()
		replace = self.replace.get()
		inst.rename_part(loc, ref, torename, replace)"""
	
	def matrename_scr(self, ref, torename, replace, qc):
		# Alternate function for scripts
		qc.startScript(values=[ref, torename, replace])
	
	def scripts(self):
		# Opens Script selection window
		inst = ScriptWin()

	def optionsMenu(self):
		# Opens options window
		inst = OptWin()
	
	def exec_script(self, script):
		# Script parsing and execution function
		print('Executing script')
		values = []
		mode = script[0]
		inst = None
		if mode == 'm' or mode == 'b':
			inst = PointerFix()
		else:
			inst = Dupe()
		qcSelect = QCWin(self.qcDATA, inst, mode, [], True, script[1])
		"""# If in duping mode
		if mode == 'd':
			for d in script[1]:
				if d == '-':
					self.dupe_scr(values[0], values[1], values[2], qcSelect)
					values = []
					continue
				else:
					values.append(d)
		# If in pointer fix mode
		elif mode == 'm':
			for d in script[1]:
				if d == '-':
					self.matrename_scr(values[0], values[1], values[2], qcSelect)
					values = []
					continue
				else:
					values.append(d)
		# If in bitmap ext mode
		elif mode == 'b':
			for d in script[1]:
				if d == '-':
					self.bmp_scr(values[0], qcSelect)
					values = []
					continue
				else:
					values.append(d)
		# If in plugin initialising mode
		elif mode == 'p':
			print(script)
			filename = script[1][0]
			w = PluginWarning(filename)"""



guii = GUI()
guii.mainloop()