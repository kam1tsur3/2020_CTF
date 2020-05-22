#include <stdio.h>

char flag[100] = "PH?>OA(vN/io/Zb<q.Zt+pZKm.io0x";
void main()
{
	int i;
	for(i = 0; flag[i] != 0; i++){
		printf("%c", flag[i]+5);
	}
	puts("");
}
