from bsddb3 import db
import re

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
	adscursor = dasDb.cursor()
	
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

		# change output type
		if "output=brief" in args:
			briefoutput = True
		elif "output=full" in args:
			briefoutput = False

		# list of queries
		queries = []

		# string patterns for parsing
		datePattern = re.compile("\d{4}/\d{2}/\d{2}")

		# iterate for each search argument
		i = 0
		while i < len(args):
			#aid
			if arg[i].lower() == "aid":
				compOp = args[i+1]
				compVal = args[i+2]

				# sql search here!!!!!!!!!!
				queries.append("aid=%s" % compVal.lower())

				# ignore next two args: the search values
				i+=2
			
			#location
			elif args[i].lower() == "location":
				compOp = args[i+1]
				compVal = args[i+2]

				# sql search here!!!!!!!!!!!
				queries.append("location=%s" % compVal.lower())

				# ignore next two args: the search values
				i+=2

			#category
			elif args[i].lower() == "cat":
				compOp = args[i+1]
				compVal = args[i+2]

				# sql search here!!!!!!!!!!!
				queries.append("cat=%s" % compVal.lower())

				# ignore next two args: the search values
				i+=2

			#date
			elif args[i].lower() == "date":
				compOp = args[i+1]
				compVal = args[i+2]

				# sql search here
				queries.append("date=%s" % compVal.lower())

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

			#output
			elif args[i].lower() == "output":
				print("Do nothing")

			#keywords: title desc
			else:
				#Query the term provided
				queries.append(args[i])




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
