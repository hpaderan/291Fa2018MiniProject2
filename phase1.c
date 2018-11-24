// Cmput 291 Fall 2018
// Mini-Project 2

// Phase 1: Preparing Data Files
#include <stdio.h>

int main () {
    FILE * inputFile, termsText, pdatesText, pricesText, adsText;
    int aid;
    char pdate[];
    char loc[];
    char cat[];
    char title[30]:
    char desc[150];
    int price;

    //read input file
    input file = fopen("./input.txt", 'r');

    //create output files
    termsText = fopen("./terms.txt", "w+");

    // for each line of input [check for EOF]:
        //get info
        fscanf(inputFile, "%*[^<ad>]");

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

