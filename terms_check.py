def main ():
    f1 = open ("terms.txt", "r")
    f2 = open ("input2.txt","r")
    
    lines2 = f2.readlines()
    print (len(lines2))
    
    line1Count = 0
    
    for i in range(243):
        line1 = f1.readline()
        line1Count += 1
        if line1 not in lines2:
            print (line1)
        
    print(line1Count)

    
main()