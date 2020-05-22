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

char basechars[BASE + 1] = "angstromctf20";
char hash[SHA256_DIGEST_LENGTH] = "\xaa\x15\xa7\xb1\x91\xff\xa9\x43\xfa\x60\x2f\x74\x72\xef\x29\x4c\x6b\x5d\x13\x8a\x62\x9a\xc2\xbb\x75\xcb\x6a\xc5\x7b\xfc\x32\x57";

void tobase(unsigned long long n, char *ret) {
    ret[BL] = 0;
    for (int i = BL - 1; i >= 0; --i) {
        ret[i] = basechars[n % BASE];
        n /= BASE;
    }
}


int main(int argc, char *argv[])
{
	char flag[33];
	char fhalf[17];
	char shalf[17];
	
	char c1[BL + 1];
    char c2[BL + 1];
    char c3[BL + 1];
    char c4[BL + 1];
    
	int i;
	unsigned long long n1, n2, n3, n4;
	
	read(0, flag, 32);
	flag[32] = 0;
	for (i = 0; i < 32; i++){
		if (i % 2) shalf[i/2] = flag[i];
		else fhalf[i/2] = flag[i];
	}
	n1 = *(unsigned long long*)fhalf;
	n2 = *(unsigned long long*)(fhalf+8);
	n2 = ~n2;
	
	n3 = *(unsigned long long*)shalf;
	n3 = -n3;
	n3 += 0x1337;
	
	n4 = *(unsigned long long*)(shalf+8);
	n4 ^= 0x1234567890abcdefl;
	n4 -= 0x4242;
	
	tobase(n1, c1);
	tobase(n2, c2);
	tobase(n3, c3);
	tobase(n4, c4);
	
	if (strcmp(c1, "artomtf2srn00tgm2f") || strcmp(c2, "ng0fa0mat0tmmmra0c") ||
        strcmp(c3, "ngnrmcornttnsmgcgr") || strcmp(c4, "a0fn2rfa00tcgctaot")) {
		printf("fuck");
		exit(1);
	}

	unsigned char digest[SHA256_DIGEST_LENGTH];

	SHA256_CTX sha_ctx;
	SHA256_Init(&sha_ctx);
	SHA256_Update(&sha_ctx, flag, 32); 
	SHA256_Final(digest, &sha_ctx); 
	
	if (strcmp(hash, digest)){
		printf("fuck");
		exit(1);
	}
	
	printf("%s\n", flag);

	//for (int i = 0; i < sizeof(digest); ++i) {
	//		printf("%x", digest[i]);
	//}
	//printf("\n");

	return 0;
}
