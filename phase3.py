from bsddb3 import db
import re
import operator

def main():
    termsDb = db.DB()
    priceDb = db.Db()
    datesDb = db.DB()
    adsDb = db.DB()
    termsDb.open('te.idx',None,db.DB_BTREE,db.DB_CREATE)
    priceDb.open('pr.idx',None,db.DB_BTREE,db.DB_CREATE)
    datesDb.open('da.idx',None,db.DB_BTREE,db.DB_CREATE)
    adsDb.open('ad.idx',None,db.DB_HASH,db.DB_CREATE)
	termcursor = termsDb.cursor()
	pricecursor = priceDb.cursor()
	datescursor = datesDb.cursor()
	adscursor = adsDb.cursor()
	
	# init output type to brief, change accordingly
	briefoutput = True
    while (True):
		# prompt
        query = input("Please enter query, or enter 'Quit'")

		'''--------------------------------------------------------'''
		tempQu = ''
		i = 0
		while i < len(query):
			if (re.match("[=<>%]", query[i])):
				if (re.match("[=]", query[i+1])):
					tempQu+=(" " + query[i] + query[i+1] + " ")
					i+=1
				else:
					tempQu+=(" " + query[i] + " ")
			else:
				tempQu+=(query[i])
			
			i+=1


		query = tempQu

		'''--------------------------------------------------------'''
		# split query keywords
		args = query.split(" ")

		# case if user wants to quit
		if 'quit' in args:
			break

'''		# change output type
		if "output=brief" in args:
			briefoutput = True
		elif "output=full" in args:
			briefoutput = False
'''
		# list of queries
		finalRes = []
		tempRes = []
		isFirst = True

		# string patterns for parsing
		datePattern = re.compile("\d{4}/\d{2}/\d{2}")
		ops = {"=":operator.eq, ">":operator.gt, ">=":operator.ge, "<":operator.lt, "<=":operator.le}

		# iterate for each search argument
		i = 0
		while i < len(args):
			#aid
			'''if arg[i].lower() == "aid":
				compOp = args[i+1]
				compVal = args[i+2]

				# sql search here!!!!!!!!!!
				#queries.append("aid=%s" % compVal.lower())
				searchInDB(args[i],compOp,compVal, adscurs,adsdb)

				# ignore next two args: the search values
				i+=2
			
			#location
			el'''
			if args[i].lower() == "location":
				compOp = args[i+1]
				compVal = args[i+2]

				# sql search here!!!!!!!!!!!
				#if tempRes is empty
				tempRes = searchInDB(args[i],compOp,compVal, curs,adsdb)
				output.append(someOut)
				# ignore next two args: the search values
				i+=2

			#category
			elif args[i].lower() == "cat":
				compOp = args[i+1]
				compVal = args[i+2]

				# search here!!!!!!!!!!!
				tempRes = CatSearch(compVal, adscursor)

				# ignore next two args: the search values
				i+=2

			#date
			elif args[i].lower() == "date":
				compOp = args[i+1]
				compVal = args[i+2]

				# search here
				tempRes = DateSearch (compVal, compOp, ops, datescursor)

				# ignore next two args: the search values
				i+=2
			#price
			elif args[i].lower() == "price":
				compOp = args[i+1]
				compVal = args[i+2]

				# sql search here
				queries.append("price=%s" % compVal.lower())
				
				# ignore next two args: the search values
				i+=2

			#output: treat 'output' as not a term
			elif args[i].lower() == "output":
				compOp = args[i+1]
				compVal = args[i+2]

				if (compVal.lower() == "brief"):
					briefoutput = True
				elif (compVal.lower() == "full"):
					briefoutput = False

			# % at end of term
			elif (args[i] == "%"):
				# assume % will never appear in beginning 
				compVal = args[i-1]
				tempRes = LikeTermSearch(compVal, termcursor)

			#terms: title, desc
			else:
				#Query the term provided
				tempRes = TermSearch(args[i], termcursor)


			# intersect onto a final result list with very query				
			if not isFirst:
				finalRes = [value for value in some1 if value in some2]
			else:
				finalRes = tempRes
				isFirst = False

			i+=1
			#--------------end while loop-----------

		#----------_QUERIES_------------------------
	


		#------------_Output_-------------------------			

		if briefoutput :
			# display ad id and title only
			briefprint()
		else:
			# display full record
			fullprint()
		
		

		# invidivual query done
		print("Query complete.")


def CatSearch (cat, cursor):
	cat = cat.lower()
	item = cursor.first()
	retAids = []
	# iterate through database
	while item:
		# get category from ads database
		ad = str(item[1].decode("utf-8"))
		tempSearch = re.search("<cat>(.*)</cat>", ad)
		if tempSearch == cat:
			retAids.append(item[0].decode('utf-8'))

		# loop terminator
		item = cursor.next
	return retAids

def DateSearch (date, searchOp, ops, cursor):
	item = cursor,first()
	retAids = []
	#iterate through database
	while item:
		# get date from datesDb and compare with provided, append aid if true
		itemDate = str(item[0].decode("utf-8"))
		if ops[searchOp](itemDate, date):
			info = str(item[1].decode("utf-8"))
			aid = info.split(",")[0]
			retAids.append(aids)
		
		#loop terminator
		item = cursor.next()

	return retAids

def TermSearch (term, cursor):
	term = term.lower()
	item = cursor.first()
	retAids = []
	#iterate through database
	while item:
		#if compare term to key is true, append aid
		dbKey = str(item[0].decode("utf-8"))
		if (term == dbKey):
			info = str(item[1].decode("utf-8"))
			retAids.append(info)

		# loop terminator
		item = cursor.next()

def LikeTermSearch (term, cursor):
	term = term.lower()
	item = cursor.first()
	retAids = []
	#iterate through database
	while item:
		#if compare term to key is true, append aid
		dbKey = str(item[0].decode("utf-8"))
		if (dbKey.lower().startswith(term)):
			info = str(item[1].decode("utf-8"))
			retAids.append(info)

		# loop terminator
		item = cursor.next()

def briefprint(aids):
	#get all withaids and print

def fullprint(aids):
