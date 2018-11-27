from bsddb3 import db
import re
import operator

def main():
    termsDb = db.DB()
    pricesDb = db.DB()
    datesDb = db.DB()
    adsDb = db.DB()
    termsDb.open('te.idx',None,db.DB_BTREE,db.DB_CREATE)
    pricesDb.open('pr.idx',None,db.DB_BTREE,db.DB_CREATE)
    datesDb.open('da.idx',None,db.DB_BTREE,db.DB_CREATE)
    adsDb.open('ad.idx',None,db.DB_HASH,db.DB_CREATE)
    termcursor = termsDb.cursor()
    pricecursor = pricesDb.cursor()
    datescursor = datesDb.cursor()
    adscursor = adsDb.cursor()

    #init output type to brief, change accordingly
    briefoutput = True
    while(True):
        #prompt
        query = input("Please enter query, or enter 'Quit': ")

        '''-----------------------------------------------------'''
        tempQu = ''
        i = 0
        while i < len(query):
            if (re.match("[=<>]", query[i])):
                if (query[i+1] == "="):
                    tempQu+=(" " + query[i]+query[i+1] + " ")
                    i+=1
                else:
                    tempQu+=(" " + query[i] + " ")
                
            else:
                tempQu+=(query[i])
            i+=1
        
        query = tempQu

        '''-----------------------------------------------------'''

        args = query.split()
        #print(args)

        isQuit = False

        finalRes = []
        tempRes = []
        isFirst = True
        
        ops = {"=":operator.eq, ">":operator.gt, ">=":operator.ge, "<":operator.lt, "<=":operator.le}

        i = 0
        while i < len(args):
            if (args[i].lower() == 'quit'):
                isQuit = True
                break

            elif args[i].lower() == "location":
                compOp = args[i+1]
                compVal = args[i+2]

                tempRes = LocationSearch(compVal,adscursor)
                i+=2
            
            elif args[i].lower() == "cat":
                compOp = args[i+1]
                compVal = args[i+2]

                tempRes = CatSearch(compVal,adscursor)
                i+=2

            elif args[i].lower() == "date":
                compOp = args[i+1]
                compVal = args[i+2]

                tempRes = DateSearch(compVal, compOp, ops, datescursor)
                i+=2

            elif args[i].lower() == 'price':
                compOp = args[i+1]
                compVal = args[i+2]

                tempRes = PriceSearch(compVal, compOp, ops, pricecursor)
                i+=2

            elif args[i].lower() == "output":
                compOp = args[i+1]
                compVal = args[i+2]

                if (compVal.lower() == "brief"):
                    briefoutput = True
                else:
                    briefoutput = False

                i+=2
            
            else:
                if (args[i][-1] == "%"):
                    compVal = str(args[i][:len(args[i])-1])
                    tempRes = LikeTermSearch(compVal, termcursor)
                else:
                    tempRes = TermSearch(args[i], termcursor)

            i+=1
        

            if not isFirst:
                bufferList = [value for value in tempRes if value in finalRes]
                finalRes = bufferList
            else:
                finalRes = tempRes
                isFirst = False
        #-------------- end of while loop ---------------

        if isQuit:
            break

        
        if briefoutput:
            briefprint(finalRes,adscursor)
        else:
            fullprint(finalRes,adscursor)
        print("============================================")
        print("Found %d results." % len(finalRes))
        print("============================================")
    #---------------------------------------------------

def CatSearch (cat, cursor):
    cat = cat.lower()
    item = cursor.first()
    retAids = []
    while item:
        info = str(item[1].decode("utf-8"))
        tempSearch = re.search("<cat>(.*)</cat>", info)
        searchRes = tempSearch.group(1)
        if searchRes == cat:
            retAids.append(item[0].decode("utf-8"))
        item = cursor.next()

    return retAids

def DateSearch (date, searchOp, ops, cursor):
    date = date.lower() #obsolete. with the format
    item = cursor.first()
    retAids = []
    while item != None:
        searchRes = str(item[0].decode("utf-8"))
        if (ops[searchOp](searchRes, date)):
            info = str(item[1].decode("utf-8"))
            infbuff = info.split(",")[0]
            retAids.append(infbuff)
        item = cursor.next()

    return retAids
    
def TermSearch (term, cursor):
    term = term.lower()
    itemB = (cursor.first())
    item = itemB[0].decode("utf-8")
    retAids = []
    while not(itemB == None):
        if (term == item.lower()):
            info = str(itemB[1].decode("utf-8"))
            retAids.append(info)

        itemB = (cursor.next())
        if not (itemB == None):
            item = itemB[0].decode("utf-8")
        else:
            item = None

    return retAids

def LikeTermSearch (term, cursor):
    term = term.lower()
    itemB = cursor.first()
    item = itemB[0].decode("utf-8")
    retAids = []
    while itemB != None:
        if (item.lower()).startswith(term):
            info = str(itemB[1].decode("utf-8"))
            retAids.append(info)

        itemB = cursor.next()
        if (itemB != None):
            item = itemB[0].decode("utf-8")
        else:
            item = None

    return retAids

def LocationSearch (arguments, curs):
    arguments = arguments.lower()
    cursor = curs.first()
    Aids = []
    while cursor != None:
        cursor_str = str(cursor[1].decode("utf-8"))
        result = re.search("<loc>(.*)</loc>",cursor_str)
        location_part = result.group(1)
        if (location_part.lower() == arguments):
            Aids.append(cursor[0].decode("utf-8"))
        cursor = curs.next()    

    return Aids

def PriceSearch (price, searchOp, ops, cursor):
    price = int(price)
    item = cursor.first()
    retAids = []
    while item != None:
        itemPrice = int(item[0].decode("utf-8"))
        if ops[searchOp](itemPrice, price):
            info = str(item[1].decode("utf-8"))
            infbuff = info.split(",")[0]
            retAids.append(infbuff)
        item = cursor.next()

    return retAids

def briefprint(aids, cursor):
    for aid in aids:
        item = cursor.first()
        while item:
            decItem = item[0].decode("utf-8")
            if (aid == decItem):
                pAidS = re.search("<aid>(.*)</aid>", item[1].decode("utf-8"))
                pAid = pAidS.group(1)
                tiS = re.search("<ti>(.*)</ti>", item[1].decode("utf-8"))
                ti = tiS.group(1)
                strFormat = "Aid: %s\nTitle: %s\n-------------------------------"
                print(strFormat % (pAid,ti))
                break
            item = cursor.next()
            

def fullprint (aids, cursor):
    for aid in aids:
        item = cursor.first()
        while item:
            if (aid == item[0].decode("utf-8")):
                pAidS = re.search("<aid>(.*)</aid>", item[1].decode("utf-8"))
                pAid = pAidS.group(1)
                dateS = re.search("<date>(.*)</date>", item[1].decode("utf-8"))
                date = dateS.group(1)
                locS = re.search("<date>(.*)</date>", item[1].decode("utf-8"))
                loc = locS.group(1)
                catS = re.search("<cat>(.*)</cat>", item[1].decode("utf-8"))
                cat = catS.group(1)
                tiS = re.search("<ti>(.*)</ti>", item[1].decode("utf-8"))
                ti = tiS.group(1)
                descS = re.search("<desc>(.*)</desc>", item[1].decode("utf-8"))
                desc = descS.group(1)
                priceS = re.search("<price>(.*)</price>", item[1].decode("utf-8"))
                price = priceS.group(1)
                strFormat = "Aid: %s\nDate: %s\nLocation: %s\nCategory: %s\nTitle: %s\nDescription: %s\nPrice: %s\n-------------------------------"
                print(strFormat % (pAid,date,loc,cat,ti,desc,price))
                break
            item = cursor.next()
	

main()