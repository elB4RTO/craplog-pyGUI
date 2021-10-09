#!/usr/bin/python3

import os
import subprocess
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as st

# GETTING CRAPLOG'S PATH
crappath = os.path.abspath(__file__)
crappath = crappath[:crappath.rfind('/craplog.py')]

window = tk.Tk()

# GETTING SCREEN PARAMETERS
screen_width	= window.winfo_screenwidth()
screen_height	= window.winfo_screenheight()
# SETTING WINDOW TO FULL SCREEN
window.geometry( "%dx%d" %(screen_width, screen_height) )
window.title("CRAPLOG")

# DEFINING VARIABLES
input_files			= [ "access.log.1" , "error.log.1" ]
search_file			= tk.StringVar(value=input_files[0])

str_grep			= tk.StringVar(value="")
file_content			= tk.StringVar(value="")
file_view			= tk.StringVar(value="")

CleanAccessLogs		= tk.IntVar(value=0)
AccessLogs			= tk.IntVar(value=1)
ErrorLogs			= tk.IntVar(value=0)
ErrorsOnly			= tk.IntVar(value=0)
GlobalsOnly			= tk.IntVar(value=0)
GlobalsAvoid		= tk.IntVar(value=0)
Backup				= tk.IntVar(value=0)
Trash				= tk.IntVar(value=0)
Shred				= tk.IntVar(value=0)

Remember			= tk.IntVar(value=0)

FallbackClean		= CleanAccessLogs.get()
FallbackAccess		= AccessLogs.get()
FallbackErrors		= ErrorLogs.get()
FallbackErrOnly		= ErrorsOnly.get()
FallbackGlobOnly	= GlobalsOnly.get()
FallbackGlobAvoid	= GlobalsAvoid.get()
FallbackBackup		= Backup.get()
FallbackTrash		= Trash.get()
FallbackShred		= Shred.get()


########################
# MANAGEMENT FUNCTIONS #
########################

# FALLBACK VALUES
def get_Fallback():
	global FallbackClean, FallbackAccess, FallbackErrors, FallbackErrOnly, FallbackGlobOnly, FallbackGlobAvoid, FallbackBackup, FallbackTrash, FallbackShred
	
	FallbackClean			= CleanAccessLogs.get()
	FallbackAccess			= AccessLogs.get()
	FallbackErrors			= ErrorLogs.get()
	FallbackErrOnly			= ErrorsOnly.get()
	FallbackGlobOnly		= GlobalsOnly.get()
	FallbackGlobAvoid		= GlobalsAvoid.get()
	FallbackBackup			= Backup.get()
	FallbackTrash			= Trash.get()
	FallbackShred			= Shred.get()

def set_Fallback():
	global FallbackClean, FallbackAccess, FallbackErrors, FallbackErrOnly, FallbackGlobOnly, FallbackGlobAvoid, FallbackBackup, FallbackTrash, FallbackShred

	CleanAccessLogs.set(	FallbackClean)
	AccessLogs.set(			FallbackAccess)
	ErrorLogs.set(			FallbackErrors)
	ErrorsOnly.set(			FallbackErrOnly)
	GlobalsOnly.set(		FallbackGlobOnly)
	GlobalsAvoid.set(		FallbackGlobAvoid)
	Backup.set(				FallbackBackup)
	Trash.set(				FallbackTrash)
	Shred.set(				FallbackShred)


# CONFIGURATION READ/WRITE
def error_NoConfig():
	subwin = tk.Tk()
	subwin.resizable(0,0)
	subwin.title("Error")
	tk.Label(
		master			= subwin,
		text			= "CONFIGURATIONS FILE NOT FOUND OR INVALID",
		foreground		= "black",
		background		= "red",
		width			= 50,
		height			= 3
	).pack()

def error_Writing():
	subwin = tk.Tk()
	subwin.resizable(0,0)
	subwin.title("Error")
	tk.Label(
		master			= subwin,
		text			= "UNABLE TO WRITE CONFIGURATIONS FILE",
		foreground		= "black",
		background		= "red",
		width			= 50,
		height			= 3
	).pack()

def done_Writing():
	subwin = tk.Tk()
	subwin.resizable(0,0)
	subwin.title("Done")
	tk.Label(
		master			= subwin,
		text			= "CONFIGURATIONS FILE HAS BEEN WRITTEN SUCCESFULLY",
		foreground		= "white",
		background		= "green",
		width			= 50,
		height			= 3
	).pack()

def ReadConfigs():
	global FallbackClean, FallbackAccess, FallbackErrors, FallbackErrOnly, FallbackGlobOnly, FallbackGlobAvoid, FallbackBackup, FallbackTrash, FallbackShred
	try:
		with open("./config/CONFIG", "r") as file:
			configs = file.read()

		configs = configs.split('\n')

		CleanAccessLogs.set(	int(configs[0]))
		AccessLogs.set(			int(configs[1]))
		ErrorLogs.set(			int(configs[2]))
		ErrorsOnly.set(			int(configs[3]))
		GlobalsOnly.set(		int(configs[4]))
		GlobalsAvoid.set(		int(configs[5]))
		Backup.set(				int(configs[6]))
		Trash.set(				int(configs[7]))
		Shred.set(				int(configs[8]))

		get_Fallback()

	except:
		window.after(1000, error_NoConfig)

def WriteConfigs():
	try:
		configs = str("%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s" %(
			CleanAccessLogs.get(),
			AccessLogs.get(),
			ErrorLogs.get(),
			ErrorsOnly.get(),
			GlobalsOnly.get(),
			GlobalsAvoid.get(),
			Backup.get(),
			Trash.get(),
			Shred.get()
		))
		with open("./config/CONFIG", "w") as file:
			file.write(configs)

		window.after(100, done_Writing)
	except:
		window.after(100, error_Writing)

# MANAGING CHECK-BOXES
def ManageALL():
	manage_ErrOnly()
	manage_GlobOnly()
	manage_GlobAvoid()
	manage_Trash()
	manage_Shred()

def manage_Terminal():
	menu_TERM.config(text=terminal.get())

def manage_ErrOnly():
	global FallbackClean, FallbackErrors
	value = ErrorsOnly.get()
	if value == 1:
		FallbackClean = CleanAccessLogs.get()
		CleanAccessLogs.set(0)
		check_CLEAN["state"] = "disabled"
		AccessLogs.set(0)
		FallbackErrors = ErrorLogs.get()
		ErrorLogs.set(1)
		check_ERRORS["state"] = "disabled"
	else:
		CleanAccessLogs.set(FallbackClean)
		check_CLEAN["state"] = "normal"
		AccessLogs.set(1)
		ErrorLogs.set(FallbackErrors)
		check_ERRORS["state"] = "normal"

def manage_GlobOnly():
	value = GlobalsOnly.get()
	if value == 1:
		GlobalsAvoid.set(0)
		check_GLOBAVOID["state"] = "disabled"
	else:
		check_GLOBAVOID["state"] = "normal"

def manage_GlobAvoid():
	value = GlobalsAvoid.get()
	if value == 1:
		GlobalsOnly.set(0)
		check_GLOBONLY["state"] = "disabled"
	else:
		check_GLOBONLY["state"] = "normal"

def manage_Trash():
	value = Trash.get()
	if value == 1:
		Shred.set(0)

def manage_Shred():
	value = Shred.get()
	if value == 1:
		Trash.set(0)


# LOCK/UNLOCK ITEMS
def LockAll():
	global FallbackClean, FallbackAccess, FallbackErrors, FallbackErrOnly, FallbackGlobOnly, FallbackGlobAvoid, FallbackBackup, FallbackTrash, FallbackShred
	get_Fallback()

	files_L.config(				state="disabled")
	files_B.config(				state="disabled")
	search_L.config(			state="disabled")
	search_E.config(			state="disabled")
	search_B.config(			state="disabled")

	button_START.config(		state="disabled")
	check_ERRORS.config(		state="disabled")
	check_ERRORSONLY.config(	state="disabled")
	check_CLEAN.config(			state="disabled")
	check_GLOBONLY.config(		state="disabled")
	check_GLOBAVOID.config(		state="disabled")
	check_BACKUP.config(		state="disabled")
	check_TRASH.config(			state="disabled")
	check_SHRED.config(			state="disabled")
	button_HELP.config(			state="disabled")
	button_REMEMBER.config(		state="disabled")
	window.after(100,StartCRAPLOG)

def UnlockAll():
	global FallbackClean, FallbackAccess, FallbackErrors, FallbackErrOnly, FallbackGlobOnly, FallbackGlobAvoid, FallbackBackup, FallbackTrash, FallbackShred

	files_L.config(				state="normal")
	files_B.config(				state="normal")
	search_L.config(			state="normal")
	search_E.config(			state="normal")
	search_B.config(			state="normal")

	button_START.config(		state="normal")
	check_ERRORS.config(		state="normal")
	check_ERRORSONLY.config(	state="normal")
	check_CLEAN.config(			state="normal")
	check_GLOBONLY.config(		state="normal")
	check_GLOBAVOID.config(		state="normal")
	check_BACKUP.config(		state="normal")
	check_TRASH.config(			state="normal")
	check_SHRED.config(			state="normal")
	button_HELP.config(			state="normal")
	button_REMEMBER.config(		state="normal")

	set_Fallback()
	ManageALL()


# RETURN PROCESS OUTPUT
def printCRAP(text):
	text_process.config(state="normal")
	text_process.update()
	text_process.delete('1.0',tk.END)
	text_process.insert(tk.INSERT, text)
	text_process.config(state="disabled")


#################
# START CRAPLOG #
#################
def StartCRAPLOG():
	crap = "%s/crappy/Main.py" %( crappath )

	if AccessLogs.get():		crap += " 1"
	else:						crap += " 0"

	if CleanAccessLogs.get():	crap += " 1"
	else:						crap += " 0"

	if ErrorLogs.get():			crap += " 1"
	else:						crap += " 0"

	if ErrorsOnly.get():		crap += " 1"
	else:						crap += " 0"

	if GlobalsOnly.get():		crap += " 1"
	else:						crap += " 0"

	if GlobalsAvoid.get():		crap += " 1"
	else:						crap += " 0"

	if Backup.get():			crap += " 1"
	else:						crap += " 0"

	if Trash.get():				crap += " 1"
	else:						crap += " 0"

	if Shred.get():				crap += " 1"
	else:						crap += " 0"

	crapOUT		= ""
	crapERR		= ""
	crapSTART	= subprocess.Popen(crap, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	crapOUT		= crapSTART.stdout.read()
	crapERR		= crapSTART.stderr.read()
	if len(crapERR) <3:	printCRAP(crapOUT)
	else:				printCRAP(crapERR)
	crapSTART.wait()
	
	window.after(500,UnlockAll)


######################
# SPECIFIC FUNCTIONS #
######################
def getHelp():
	helpText = ""
	with open("./aux/elbarto", "r") as file:
		helpText += file.read()
	with open("./aux/craplogo", "r") as file:
		helpText += file.read()
	with open("./aux/help", "r") as file:
		helpText += file.read()

	subwin = tk.Tk()
	subwin.resizable(0,0)
	subwin.title("Help")
	subwin.columnconfigure(0)
	subwin.rowconfigure(0)

	helpWin = st.ScrolledText(
		master			= subwin,
		foreground		= "white",
		background		= "black",
		width			= 63
	)
	helpWin.insert(tk.INSERT, helpText)
	helpWin.insert(tk.END,"\n")
	helpWin.pack()


def set_SearchFile():
	search_Files.config(text=search_file.get())


def search_String():
	tmp_content		= file_content.get().split("\n")
	tmp_view		= ""
	str_grep.set(	value=search_E.get())
	for log in tmp_content:
		if log.find( str_grep.get() ) != -1:
			tmp_view += "%s\n\n" %( log )
	
	search_view.config(state="normal")
	search_view.update()
	search_view.delete('1.0',tk.END)
	search_view.insert(tk.INSERT, tmp_view)
	search_view.config(state="disabled")


########################
# WINDOW CONFIGURATION #
########################
window.config( background="white" )
window.columnconfigure(		0,		weight=1,	minsize=300)
window.columnconfigure(		1,		weight=1,	minsize=300)
window.grid_rowconfigure(	0,		weight=1)


###################
# SEARCH/VIEW BOX #
###################
box_search = tk.Frame(
	master			= window,
	background		= "#FFFFFF"
)
box_search.columnconfigure(		[0],				weight=1,	minsize=100)	# MAIN WIDTH
box_search.rowconfigure(		[0],				weight=0,	minsize=10)		# HEAD'S ROW
box_search.rowconfigure(		[1,2,3,4,5,6,7,8],	weight=1,	minsize=20)		# BODY'S ROW

search_Head = tk.Frame(
	master			= box_search,
	height			= 1,
	background		= "#FFFFFF"
)
search_Head.columnconfigure(	[0],		weight=1,	minsize=100)	# INPUTS' COLUMN
search_Head.columnconfigure(	[1],		weight=1,	minsize=50)		# BUTTONS' COLUMN
search_Head.rowconfigure(		[0],		weight=1,	minsize=10)		# TITLE'S ROW
search_Head.rowconfigure(		[1,4],		weight=1,	minsize=10)		# LABELS' ROW
search_Head.rowconfigure(		[3],		weight=1,	minsize=20)		# EMPTY SPACE
search_Head.rowconfigure(		[2,5],		weight=1,	minsize=20)		# INPUTS' ROW

# TITLE
search_Head_L = tk.Label(
	master			= search_Head,
	text			= "LOGS FILE VIEWER",
	state			= "normal",
	foreground		= "#000000",
	background		= "#FFFFFF"
)


# INPUT FILE
search_Files = ttk.Menubutton(
	master		= search_Head,
	state		= "normal",
	text		= search_file.get(),
	width		= 12
)

files_radio = tk.Menu(
	master		= search_Files,
	tearoff		= 0
)

for file in input_files:
	files_radio.add_radiobutton(
		command		= set_SearchFile,
		label		= file,
		value		= file,
		variable	= search_file
	)

search_Files["menu"] = files_radio

files_L = tk.Label(
	master			= search_Head,
	text			= "select a file to view",
	state			= "normal",
	foreground		= "#000000",
	background		= "#FFFFFF"
)

files_B = tk.Button(
	master			= search_Head,
	command			= None,
	text			= "Load",
	state			= "normal",
	foreground		= "white",
	background		= "black"
)


# INPUT STRING
search_L = tk.Label(
	master			= search_Head,
	text			= "search for a string",
	state			= "normal",
	foreground		= "#000000",
	background		= "#FFFFFF"
)

search_E = tk.Entry(
	master			= search_Head,
	text			= str_grep,
	state			= "normal",
	foreground		= "#000000",
	background		= "#FFFFFF",
	width			= 50
)

search_B = tk.Button(
	master			= search_Head,
	command			= search_String,
	text			= "Search",
	state			= "normal",
	foreground		= "white",
	background		= "black"
)


search_view = st.ScrolledText(
	master			= box_search,
	state			= "disabled",
	foreground		= "black",
	background		= "white",
	wrap			= "word"
)
def load_SearchFile():
	with open("/var/log/apache2/%s" %( search_file.get() )) as file:
		file_content.set( value=str(file.read()).replace("\n","\n\n") )
	search_view.config(state="normal")
	search_view.update()
	search_view.delete('1.0',tk.END)
	search_view.insert(tk.INSERT, file_content.get())
	search_view.config(state="disabled")

files_B.config(command=load_SearchFile)


############
# MAIN BOX #
############
box_main = tk.Frame(
	master			= window,
	background		= "#1e1e1e"
)
box_main.columnconfigure(		[0],		weight=1,	minsize=100)	# MAIN WIDTH
box_main.rowconfigure(			[0],		weight=1,	minsize=100)	# STARTER'S ROW
box_main.rowconfigure(			[1],		weight=0,	minsize=10)		# ARGUMENTS' ROW
box_main.rowconfigure(			[2],		weight=1,	minsize=500)	# TERMINAL'S ROW

button_START = tk.Button(
	master					= box_main,
	text					= "Start CRAPLOG",
	command					= LockAll,
	state					= "normal",
	height					= 2,
	foreground				= "white",
	background				= "black",
	activebackground		= "green",
	highlightbackground		= "#1e1e1e",
	borderwidth				= 1,
	relief					= tk.GROOVE
)

box_arguments = tk.Frame(
	master			= box_main,
	height			= 2,
	background		= "#1e1e1e"
)
box_arguments.columnconfigure(	[0,1,2,3,4],		weight=1,	minsize=150)
box_arguments.rowconfigure(		[0,3],				weight=0,	minsize=10)		# TITLE & FOOTER
box_arguments.rowconfigure(		[1,2],				weight=0,	minsize=10)		# BODY

label_TITLE = tk.Label(
	master			= box_arguments,
	text			= "ARGUMENTS",
	justify			= "center",
	foreground		= "#afafaf",
	background		= "#1e1e1e"
)

check_ACCESS = tk.Checkbutton(
	master					= box_arguments,
	variable				= AccessLogs,
	state					= "disabled",
	offvalue				= 0,
	onvalue					= 1,
	selectcolor				= "black",
	text					= "access logs",
	justify					= "center",
	foreground				= "#FFFFFF",
	activeforeground		= "#FFFFFF",
	disabledforeground		= "#5e5e5e",
	background				= "#1e1e1e",
	activebackground		= "#2e2e2e",
	border					= 3,
	highlightthickness		= 0
)

check_CLEAN = tk.Checkbutton(
	master					= box_arguments,
	variable				= CleanAccessLogs,
	state					= "normal",
	offvalue				= 0,
	onvalue					= 1,
	selectcolor				= "black",
	text					= "clean access logs",
	justify					= "center",
	foreground				= "#FFFFFF",
	activeforeground		= "#FFFFFF",
	disabledforeground		= "#5e5e5e",
	background				= "#1e1e1e",
	activebackground		= "#2e2e2e",
	border					= 3,
	highlightthickness		= 0
)

check_ERRORS = tk.Checkbutton(
	master					= box_arguments,
	variable				= ErrorLogs,
	state					= "normal",
	offvalue				= 0,
	onvalue					= 1,
	selectcolor				= "black",
	text					= "error logs",
	justify					= "center",
	foreground				= "#FFFFFF",
	activeforeground		= "#FFFFFF",
	disabledforeground		= "#5e5e5e",
	background				= "#1e1e1e",
	activebackground		= "#2e2e2e",
	border					= 3,
	highlightthickness		= 0
)

check_ERRORSONLY = tk.Checkbutton(
	master					= box_arguments,
	variable				= ErrorsOnly,
	command					= manage_ErrOnly,
	state					= "normal",
	offvalue				= 0,
	onvalue					= 1,
	selectcolor				= "black",
	text					= "only error logs",
	justify					= "center",
	foreground				= "#FFFFFF",
	activeforeground		= "#FFFFFF",
	disabledforeground		= "#5e5e5e",
	background				= "#1e1e1e",
	activebackground		= "#2e2e2e",
	border					= 3,
	highlightthickness		= 0
)

check_GLOBONLY = tk.Checkbutton(
	master					= box_arguments,
	variable				= GlobalsOnly,
	command					= manage_GlobOnly,
	state					= "normal",
	offvalue				= 0,
	onvalue					= 1,
	selectcolor				= "black",
	text					= "only globals",
	justify					= "center",
	foreground				= "#FFFFFF",
	activeforeground		= "#FFFFFF",
	disabledforeground		= "#5e5e5e",
	background				= "#1e1e1e",
	activebackground		= "#2e2e2e",
	border					= 3,
	highlightthickness		= 0
)

check_GLOBAVOID = tk.Checkbutton(
	master					= box_arguments,
	variable				= GlobalsAvoid,
	command					= manage_GlobAvoid,
	state					= "normal",
	offvalue				= 0,
	onvalue					= 1,
	selectcolor				= "black",
	text					= "avoid globals",
	justify					= "center",
	foreground				= "#FFFFFF",
	activeforeground		= "#FFFFFF",
	disabledforeground		= "#5e5e5e",
	background				= "#1e1e1e",
	activebackground		= "#2e2e2e",
	border					= 3,
	highlightthickness		= 0
)

check_BACKUP = tk.Checkbutton(
	master					= box_arguments,
	variable				= Backup,
	state					= "normal",
	offvalue				= 0,
	onvalue					= 1,
	selectcolor				= "black",
	text					= "backup",
	justify					= "center",
	foreground				= "#FFFFFF",
	activeforeground		= "#FFFFFF",
	disabledforeground		= "#5e5e5e",
	background				= "#1e1e1e",
	activebackground		= "#2e2e2e",
	border					= 3,
	highlightthickness		= 0
)

check_TRASH = tk.Checkbutton(
	master					= box_arguments,
	variable				= Trash,
	command					= manage_Trash,
	state					= "normal",
	offvalue				= 0,
	onvalue					= 1,
	selectcolor				= "black",
	text					= "trash",
	justify					= "center",
	foreground				= "#FFFFFF",
	activeforeground		= "#FFFFFF",
	disabledforeground		= "#5e5e5e",
	background				= "#1e1e1e",
	activebackground		= "#2e2e2e",
	border					= 3,
	highlightthickness		= 0
)

check_SHRED = tk.Checkbutton(
	master					= box_arguments,
	variable				= Shred,
	command					= manage_Shred,
	state					= "normal",
	offvalue				= 0,
	onvalue					= 1,
	selectcolor				= "black",
	text					= "shred",
	justify					= "center",
	foreground				= "#FFFFFF",
	activeforeground		= "#FFFFFF",
	disabledforeground		= "#5e5e5e",
	background				= "#1e1e1e",
	activebackground		= "#2e2e2e",
	border					= 3,
	highlightthickness		= 0
)

button_REMEMBER	= tk.Button(
	master					= box_arguments,
	command					= WriteConfigs,
	text					= "Save these settings",
	relief					= "flat",
	justify					= "center",
	foreground				= "#FFFFFF",
	activeforeground		= "#FFFFFF",
	disabledforeground		= "#5e5e5e",
	background				= "#1e1e1e",
	activebackground		= "#2e2eee"
)

button_HELP = tk.Button(
	master					= box_arguments,
	command					= getHelp,
	text					= "Help",
	justify					= "center",
	relief					= "flat",
	foreground				= "#FFFFFF",
	activeforeground		= "#FFFFFF",
	disabledforeground		= "#5e5e5e",
	background				= "#1e1e1e",
	activebackground		= "#2e2e2e"
)


text_process = tk.Text(
	master			= box_main,
	state			= "disabled",
	foreground		= "white",
	background		= "black"
)



################
# FINAL SET UP #
################
ReadConfigs()
ManageALL()


#################
# WINDOW SET UP #
#################

# SEARCH
box_search.grid(			row=0,	column=0,	sticky="nswe")
## HEAD
search_Head.grid(			row=0,	column=0,	sticky="nswe",				padx=10)
### TITLE
search_Head_L.grid(			row=0,	column=0,	sticky="we",	pady=10,				columnspan=2)
### INPUT FILE
files_L.grid(				row=1,	column=0,	sticky="w",		pady=5)
search_Files.grid(			row=2,	column=0,	sticky="we",				padx=3)
files_B.grid(				row=2,	column=1,	sticky="we",				padx=3)
### INPUT STRING
search_L.grid(				row=4,	column=0,	sticky="w",		pady=5)
search_E.grid(				row=5,	column=0,	sticky="we")
search_B.grid(				row=5,	column=1,	sticky="we",				padx=3)
## BODY
search_view.grid(			row=2,	column=0,	sticky="nswe",							rowspan=8)

# MAIN
box_main.grid(				row=0,	column=1,	sticky="nswe")
## STARTER
button_START.grid(			row=0,	column=0,	sticky="nswe")
## ARGUMENTS
box_arguments.grid(			row=1,	column=0,	sticky="we",	pady=10)
### ARGS CHECK-BOXES
label_TITLE.grid(			row=0,	column=0,	sticky="we",	pady=5,					columnspan=5)
check_ACCESS.grid(			row=1,	column=0,	sticky="w",		pady=10,	padx=5)
check_CLEAN.grid(			row=2,	column=0,	sticky="w",		pady=10,	padx=5)
check_ERRORS.grid(			row=1,	column=1,	sticky="w",		pady=10,	padx=5)
check_ERRORSONLY.grid(		row=2,	column=1,	sticky="w",		pady=10,	padx=5)
check_GLOBONLY.grid(		row=1,	column=2,	sticky="w",		pady=10,	padx=5)
check_GLOBAVOID.grid(		row=2,	column=2,	sticky="w",		pady=10,	padx=5)
check_BACKUP.grid(			row=1,	column=3,	sticky="w",		pady=10,	padx=5)
check_TRASH.grid(			row=1,	column=4,	sticky="w",		pady=10,	padx=5)
check_SHRED.grid(			row=2,	column=4,	sticky="w",		pady=10,	padx=5)
### ARGUMENTS FOOTER
button_REMEMBER.grid(		row=3,	column=0,	sticky="we",	pady=10,	padx=20)
button_HELP.grid(			row=3,	column=4,	sticky="we",	pady=10,	padx=20)
## PROCESS
text_process.grid(			row=2,	column=0,	sticky="nswe")


search = search_E.get()


####################
# FINALLY STARTING #
####################
window.mainloop()
