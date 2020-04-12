#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

char key[31] = {0}; 
char flag[0x30] = {0};

void main(int argc, char** argv)
{
	int fd, i;
	char tmp[10];
	char len;
	fd = open(argv[1], O_RDONLY);
	lseek(fd, 0x95a, 0);
	read(fd, &len, 1);

	lseek(fd, 0xaa8, 0);
	read(fd, key, 30);
	lseek(fd, 0x7fa, 0);
	for(i = 0; i < len; i++){
		if(i < 0x17){
			read(fd, tmp, 10);
			flag[i] = key[tmp[0]];
		} else {
			read(fd, tmp, 7);
			flag[i] = key[tmp[0]];
		}
		//printf("%x, ", (int)(tmp[0]));
	}
	//puts("");
	//printf("key:%s\n", key);	
	//printf("flag:%s\n", flag);
	printf("%s\n", flag);
	
}
