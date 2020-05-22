#include <stdio.h>
#include <fcntl.h>
#include <setjmp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/prctl.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>

#include <openssl/sha.h>

#define BASE 13
#define BL 18
#define PASS	8

char basechars[BASE + 1] = "angstromctf20";

char c1[BL+1] = "artomtf2srn00tgm2f";
//char c1[BL+1] = "ng0fa0mat0tmmmra0c";
//char c1[BL+1] = "ngnrmcornttnsmgcgr";
//char c1[BL+1] = "a0fn2rfa00tcgctaot";

void tobase(unsigned long long n, char *ret) {
    ret[BL] = 0;
    for (int i = BL - 1; i >= 0; --i) {
        ret[i] = basechars[n % BASE];
        n /= BASE;
    }
}

int check(unsigned long long n)
{
	int i;
	unsigned char c;
	for(i = 0; i < 8; i++){
		c = (unsigned char)(n & 0xff);
		if( c <= '!' || c >= '}'){
			return -1;
		}
		n >>= 0x8;
	}
	return 0;	
}

int main(int argc, char *argv[])
{
	unsigned long long n1;
	char *diff;
	unsigned long long i;
	int j;
	
	scanf("%llx", &i);
	n1 = BASE*i;
	for(j = 0; j < BL; j++){
		diff = strchr(basechars, c1[j]);
		n1 += (unsigned long long)(diff - basechars);
		n1 *= BASE;
	}
	n1 /= BASE;
	//if(check(n1) == -1){
	//	exit(1);
	//}
	printf("good, %llx\n",n1);
	//n2 = *(unsigned long long*)(fhalf+8);
	//n2 = ~n2;

	//n3 = *(unsigned long long*)shalf;
	//n3 = -n3;
	//n3 += 0x1337;
	//
	//n4 = *(unsigned long long*)(shalf+8);
	//n4 ^= 0x1234567890abcdefl;
	//n4 -= 0x4242;
	
	//if (strcmp(c1, "artomtf2srn00tgm2f") || strcmp(c2, "ng0fa0mat0tmmmra0c") ||
    //    strcmp(c3, "ngnrmcornttnsmgcgr") || strcmp(c4, "a0fn2rfa00tcgctaot")) {
	//	printf("fuck");
	//	exit(1);
	//}

	return 0;
}
