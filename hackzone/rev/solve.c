#include <stdio.h>

int flag[0x12] = {3, 1, 9, 1, 3, 3, 2, 2, 
			  0, 5, 4, 2, 2, 0, 6, 5, 1};
long long num[2] = {0x665d30696f643032, 0x68656332705f5a7a};
void main()
{
	int i;
	for(i = 0; i < 0x12; i++){
		printf("%c", (char)(flag[i]+((char *)num)[i]));
	}
}
