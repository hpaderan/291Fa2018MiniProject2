from bsddb3 import db
import re
import operator

def main():
    termsDb = db.DB()
    priceDb = db.DB()
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
        query = input("Please enter query, or enter 'Quit': ")

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
                        print("locations")
                        compOp = args[i+1]
                        compVal = args[i+2]

			# sql search here!!!!!!!!!!!
                        loc_aid = LocationSearch(compVal,adscursor)
			# ignore next two args: the search values
                        i+=2

			#category
                    elif args[i].lower() == "cat":
                        print("cat")
                        compOp = args[i+1]
                        compVal = args[i+2]

			# search here!!!!!!!!!!!
                        tempRes = CatSearch(compVal, adscursor)

			# ignore next two args: the search values
                        i+=2

			#date
                    elif args[i].lower() == "date":
                        print("date")
                        compOp = args[i+1]
                        compVal = args[i+2]

			# search here
                        tempRes = DateSearch (compVal, compOp, ops, datescursor)

			# ignore next two args: the search values
                        i+=2
			#price
                    elif args[i].lower() == "price":
                        print("price")
                        compOp = args[i+1]
                        compVal = args[i+2]
			
			# sql search here
                        PriceSearch (compOp,compVal, ops, cursor)
				
			# ignore next two args: the search values
                        i+=2

			#output: treat 'output' as not a term
                    elif args[i].lower() == "output":
                        print("output")
                        compOp = args[i+1]
                        compVal = args[i+2]

                        if (compVal.lower() == "brief"):
                            briefoutput = True
                        elif (compVal.lower() == "full"):
                            briefoutput = False

			# % at end of term
                    elif (args[i] == "%"):
                        print("term extra")
				# assume % will never appear in beginning 
                        compVal = args[i-1]
                        tempRes = LikeTermSearch(compVal, termcursor)

			#terms: title, desc
                    else:
                        print("term")
				#Query the term provided
                        tempRes = TermSearch(args[i], termcursor)


			# intersect onto a final result list with very query				
                    if not isFirst:
                        print(tempRes, len(finalRes))
                        finalRes = [value for value in some1 if value in some2]
                    else:
                        print(tempRes, len(finalRes), '2')
                        finalRes = tempRes
                        isFirst = False

                    i+=1
		    #--------------end while loop-----------

		#------------_Output_-------------------------
                print("OVERHERE 0")
                print(finalRes, "OVER HERE")

                if briefoutput :
			# display ad id and title only
                    briefprint(finalRes, adscursor)
                else:
			# display full record
                    fullprint(finalRes, adscursor)
		
		

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
	return retAids

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
	return retAids
		
def LocationSearch(argument,curs):
    argument = argument.lower()
    cursor = curs.first()
    Aids = []
    while cursor != None:
        cursor_str = str(cursor[1].decode("utf-8"))
        result = re.search('<loc>(.*)<loc/>',cursor_str)
        location_part = result.group(1)
        if (location_part.lower() == argument):
            Aids.append(cursor[0].decode("utf-8"))
    
    return Aids


def PriceSearch (searchOp,price,ops, cursor):
	item = cursor,first()
	retAids = []
	#iterate through database
	while item:
		itemPrice = str(item[0].decode("utf-8"))
		if ops[searchOp](itemPrice, price):
			info = str(item[1].decode("utf-8"))
			aid = info.split(",")[0]
			retAids.append(aids)
		cursor.next()

	return retAids

def briefprint(aids, cursor):
	# print aid and title
	for aid in aids:
		item = cursor.first()
		while item:
			if (aid == item[0].decode("utf-8")):
				pAid = re.search("<aid>(.*)</aid>", item[1])
				ti = re.search("<ti>(.*)</ti>", item[1])
				strFormat = "Aid: %s\nTitle: %s\n-------------------------------"
				print(strFormat % (pAid,ti))

def fullprint(aids, cursor):
	# print full details
	for aid in aids:
		item = cursor.first()
		while item:
			if (aid == item[0].decode("utf-8")):
				pAid = re.search("<aid>(.*)</aid>", item[1])
				date = re.search("<date>(.*)</date>", item[1])
				loc = re.search("<loc>(.*)</loc>", item[1])
				cat = re.search("<cat>(.*)</cat>", item[1])
				ti = re.search("<ti>(.*)</ti>", item[1])
				desc = re.search("<desc>(.*)</desc>", item[1])
				price = re.search("<price>(.*)</price>", item[1])
				strFormat = "Aid: %s\nDate: %s\nLocation: %s\nCategory: %s\nTitle: %s\nDescription: %s\nPrice: %s\n-------------------------------"
				print(strFormat % (pAid,date,loc,cat,ti,desc,price))
				
main()