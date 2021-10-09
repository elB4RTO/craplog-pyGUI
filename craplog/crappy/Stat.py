from collections import Counter

def Access():

	print(" Created statistics from ACCESS LOGs")

	# IPs
	with open("./STATS/.IP.crap", "r") as file:
		LOGlist = file.read()

	CheckList	= []
	LOGlist		= LOGlist.split()
	count		= Counter(LOGlist)
	LOGlist		= (sorted(LOGlist, key=lambda x: (count[x], x), reverse=True))

	with open("./STATS/IP.crapstats", "a") as file:
		for ip in LOGlist:
			if ip in CheckList:
				continue
			else:
				CheckList.append(ip)
				file.write("{ %s }   >>>   %s\n-\n" %( LOGlist.count(ip), ip ))


	# REQUESTS
	with open("./STATS/.REQ.crap", "r") as file:
		LOGlist = file.read()

	CheckList	= []
	LOGlist		= LOGlist.split("\n")
	count		= Counter(LOGlist)
	LOGlist		= (sorted(LOGlist, key=lambda x: (count[x], x), reverse=True))

	with open("./STATS/REQ.crapstats", "a") as file:
		for req in LOGlist:
			if req in CheckList:
				continue
			else:
				CheckList.append(req)
				if req.startswith('OPTIONS'):
					req_t = req.split(" ")
					rq_t = ""
					for rq in req_t:
						if rq.startswith('OPTIONS'):
							rq_t += rq + " * "
						elif rq.startswith('HTTP/'):
							rq_t += rq
					file.write("{ %s }   >>>   %s\n-\n" %( LOGlist.count(req), rq_t ))
				else:
					file.write("{ %s }   >>>   %s\n-\n" %( LOGlist.count(req), req ))


	# RESPONSES
	with open("./STATS/.RES.crap", "r") as file:
		LOGlist = file.read()

	CheckList	= []
	LOGlist_tmp	= []
	LOGlist		= LOGlist.split("\n")
	LOGlist		= (sorted(LOGlist, key=lambda x: (count[x], x), reverse=True))

	for res in LOGlist:
		res = str(res.strip()[:3])
		LOGlist_tmp.append(res)

	count	= Counter(LOGlist_tmp)
	LOGlist	= sorted(LOGlist_tmp, key=count.get, reverse=True)

	with open("./STATS/RES.crapstats", "a") as file:
		for res in LOGlist:
			if res in CheckList:
				continue
			else:
				CheckList.append(res)
				file.write("{ %s }   >>>   %s\n-\n" %( LOGlist.count(res), res ))


	# USER AGENTS
	with open("./STATS/.UA.crap", "r") as file:
		LOGlist = file.read()

	CheckList	= []
	LOGlist		= LOGlist.split("\n")
	count		= Counter(LOGlist)
	LOGlist		= (sorted(LOGlist, key=lambda x: (count[x], x), reverse=True))

	file = open("./STATS/UA.crapstats", "a")
	for ua in LOGlist:
		if ua in CheckList:
			continue
		else:
			CheckList.append(ua)
			file.write("{ %s }   >>>   %s\n-\n" %( LOGlist.count(ua), ua ))



def Error():
	print(" Created statistics from ERROR LOGs")

	# LEVs
	with open("./STATS/.LEV.crap", "r") as file:
		LOGlist = file.read()

	CheckList	= []
	LOGlist		= LOGlist.split('\n')
	count		= Counter(LOGlist)
	LOGlist		= (sorted(LOGlist, key=lambda x: (count[x], x), reverse=True))

	with open("./STATS/LEV.crapstats", "a") as file:
		for lev in LOGlist:
			if lev in CheckList or lev == "::1":
				continue
			else:
				CheckList.append(lev)
				file.write("{ %s }   >>>   %s\n-\n" %( LOGlist.count(lev) , lev ))

	# ERRs
	with open("./STATS/.ERR.crap", "r") as file:
		LOGlist = file.read()

	CheckList	= []
	LOGlist		= LOGlist.split('\n')
	count		= Counter(LOGlist)
	LOGlist		= (sorted(LOGlist, key=lambda x: (count[x], x), reverse=True))

	with open("./STATS/ERR.crapstats", "a") as file:
		for err in LOGlist:
			if err in CheckList or err == "::1":
				continue
			else:
				CheckList.append(err)
				file.write("{ %s }   >>>   %s\n-\n" %( LOGlist.count(err) , err ))
