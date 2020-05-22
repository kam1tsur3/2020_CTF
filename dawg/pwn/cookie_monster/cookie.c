#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void main()
{
	unsigned int now;
	now = time(0);
	srand(now+1);
	printf("0x%llx\n", rand());
	return;
}
