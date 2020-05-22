#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define BASE 13
char basechars[BASE + 1] = "angstromctf20";

/*
void tobase(ulo n, char *ret) {
    ret[BL] = 0;
    for (int i = BL - 1; i >= 0; --i) {
        ret[i] = basechars[n % BASE];
        n /= BASE;
    }
}

if (strcmp(c1, "artomtf2srn00tgm2f") || strcmp(c2, "ng0fa0mat0tmmmra0c") ||
    strcmp(c3, "ngnrmcornttnsmgcgr") || strcmp(c4, "a0fn2rfa00tcgctaot")) {
*/

char* s[4] = {"artomtf2srn00tgm2f",
			  "ng0fa0mat0tmmmra0c",
			  "ngnrmcornttnsmgcgr",
			  "a0fn2rfa00tcgctaot"
			 };

int main()
{
	int i, j;
	char* ptr;
	unsigned long long n[4];
	for(i = 0; i < 4; i++){
		n[i] = BASE*9*10000000000000000;
		for(j = 0; j < BASE; j++){
			ptr = strchr(basechars, s[i][j]);
			if(ptr == NULL){
				printf("error");
				exit(1);
			}
			n[i] += (int)(ptr - basechars);
			n[i] *= BASE;
		}
		n[i] /= BASE;
	}
	n[1] = ~n[1];
	printf("%llx, %llx, %llx, %llx\n", n[0], n[1], n[2], n[3]);
	
}
