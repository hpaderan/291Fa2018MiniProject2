from bsddb3 import db

def main():
    termsDb = db.DB()
    priceDb = db.Db()
    datesDb = db.DB()
    adsDb = db.DB()
    termsDb.open('te.idx',None,db.DB_BTREE,db.DB_CREATE)
    priceDb.open('pr.idx',None,db.DB_BTREE,db.DB_CREATE)
    datesDb.open('da.idx',None,db.DB_BTREE,db.DB_CREATE)
    adsDb.open('ad.idx',None,db.DB_HASH,db.DB_CREATE)
    while (True):
        query = input("Please enter query or enter quit")
        if query == 'quit':
            break
        brifeoutput = True
        option = input("Do you want to change the format of output y/n?")
        if option == 'y':
            out_put_format = input("please enter the format")
            if out_put_format == 'output=full':
                brifeoutput = False
            elif out_put_format == 'output=brief':
                brifeoutput = True
            else:
                print("incorrect input enter output=full or output=brief")
        
        if brifeoutput :
            titlesearch()
        else:
            wholesearch()