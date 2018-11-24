#include <stdio.h>

int main () {
    FILE *inpTest, *outTest;
    char chartest[4];

    inpTest = fopen("./testtest.txt", "r");
    outTest = fopen("./outtest.txt", "w");

    fscanf(inpTest, "<ad><aid>%s</aid></ad>", &chartest);

    printf("Whatever test print here");
    
    fprintf(outTest, "This is basic printing test.");
    fprintf(outTest, "We got this file. I think. %s", chartest);

    return 1;
}