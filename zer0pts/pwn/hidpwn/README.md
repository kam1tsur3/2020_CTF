# hipwn 
158pt ?solves

## TLDR
* BOF 
	* this binary uses gets() 
* ROP chain
	* call read and execve system call 

## Challenge
We can get the executable binary file and C source code.

### Description
result of file command
* Arch    : x86-64
* Library : Statically linked
* Symbol  : Stripped

result of checksec
* RELRO  : Partial RELRO
* Canary : Disable
* NX     : Enable
* PIE    : Disable

### Exploit 
The source code is so simple.
```c:main.c
#include <stdio.h>

int main(void) {
  char name[0x100];
  puts("What's your team name?");
  gets(name);
  printf("Hi, %s. Welcome to zer0pts CTF 2020!\n", name);
  return 0;
}
```

In this binary, there is a vulnerability of buffer overflow by gets function.
So we can use ROP chain attack that calls read and execve system call.

I use strace with option i in order to know how long input trigger BOF, and use rp++ to search rop gadgets.

```
vagrant@ubuntu-bionic:~/workspace/2020/zer0pts/pwn/hidpwn$ perl -e 'print "A"x264 . "BCDE"' | strace -i ./chall
[00007ff4c18d1e37] execve("./chall", ["./chall"], 0x7ffebf8c4788 /* 23 vars */) = 0
[0000000000402a74] arch_prctl(ARCH_SET_FS, 0x604af8) = 0
[0000000000402035] set_tid_address(0x604d10) = 11498
[000000000040265c] ioctl(1, TIOCGWINSZ, {ws_row=51, ws_col=178, ws_xpixel=0, ws_ypixel=0}) = 0
[0000000000402cac] writev(1, [{iov_base="What's your team name?", iov_len=22}, {iov_base="\n", iov_len=1}], 2What's your team name?
) = 23
[00000000004025bf] read(0, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"..., 1024) = 268
[00000000004025bf] read(0, "", 1024)    = 0
[0000000000402cac] writev(1, [{iov_base="Hi, AAAAAAAAAAAAAAAAAAAAAAAAAAAA"..., iov_len=272}, {iov_base=". Welcome to zer0pts CTF 2020!\n", iov_len=31}], 2Hi, AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABCDE. Welcome to zer0pts CTF 2020!
) = 303
[0000000045444342] --- SIGSEGV {si_signo=SIGSEGV, si_code=SEGV_MAPERR, si_addr=0x45444342} ---
[????????????????] +++ killed by SIGSEGV (core dumped) +++
Segmentation fault (core dumped)
```

My exploit code is [solve.py](https://github.com/kam1tsur3/2020_CTF/blob/master/zer0pts/pwn/hidpwn/solve.py).
