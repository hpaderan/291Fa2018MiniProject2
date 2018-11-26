def main ():
    f1 = open ("terms.txt", "r")
    f2 = open ("input2.txt","r")
    
    lines1 = f1.readlines()
    lines2 = f2.readlines()
    print (len(lines2))
    
    line1Count = 0
    mismatchcount = 0
    
    for i in range(len(lines1)):
        #line1 = f1.readline()
        line1Count += 1
        if lines1[i] not in lines2:
            mismatchcount+= 1
            print (lines1[i])
        
    print(line1Count, mismatchcount)

    
main()