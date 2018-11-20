// Cmput 291 Fall 2018
// Mini-Project 2

// Phase 1: Preparing Data Files
#include <stdio.h>

int main () {
    '''-------------------------------------'''
    //read text; maybe iterate per line?
    //make list; maybe struct?
        

    // terms.txt -> terms: ad id
        //create writable file
        //for each iteration:
            //scan each keyword, split?
            //check len > 2
            //write on file with adid

    // pdaes.txt -> date: ad id, category, locaion
        //create writable file
        //for each iteration:
            //scan ad id
            //scan date
            //scan loc
            //scan cat
            //write all to file 
            // d:a,c,l
            //scan to end? \n

    // prices.txt -> prices: ad id, category, location
        //create writable file
        //for each iteration:
            //scan ad id
            //scan location
            //scan category
            //skip scan until prices
            //write to file
            // p:a,c,l
            //scan to end

    // ads.txt -> ad id: full record
    '''-------------------------------------'''
    //read input file
    //create output files
    // struct Ads
    // for each line of input [check for EOF]:
        //get info
        //create struct
        // write onto outputs using struct info.

        //ads.txt
            //write full record

        //terms.txt
            //split
            //for each split: write term : ad id
        
        //pdate.txt
            // write pdate: ad id, category, location

        //prices.txt
            // write prices: ad id, category, location
    
}

