#include <stdio.h>
#include <stdlib.h>
int key(unsigned int seed)
{
	asm volatile(
		".intel_syntax noprefix;\n\t"
		"mov	%eax,%edi;\n\t"
		"movsxd %rdx,%eax;\n\t"
		"imul   %rdx,%rdx,0x14f8b589;\n\t"
		"shr    %rdx,0x20;\n\t"
		"mov    %ecx,%edx;\n\t"
		"sar    %ecx,0xd;\n\t"
		"cdq    ;\n\t"
		"sub    %ecx,%edx;\n\t"
		"mov    %edx,%ecx;\n\t"
		"imul   %edx,%edx,0x186a0;\n\t"
		"sub    %eax,%edx;\n\t"
		"mov    %edx,%eax;\n\t"
		"lea    %eax,[rdx+0x1];\n\t"
		".att_syntax;\n\t"
	);
}
int main()
{
	unsigned int r;
	srand(0);
	for(int i = 0; i <= 0x63; i++){
		r = rand();
		r = key(r);
		printf("%d\n", r);
	}
}
