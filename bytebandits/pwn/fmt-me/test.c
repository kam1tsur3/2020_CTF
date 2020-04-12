#include <stdio.h>
#include <stdlib.h>

char buf[0x200] = {0};

void main()
{
	char t[0x100] = {0};
	fgets(t, 0x100, stdin);
	snprintf(buf, 0x10, t);
	puts(buf);
}
