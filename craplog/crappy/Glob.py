
def Access():

	print(" Updated GLOBAL statistics of ACCESS LOGs")
	
	def RetrieveSessionStats():
		nonlocal LOGlist_tmp, LOGlist, LOGcount
		for line in LOGlist_tmp:
			line = line.strip()
			if len(line) > 2:
				line	= line.split('>>>')
				count	= int(line[0].strip('{ }'))
				LOGcount.append(count)
				log = line[1].strip('{ }')
				LOGlist.append(log)
	
	def UpdateGlobals(path):
		nonlocal LOGlist, LOGcount, G_LOGlist_tmp, G_LOGlist, G_LOGcount
		if len(G_LOGlist_tmp) > 2:
			F_LOGlist	= {}
			F_LOGcount	= {}
			
			for line in G_LOGlist_tmp:
				if len(line) > 2:
					line	= line.split('>>>')
					count	= int(line[0].strip('{ }'))
					G_LOGcount.append(count)
					log = line[1].strip('{ }')
					G_LOGlist.append(log)
			for log in G_LOGlist:
				i		= G_LOGlist.index(log)
				log_Gc	= G_LOGcount[i]
				if log in LOGlist:
					count			= LOGlist.index(log)
					log_i			= LOGlist[count]
					log_c			= LOGcount[count]
					log_Fc			= int(log_Gc) + int(log_c)
					F_LOGcount[log]	= log_Fc
					F_LOGlist[log]	= log
				else:
					F_LOGcount[log]	= int(log_Gc)
					F_LOGlist[log]	= log

			F_LOGarr = ({key: value for key, value in sorted(F_LOGcount.items(), key=lambda item: item[1], reverse=True)})
			with open( path, "a") as file:
				for logs in F_LOGarr.keys():
					count	= F_LOGcount[logs]
					log	= F_LOGlist[logs]
					file.write("{ %s }   >>>   %s\n-\n" %( count, log ))
		else:
			F_LOGlist	= []
			F_LOGcount	= []
			for log in LOGlist:
				if log in F_LOGlist:
					continue
				else:
					count = LOGlist.index(log)
					F_LOGlist.append(LOGlist[count])
					F_LOGcount.append(LOGcount[count])
			with open( path, "a") as file:
				for log in F_LOGlist:
					count = F_LOGlist.index(log)
					file.write("{ %s }   >>>   %s\n-\n" %( F_LOGcount[count] , F_LOGlist[count] ))



	# ACTUAL IPs
	with open("./STATS/IP.crapstats", "r") as file:
		LOGlist_tmp = file.read()

	LOGlist_tmp	= LOGlist_tmp.strip().split("\n")
	LOGlist		= []
	LOGcount	= []

	RetrieveSessionStats()


	# GLOBAL IPs
	with open("./STATS/GLOBALS/.GLOBAL.IP.crap", "r") as file:
		G_LOGlist_tmp = file.read()

	G_LOGlist_tmp	= G_LOGlist_tmp.strip().split("\n")
	G_LOGlist		= []
	G_LOGcount		= []

	UpdateGlobals("./STATS/GLOBALS/GLOBAL.IP.crapstats")



	# ACTUAL REQs
	with open("./STATS/REQ.crapstats", "r") as file:
		LOGlist_tmp = file.read()

	LOGlist_tmp	= LOGlist_tmp.strip().split("\n")
	LOGlist		= []
	LOGcount	= []

	RetrieveSessionStats()


	# GLOBAL REQs
	with open("./STATS/GLOBALS/.GLOBAL.REQ.crap", "r") as file:
		G_LOGlist_tmp = file.read()

	G_LOGlist_tmp	= G_LOGlist_tmp.strip().split("\n")
	G_LOGlist		= []
	G_LOGcount		= []

	UpdateGlobals("./STATS/GLOBALS/GLOBAL.REQ.crapstats")


	# ACTUAL RESs
	with open("./STATS/RES.crapstats", "r") as file:
		LOGlist_tmp = file.read()
	
	LOGlist_tmp	= LOGlist_tmp.strip().split("\n")
	LOGlist		= []
	LOGcount	= []

	RetrieveSessionStats()


	# GLOBAL RESs
	with open("./STATS/GLOBALS/.GLOBAL.RES.crap", "r") as file:
		G_LOGlist_tmp = file.read()

	G_LOGlist_tmp	= G_LOGlist_tmp.strip().split("\n")
	G_LOGlist		= []
	G_LOGcount		= []

	UpdateGlobals("./STATS/GLOBALS/GLOBAL.RES.crapstats")



	# ACTUAL UAs
	with open("./STATS/UA.crapstats", "r") as file:
		LOGlist_tmp = file.read()

	LOGlist_tmp	= LOGlist_tmp.strip().split("\n")
	LOGlist		= []
	LOGcount	= []

	RetrieveSessionStats()


	# GLOBAL UAs
	with open("./STATS/GLOBALS/.GLOBAL.UA.crap", "r") as file:
		G_LOGlist_tmp = file.read()

	G_LOGlist_tmp	= G_LOGlist_tmp.strip().split("\n")
	G_LOGlist		= []
	G_LOGcount		= []

	UpdateGlobals("./STATS/GLOBALS/GLOBAL.UA.crapstats")



def Error():

	print(" Updated GLOBAL statistics of ERROR LOGs")
	
	def RetrieveSessionStats():
		nonlocal LOGlist_tmp, LOGlist, LOGcount
		for line in LOGlist_tmp:
			line = line.strip()
			if len(line) > 2:
				line	= line.split('>>>')
				count	= int(line[0].strip('{ }'))
				LOGcount.append(count)
				log = line[1].strip('{ }')
				LOGlist.append(log)
	
	def UpdateGlobals(path):
		nonlocal LOGlist, LOGcount, G_LOGlist_tmp, G_LOGlist, G_LOGcount
		if len(G_LOGlist_tmp) > 2:
			F_LOGlist	= {}
			F_LOGcount	= {}
			
			for line in G_LOGlist_tmp:
				if len(line) > 2:
					line	= line.split('>>>')
					count	= int(line[0].strip('{ }'))
					G_LOGcount.append(count)
					log = line[1].strip('{ }')
					G_LOGlist.append(log)
			for log in G_LOGlist:
				i		= G_LOGlist.index(log)
				log_Gc	= G_LOGcount[i]
				if log in LOGlist:
					count			= LOGlist.index(log)
					log_i			= LOGlist[count]
					log_c			= LOGcount[count]
					log_Fc			= int(log_Gc) + int(log_c)
					F_LOGcount[log]	= log_Fc
					F_LOGlist[log]	= log
				else:
					F_LOGcount[log]	= int(log_Gc)
					F_LOGlist[log]	= log

			F_LOGarr = ({key: value for key, value in sorted(F_LOGcount.items(), key=lambda item: item[1], reverse=True)})
			with open( path, "a") as file:
				for logs in F_LOGarr.keys():
					count	= F_LOGcount[logs]
					log	= F_LOGlist[logs]
					file.write("{ %s }   >>>   %s\n-\n" %( count, log ))
		else:
			F_LOGlist	= []
			F_LOGcount	= []
			for log in LOGlist:
				if log in F_LOGlist:
					continue
				else:
					count = LOGlist.index(log)
					F_LOGlist.append(LOGlist[count])
					F_LOGcount.append(LOGcount[count])
			with open( path, "a") as file:
				for log in F_LOGlist:
					count = F_LOGlist.index(log)
					file.write("{ %s }   >>>   %s\n-\n" %( F_LOGcount[count] , F_LOGlist[count] ))
		

	# ACTUAL LEVs
	with open("./STATS/LEV.crapstats", "r") as file:
		LOGlist_tmp = file.read()

	LOGlist_tmp	= LOGlist_tmp.strip().split("\n")
	LOGlist		= []
	LOGcount	= []

	RetrieveSessionStats()


	# GLOBAL LEVs
	with open("./STATS/GLOBALS/.GLOBAL.LEV.crap", "r") as file:
		G_LOGlist_tmp = file.read()

	G_LOGlist_tmp	= G_LOGlist_tmp.strip().split("\n")
	G_LOGlist		= []
	G_LOGcount		= []

	UpdateGlobals("./STATS/GLOBALS/GLOBAL.LEV.crapstats")


	# ACTUAL ERRs
	with open("./STATS/ERR.crapstats", "r") as file:
		LOGlist_tmp = file.read()

	LOGlist_tmp	= LOGlist_tmp.strip().split("\n")
	LOGlist		= []
	LOGcount	= []

	RetrieveSessionStats()


	# GLOBAL ERRs
	with open("./STATS/GLOBALS/.GLOBAL.ERR.crap", "r") as file:
		G_LOGlist_tmp = file.read()

	G_LOGlist_tmp	= G_LOGlist_tmp.strip().split("\n")
	G_LOGlist		= []
	G_LOGcount		= []

	UpdateGlobals("./STATS/GLOBALS/GLOBAL.ERR.crapstats")
