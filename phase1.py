# 291 Fall 2018 - Mini Project 2 - Harrold Paderan
# Phase 1
import os
import re
import sys

def main ():
    currDir = os.getcwd()
    inpFile = open(currDir + "/"+sys.argv[1], "r")
    #read input file
    
    ##create output files
    termsOut = open("terms.txt", "w")
    pdatesOut = open("pdates.txt", "w")
    pricesOut = open("prices.txt", "w")
    adsOut = open("ads.txt", "w")
    
    #termsOut.write("Test 1")
    #pdatesOut.write("Test 1")
    #pricesOut.write("Test 1")
    #adsOut.write("Test 1")
    
    ##HARDCODED IGNORE
    ignoretemp = inpFile.readline()
    while (str.startswith(ignoretemp,"<ad>") == False):
        ignoretemp = inpFile.readline()
        
    #init loop
    currAd = ignoretemp
    #currAd = inpFile.readline()
    infoBuff = currAd.partition("<ad>")
    aid = 0
    pdate = ""
    loc = ""
    cat = ""
    title = ""
    desc = ""
    price = 0
    
    #for each line of input [check for EOF]:
    while infoBuff[0] != "</ads>":
        if infoBuff[0] == '':
            break        
        #----------- read ad info -------------------
        infoBuff = infoBuff[2].partition("<aid>")
        
        #aid
        infoBuff = infoBuff[2].partition("</aid><date>")
        aid = int(infoBuff[0])
        
        #pdate
        infoBuff = infoBuff[2].partition("</date><loc>")
        pdate = infoBuff[0]
        
        #loc
        infoBuff = infoBuff[2].partition("</loc><cat>")
        loc = infoBuff[0]
        
        #cat
        infoBuff = infoBuff[2].partition("</cat><ti>")
        cat = infoBuff[0]
        
        #title
        infoBuff = infoBuff[2].partition("</ti><desc>")
        title = infoBuff[0]
        
        #desc
        infoBuff = infoBuff[2].partition("</desc><price>")
        desc = infoBuff[0]
        
        #price
        infoBuff = infoBuff[2].partition("</price></ad>")
        price = int(infoBuff[0])        
        
        currAd = inpFile.readline()
        infoBuff = currAd.partition("<ad>")
        
        '''===================================================================='''
        #------- Write to output -----------
        
        #//terms.txt
            #//split
             #title split
        titleTerms = title.split(" ")
        
        for tiTerm in titleTerms:
            tempTerm = ""
            # case if alnum
            if (re.match("^[A-Za-z0-9_-]*$", tiTerm)):
                newTerm = tiTerm
            # case if special chars found
            else:
                i = 0
                prev =''
                # check each char in string
                while i < len(tiTerm):
                    # if found coded special character
                    if (tiTerm[i] == '&'):
                        # case if eg. tiTerm = &#123; -> ignore
                        if ((i < (len(tiTerm) - 1)) and tiTerm[i+1] == '#'):
                            while (tiTerm[i] != ';' and i < len(tiTerm)):
                                i+=1
                        #case if eg tiTerm = &apos; -> treat as separator
                        else:
                            while (tiTerm[i] != ';' and i < len(tiTerm)):
                                i+=1
                            titleTerms.append(tiTerm[i:])
                            break
                        # if found '.' : take last part of string and add to titleTerms list for checking
                    elif ((re.match("^[A-Za-z0-9_-]*$", tiTerm[i]) == None)):
                        titleTerms.append(tiTerm[i+1:])
                        break
                    
                    # look if alnum, if so then append to string placeholder
                    if (re.match("^[A-Za-z0-9_-]*$", tiTerm[i])):
                        tempTerm+=tiTerm[i]
                    
                    # update prev for checking for special coded chars
                    #prev = tiTerm[i]
                    
                    i+=1
                    # -------------end of while loop--------------
                        
                # end of search, print found string sequence
                newTerm = tempTerm
            
            # check length of found string: if so then record
            if len(newTerm) > 2:
                termsOut.write("%s:%d\n" % (newTerm.lower(),aid))
            
        '''-----------------------------------------------------------------'''
                 
        #desc split
        descTerms = desc.split(" ")
            
        for deTerm in descTerms:
            tempTerm = ""
            # case if alnum
            if (re.match("^[A-Za-z0-9_-]*$", deTerm)):
                newTerm = deTerm
                
            #case if special chars found
            else:
                i = 0
                #prev = ''
                # check each char in string
                while i < len(deTerm):
                    #if found coded special char
                    if (deTerm[i] == '&'):
                        # case if eg. deTerm = &#123; -> ignore
                        if ((i < len(deTerm) - 1) and (deTerm[i+1] == '#')):
                            while (deTerm[i] != ';' and i < len(deTerm)):
                                i+=1
                        # case if eg. deTerm = &apos; -> treat as separator
                        else:
                            while (deTerm[i] != ';' and i < len(deTerm)):
                                i+=1
                            descTerms.append(deTerm[i:])
                            break
                    # if found special char -> treat as separator
                    elif ((re.match("^[A-Za-z0-9_-]*$", deTerm[i]) == None)):
                        descTerms.append(deTerm[i+1:])
                        break
                    
                    # check if char is valid
                    if (re.match("^[A-Za-z0-9_-]*$", deTerm[i])):
                        tempTerm+=deTerm[i]
                    # update prev for checking for special coded chars
                    #prev = deTerm[i]
                    
                    # loop counter
                    i+=1
                    # -------------end of while loop--------------                    
    
                newTerm = tempTerm
                    
            if len(newTerm) > 2:
                termsOut.write("%s:%d\n" % (newTerm.lower(),aid))
                 
            #//for each split: write term : ad id
        '''===================================================================='''
        #//pdate.txt
            #// write pdate: ad id, category, location
        pdateLine = "%s:%d,%s,%s" % (pdate,aid,cat,loc)
        pdatesOut.write(pdateLine + "\n")
        '''===================================================================='''

        #//prices.txt
            #// write prices: ad id, category, location
        pricesLine = "%8d:%d,%s,%s" % (price,aid,cat,loc)
        pricesOut.write(pricesLine + "\n")
        '''===================================================================='''
        
        #ads.txt
        # write full record
        adsLine = "%d:<ad><aid>%d</aid><date>%s</date><loc>%s</loc><cat>%s</cat><ti>%s</ti><desc>%s</desc><price>%d</price></ad>" % (aid,aid,pdate,loc,cat,title,desc,price)
        adsOut.write(adsLine + "\n")        
    #---end of loop---
            
    # close all files
    inpFile.close()
    termsOut.close()
    pdatesOut.close()
    pricesOut.close()
    adsOut.close()
        

main()
