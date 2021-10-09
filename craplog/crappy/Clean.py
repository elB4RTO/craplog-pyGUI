
def Access(CleanAccessLogs):
	if CleanAccessLogs:
		print(" Created CLEAN file from ACCESS LOGs")

	# MODIFY THE NEXT LINE IF YOUR LOG PATH IS DIFFERENT
	with open("/var/log/apache2/access.log.1", "r") as file:
		LOGlist = file.read()

	LOGlist		= LOGlist.split('\n')
	LOGlist_tmp	= []

	for log in LOGlist:
		if log.startswith('192.168.') or log.startswith('::1') or log == '':
			continue
		else:
			LOGlist_tmp.append(log)

	LOGlist		= LOGlist_tmp
	LOGlist_tmp = []
	log_check	= ""
	
	if CleanAccessLogs:
		with open("./STATS/CLEAN.access.log", "a") as file:
			for log in LOGlist:
				log_tmp	= log.split(' ')[0]
				if log_tmp == log_check:
					file.write("\n%s\n" %( log ))
				else:
					if len(LOGlist_tmp) == 0:
						file.write("%s\n" %( log ))
						LOGlist_tmp.append(log)
					else:
						file.write("\n\n%s\n" %( log ))
					log_check = log_tmp

	with open("./STATS/.IP.crap", "a") as file:
		for log in LOGlist:
			log = log.split(' ')[0]
			file.write("%s\n" %( log ))

	req_file = open("./STATS/.REQ.crap", "a")
	res_file = open("./STATS/.RES.crap", "a")
	ua_file  = open("./STATS/.UA.crap", "a")

	for log in LOGlist:
		log = log.split('"')
		
		req = log[1]
		req_file.write("%s\n" %( req ))

		res = log[2].strip()[:3]
		res_file.write("%s\n" %( res ))

		ua = log[5]
		ua_file.write("%s\n" %( ua ))
	
	req_file.close()
	res_file.close()
	ua_file.close()



def Error():
	
	# MODIFY THE NEXT LINE IF YOUR LOG PATH IS DIFFERENT
	with open("/var/log/apache2/error.log.1", "r") as file:
		LOGlist = file.read()

	LOGlist = LOGlist.strip().split('\n')

	err_file = open("./STATS/.ERR.crap", "a")
	lev_file = open("./STATS/.LEV.crap", "a")

	for log in LOGlist:
		if log != '':
			log = log.split('[')

			lev_file.write("%s\n" %( log[2].strip(' ]') ))

			if log[3].startswith('pid') and log[3].endswith('] '):
				err_file.write("%s\n" %( log[4].split(']')[1].strip() ))
			else:
				err_file.write("%s\n" %( log[3].split(']')[1].strip() ))

	err_file.close()
	lev_file.close()
