#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

void reverse(char *c)
{
	int i;
	char tmp = 0;
	for(i = 0; i < 8; i++){
		if(*c & (1 << i))
			tmp |= (1 << (7-i));
	}
	*c = tmp;
	return;
}

void main()
{
	int fd, i;
	char flag[0x2c] = {0};
	
	fd = open("./missyelliott", O_RDONLY);
	lseek(fd, 0x2008, 0);	
	for(i = 0; i < 0x2b; i++){
		read(fd, &flag[0x2a-i], 1);		
	}
	// decode
	for(i = 0; i < 0x2b; i++){
		reverse(&flag[i]);
		flag[i] = ~flag[i];
	}
	printf("%s\n", flag);
	return;
}
