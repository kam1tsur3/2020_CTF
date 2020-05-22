#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>

void main()
{
	char buf[100];
	int fd, i;
	fd = open("chall2.elf", O_RDONLY);
	lseek(fd, 0x2030, 0);
	read(fd, buf, 0x25);
	for(i = 0; i < 0x25; i++){
		printf("%c", buf[i]^0x55);
	}
	puts("");
	return;
}
