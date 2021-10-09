#!/usr/bin/python3

import os
import time
import subprocess
from sys import argv
from pathlib import Path
from datetime import datetime

# GETTING ARGUMENTS
AccessLogs			= int( argv[1]  )
CleanAccessLogs		= int( argv[2]  )
ErrorLogs			= int( argv[3]  )
ErrorsOnly			= int( argv[4]  )
GlobalsOnly			= int( argv[5]  )
GlobalsAvoid		= int( argv[6]  )
Backup				= int( argv[7]  )
Trash				= int( argv[8] )
Shred				= int( argv[9] )

# GETTING OWN MODULES
import Clean, Stat
if not GlobalsAvoid:
	import Glob

# GETTING CRAPLOG'S PATH
crappath = os.path.abspath(__file__)
crappath = crappath[:crappath.rfind('/crappy/Main.py')]

# CRAPLOGO
print("\n\
    CCCC  RRRR   AAAAA  PPPP   L      OOOOO  GGGGG   \n\
   C      R   R  A   A  P   P  L      O   O  G       \n\
   C      RRRR   AAAAA  PPPP   L      O   O  G  GG   \n\
   C      R  R   A   A  P      L      O   O  G   G   \n\
    CCCC  R   R  A   A  P      LLLLL  OOOOO  GGGGG   \n\
\n")

# VARIABLES INTEGRITY CHECKS
errMSG = " [+]: this should be only a security check\n [+]: if you manually edited any file, undo the changes or copy paste the original from https://github.com/elB4RTO/craplog-fullGUI\n [+]: if you haven't edited any file, please report this error"

if not AccessLogs and not ErrorLogs:
	print(" Error: you can't avoid using both access and error log files, nothing will be done\n")
	print(errMSG)
	exit()

if not AccessLogs and CleanAccessLogs:
	print(" Error: not possible to make a clean access log file [clean] without working on a access.log file [only error logs]")
	print(errMSG)
	exit()

if not ErrorLogs and ErrorsOnly:
	print(" Error: not possible to only use error logs file [only error logs] without working on a error.log file [error logs]\n")
	print(errMSG)
	exit()

if GlobalsOnly and GlobalsAvoid:
	print(" Error: you can't use [only globals] toghether with [avoid globals]")
	print(errMSG)
	exit()

if Trash and Shred:
	print(" Error: you can't use [trash] toghether with [shred]")
	print(errMSG)
	exit()

# INPUT FILES EXISTENCE CHECKS
if not os.path.exists("/var/log/apache2"):
	print(" Error: directory /var/log/apache2/ does not exist")
	exit()

if AccessLogs:
	if not os.path.exists("/var/log/apache2/access.log.1"):
		print("Error: there is no access.log.1 file inside /var/log/apache2/")
		exit()
	else:
		try:
			file = open("/var/log/apache2/access.log.1", "r")
			file.close()
		except IOError:
			print("Error: can't read /var/log/apache2/access.log.1")
			exit()

if ErrorLogs:
	if not os.path.exists("/var/log/apache2/error.log.1"):
		print("Error: there is no error.log.1 file inside /var/log/apache2/")
		exit()
	else:
		try:
			file = open("/var/log/apache2/error.log.1", "r")
			file.close()
		except IOError:
			print("Error: can't read /var/log/apache2/error.log.1")
			exit()

# TRASH EXISTENCE CHECK
if Trash:
	TrashPath = "%s/.local/share/Trash/files/" %( os.environ['HOME'] )
	if not os.path.exists(TrashPath):
		print("Error: directory %s does not exist" %( TrashPath ))
		exit()

# ALL CHECKS PASSED

# CHECKING AND REMOVING CONFLICT FILES
FilesList		= []
ConflictFiles	= []
if os.path.exists("%s/STATS/" %( crappath )):
	for (path, dirs, files) in os.walk("%s/STATS/" %( crappath )):
		FilesList.extend(files)
		break
	if len(FilesList) > 0:
		for File in FilesList:
			if File.endswith(".crap") or File.endswith(".crapstats") or File == "CLEAN.access.log":			
				ConflictFiles.append(File)

	FilesList		= []
	for (path, dirs, files) in os.walk("%s/STATS/GLOBALS/" %( crappath )):
		FilesList.extend(files)
		break
	if len(FilesList) > 0:
		for File in FilesList:
			if File.startswith(".GLOBAL.") and File.endswith(".crap"):
				ConflictFiles.append("GLOBALS/%s" %( File ))
else:
	Path("%s/STATS/GLOBALS" %( crappath )).mkdir(parents=True, exist_ok=True)

if len(ConflictFiles) > 0:
	for File in ConflictFiles:
		if Trash:
			subprocess.run([ "mv", "%s/STATS/%s" %( crappath, File ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

		elif Shred:
			subprocess.run(["shred", "-uvz", "%s/STATS/%s" %( crappath, File )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		else:
			subprocess.run(["rm", "%s/STATS/%s" %( crappath, File )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


# STARTING CRAPLOG
# CLEANING AND SCRAPING SESSION LOGS
if AccessLogs:	Clean.Access( CleanAccessLogs )
if ErrorLogs:	Clean.Error()
print()


# CREATING STATISTICS FROM SESSION LOGS
if AccessLogs:	Stat.Access()
if ErrorLogs:	Stat.Error()
print()


# UPDATING GLOBAL STATISTICS
if not GlobalsAvoid:
	if AccessLogs:
		try:
			os.rename("%s/STATS/GLOBALS/GLOBAL.IP.crapstats" %( crappath ), "%s/STATS/GLOBALS/.GLOBAL.IP.crap" %( crappath ))
		except:
			Path("%s/STATS/GLOBALS/.GLOBAL.IP.crap" %( crappath )).touch()

		try:
			os.rename("%s/STATS/GLOBALS/GLOBAL.REQ.crapstats" %( crappath ), "%s/STATS/GLOBALS/.GLOBAL.REQ.crap" %( crappath ))
		except:
			Path("%s/STATS/GLOBALS/.GLOBAL.REQ.crap" %( crappath )).touch()
		
		try:
			os.rename("%s/STATS/GLOBALS/GLOBAL.RES.crapstats" %( crappath ), "%s/STATS/GLOBALS/.GLOBAL.RES.crap" %( crappath ))
		except:
			Path("%s/STATS/GLOBALS/.GLOBAL.RES.crap" %( crappath )).touch()
		
		try:
			os.rename("%s/STATS/GLOBALS/GLOBAL.UA.crapstats" %( crappath ), "%s/STATS/GLOBALS/.GLOBAL.UA.crap" %( crappath ))
		except:
			Path("%s/STATS/GLOBALS/.GLOBAL.UA.crap" %( crappath )).touch()

	if ErrorLogs:
		try:
			os.rename("%s/STATS/GLOBALS/GLOBAL.LEV.crapstats" %( crappath ), "%s/STATS/GLOBALS/.GLOBAL.LEV.crap" %( crappath ))
		except:
			Path("%s/STATS/GLOBALS/.GLOBAL.LEV.crap" %( crappath )).touch()
		
		try:
			os.rename("%s/STATS/GLOBALS/GLOBAL.ERR.crapstats" %( crappath ), "%s/STATS/GLOBALS/.GLOBAL.ERR.crap" %( crappath ))
		except:
			Path("%s/STATS/GLOBALS/.GLOBAL.ERR.crap" %( crappath )).touch()

	if AccessLogs:	Glob.Access()
	if ErrorLogs:	Glob.Error()
	print()



# MOVING NEWLY CREATED FILES
if not GlobalsOnly:

	# SETTING YESTERDAY'S DATE
	day = datetime.now().day - 1
	if day < 1:
		# YESTERDAY WAS THE LAST DAY OF THE PREVIOUS MONTH
		month = datetime.now().month - 1
		if month < 1:
			# YESTERDAY WAS THE LAST DAY OF THE LAST MONTH OF THE PREVIOUS YEAR
			day		= 31
			month	= 12
			year	= datetime.now().year - 1
		else:
			year	= datetime.now().year
			if month in [1,3,5,7,8,10]:
				day	= 31
			elif month in [4,6,9,11]:
				day = 30
			else:
				if (year % 4) == 0:
					day = 29
				else:
					day = 28
	else:
		month	= datetime.now().month
		year	= datetime.now().year

	if day < 10:
		day = "0%s" %( day )
	if month < 10:
		month = "0%s" %( month )
	DateDir = "%s/STATS/%s/%s/%s" %( crappath, year, month, day )
	print(" SESSION DIRECTORY: %s/" %( DateDir ))

	if os.path.exists(DateDir):
		if CleanAccessLogs:
			if os.path.exists("%s/CLEAN.access.log" %( DateDir )):
				if Trash:
					subprocess.run(["mv", "%s/CLEAN.access.log" %( DateDir ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
				elif Shred:
					subprocess.run(["shred", "-uvz", "%s/CLEAN.access.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
				else:
					subprocess.run(["rm", "%s/CLEAN.access.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			
			subprocess.run(["mv", "%s/STATS/CLEAN.access.log" %( crappath ), "%s/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		
		if AccessLogs:
			if os.path.exists("%s/ACCESS/" %( DateDir )):
				FilesList		= []
				ConflictFiles	= []
				for (path, dirs, files) in os.walk("%s/ACCESS/" %( DateDir )):
					FilesList.extend(files)
					break
				if len(FilesList) > 0:
					for File in FilesList:
						if File.endswith(".crapstats"):
							ConflictFiles.append(File)
			
				if len(ConflictFiles) > 0:
					for File in ConflictFiles:
						if Trash:
							subprocess.run(["mv", "%s/ACCESS/%s" %( DateDir, File ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
						elif Shred:
							subprocess.run(["shred", "-uvz", "%s/ACCESS/%s" %( DateDir, File )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
						else:
							subprocess.run(["rm", "%s/ACCESS/%s" %( DateDir, File )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
					
			else:
				Path("%s/ACCESS" %( DateDir )).mkdir(parents=True, exist_ok=True)
			
			subprocess.run(["mv", "%s/STATS/IP.crapstats" %( crappath ), "%s/ACCESS/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			subprocess.run(["mv", "%s/STATS/REQ.crapstats" %( crappath ), "%s/ACCESS/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			subprocess.run(["mv", "%s/STATS/RES.crapstats" %( crappath ), "%s/ACCESS/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			subprocess.run(["mv", "%s/STATS/UA.crapstats" %( crappath ), "%s/ACCESS/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

		if ErrorLogs:
			if os.path.exists("%s/ERROR/" %( DateDir )):
				FilesList		= []
				ConflictFiles	= []
				for (path, dirs, files) in os.walk("%s/ERROR/" %( DateDir )):
					FilesList.extend(files)
					break
				if len(FilesList) > 0:
					for File in FilesList:
						if File.endswith(".crapstats"):
							ConflictFiles.append(File)
			
				if len(FilesList) > 0:
					for File in ConflictFiles:
						if Trash:
							subprocess.run(["mv", "%s/ERROR/%s" %( DateDir, File ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
						elif Shred:
							subprocess.run(["shred", "-uvz", "%s/ERROR/%s" %( DateDir, File )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
						else:
							subprocess.run(["rm", "%s/ERROR/%s" %( DateDir, File )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
					
			else:
				Path("%s/ERROR" %( DateDir )).mkdir(parents=True, exist_ok=True)

			subprocess.run(["mv", "%s/STATS/ERR.crapstats" %( crappath ), "%s/ERROR/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			subprocess.run(["mv", "%s/STATS/LEV.crapstats" %( crappath ), "%s/ERROR/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			
	else:
		Path("%s" %( DateDir )).mkdir(parents=True, exist_ok=True)
		
		if CleanAccessLogs:
			subprocess.run(["mv", "%s/STATS/CLEAN.access.log" %( crappath ), "%s/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		
		if AccessLogs:
			Path("%s/ACCESS" %( DateDir )).mkdir(parents=True, exist_ok=True)
			subprocess.run(["mv", "%s/STATS/IP.crapstats" %( crappath ), "%s/ACCESS/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			subprocess.run(["mv", "%s/STATS/REQ.crapstats" %( crappath ), "%s/ACCESS/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			subprocess.run(["mv", "%s/STATS/RES.crapstats" %( crappath ), "%s/ACCESS/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			subprocess.run(["mv", "%s/STATS/UA.crapstats" %( crappath ), "%s/ACCESS/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		
		if ErrorLogs:
			Path("%s/ERROR" %( DateDir )).mkdir(parents=True, exist_ok=True)
			subprocess.run(["mv", "%s/STATS/ERR.crapstats" %( crappath ), "%s/ERROR/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			subprocess.run(["mv", "%s/STATS/LEV.crapstats" %( crappath ), "%s/ERROR/" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		

# CREATING BACKUP OF ORIGINAL LOG FILES
if Backup:
	if os.path.exists("%s/BACKUP.tar.gz" %( DateDir )):
		if Trash:
			subprocess.run(["mv", "%s/BACKUP.tar.gz" %( DateDir ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		elif Shred:
			subprocess.run(["shred", "-uvz", "%s/BACKUP.tar.gz" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		else:
			subprocess.run(["rm", "%s/BACKUP.tar.gz" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	
	if os.path.exists("%s/access.log" %( DateDir )):
		if Trash:
			subprocess.run(["mv", "%s/access.log" %( DateDir ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		elif Shred:
			subprocess.run(["shred", "-uvz", "%s/access.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		else:
			subprocess.run(["rm", "%s/access.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

	if os.path.exists("%s/error.log" %( DateDir )):
		if Trash:
			subprocess.run(["mv", "%s/error.log" %( DateDir ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		elif Shred:
			subprocess.run(["shred", "-uvz", "%s/error.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		else:
			subprocess.run(["rm", "%s/error.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	
	subprocess.run(["cp", "/var/log/apache2/access.log.1", "%s/access.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	subprocess.run(["cp", "/var/log/apache2/error.log.1", "%s/error.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

	os.chdir("%s" %( DateDir ) )
	subprocess.run(["tar", "-czf", "BACKUP.tar.gz", "access.log", "error.log"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

	if Trash:
		subprocess.run(["mv", "%s/access.log" %( DateDir ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		subprocess.run(["mv", "%s/error.log" %( DateDir ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	elif Shred:
		subprocess.run(["shred", "-uvz", "%s/access.log" %( DateDir ), "%s/error.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	else:
		subprocess.run(["rm", "%s/access.log" %( DateDir ), "%s/error.log" %( DateDir )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
print("\n Created BACKUP of original files")


# REMOVING TEMPORARY FILES
TempFiles	= []
FilesList	= []
for (path, dirs, files) in os.walk("%s/STATS/" %( crappath )):
	FilesList.extend(files)
	break
if len(FilesList) > 0:
	for File in FilesList:
		if File.endswith(".crap") or File.endswith(".crapstats"):
			TempFiles.append(File)

FilesList	= []
for (path, dirs, files) in os.walk("%s/STATS/GLOBALS/" %( crappath )):
	FilesList.extend(files)
	break
if len(FilesList) > 0:
	for File in FilesList:
		if File.startswith(".GLOBAL.") and File.endswith(".crap"):
			TempFiles.append("GLOBALS/%s" %( File ))

if len(TempFiles) > 0:
	for File in TempFiles:
		if Trash:
			subprocess.run(["mv", "%s/STATS/%s" %( crappath, File ), TrashPath ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		elif Shred:
			subprocess.run(["shred", "-uvz", "%s/STATS/%s" %( crappath, File )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		else:
			subprocess.run(["rm", "%s/STATS/%s" %( crappath, File )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


# UPDATING GOLBALS' BACKUPS
if not os.path.exists("%s/STATS/GLOBALS/.BACKUPS" %( crappath )):
	Path("%s/STATS/GLOBALS/.BACKUPS" %( crappath )).mkdir(parents=True, exist_ok=True)
	with open("%s/STATS/GLOBALS/.BACKUPS/.last_time" %( crappath ), "w") as file:
		file.write(str(0))

if not os.path.exists("%s/STATS/GLOBALS/.BACKUPS/.last_time" %( crappath )):
	with open("%s/STATS/GLOBALS/.BACKUPS/.last_time" %( crappath ), "w") as file:
		file.write(str( 7 ))

if not os.path.exists("%s/STATS/GLOBALS/.BACKUPS/TMP" %( crappath )):
	Path("%s/STATS/GLOBALS/.BACKUPS/TMP" %( crappath )).mkdir(parents=True, exist_ok=True)

for dirname in [1,2,3,4,5,6,7]:
	if not os.path.exists("%s/STATS/GLOBALS/.BACKUPS/%s" %( crappath, dirname )):
		Path("%s/STATS/GLOBALS/.BACKUPS/%s" %( crappath, dirname )).mkdir(parents=True, exist_ok=True)

# GETTING BACKUP'S LAST-TIME VALUE
with open("%s/STATS/GLOBALS/.BACKUPS/.last_time" %( crappath ), "r") as file:
	LastGlobalsBackup = int(file.read().strip())

if LastGlobalsBackup < 7:
	# INCRASING BACKUP'S LAST-TIME VALUE
	with open("%s/STATS/GLOBALS/.BACKUPS/.last_time" %( crappath ), "w") as file:
		file.write(str( LastGlobalsBackup + 1 ))

else:
	# COPYING ACTUAL GLOBALS TO 'TMP' FOLDER
	FilesList = []
	for (path, dirs, files) in os.walk("%s/STATS/GLOBALS/" %( crappath )):
		FilesList.extend(files)
		break
	if len(FilesList) > 0:
		for File in FilesList:
			if File.endswith(".crapstats"):
				subprocess.run(["cp", "%s/STATS/GLOBALS/%s" %( crappath, File ), "%s/STATS/GLOBALS/.BACKUPS/TMP/" %( crappath )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	# SWITCHING BACKUPS FOLDERS' NAMES
	subprocess.run(["rm", "-r", "%s/STATS/GLOBALS/.BACKUPS/1" %( crappath )], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	os.rename("%s/STATS/GLOBALS/.BACKUPS/2" %( crappath ), "%s/STATS/GLOBALS/.BACKUPS/1" %( crappath ))
	os.rename("%s/STATS/GLOBALS/.BACKUPS/3" %( crappath ), "%s/STATS/GLOBALS/.BACKUPS/2" %( crappath ))
	os.rename("%s/STATS/GLOBALS/.BACKUPS/4" %( crappath ), "%s/STATS/GLOBALS/.BACKUPS/3" %( crappath ))
	os.rename("%s/STATS/GLOBALS/.BACKUPS/5" %( crappath ), "%s/STATS/GLOBALS/.BACKUPS/4" %( crappath ))
	os.rename("%s/STATS/GLOBALS/.BACKUPS/6" %( crappath ), "%s/STATS/GLOBALS/.BACKUPS/5" %( crappath ))
	os.rename("%s/STATS/GLOBALS/.BACKUPS/7" %( crappath ), "%s/STATS/GLOBALS/.BACKUPS/6" %( crappath ))
	os.rename("%s/STATS/GLOBALS/.BACKUPS/TMP" %( crappath ), "%s/STATS/GLOBALS/.BACKUPS/7" %( crappath ))
	# RESETTING BACKUPS' LAST-TIME
	with open("%s/STATS/GLOBALS/.BACKUPS/.last_time" %( crappath ), "w") as file:
		file.write(str( 0 ))


# CRAPLOG HAS DONE HIS JOB
print("\n\n\
   FFFFF  II  N   N\n\
   F      II  NN  N\n\
   FFF    II  N N N\n\
   F      II  N  NN\n\
   F      II  N   N\n\n")
