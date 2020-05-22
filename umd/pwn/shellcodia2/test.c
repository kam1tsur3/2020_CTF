#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>
#include <unistd.h>

void main()
{
	int fd;
	fd = open("test.txt", O_WRONLY);
	write(fd, "testdayo", 8);
}
