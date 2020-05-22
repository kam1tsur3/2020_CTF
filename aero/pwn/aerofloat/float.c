#include <stdio.h>
#include <stdlib.h>

void main()
{
	//unsigned long num;
	//scanf("%lx", &num);
	// printf("(int)  : %ld\n", num);
	// printf("(hex)  : %lx\n", num);
	// printf("(p)  : %p\n", num);
	// printf("(float): %lf\n", *((float *)&num));

	// unsigned long num;
	// scanf("%lx", &num);
	
	double num;
	scanf("%lf", &num);
	
	printf("(int)  : %ld\n", *(unsigned long*)&num);
	printf("(hex)  : %lx\n", *(unsigned long*)&num);
	printf("(double)  : %100.1400lf\n", *(double*)&num);
	return;
}
