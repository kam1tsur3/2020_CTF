# write 
?pt ?solves

## TLDR
* overwrite function pointer in libc 
	* \_\_rtld\_lock\_lock\_recursive 

## Challenge
### Description
result of file command
* Arch    : x86-64
* Library : Dynamically linked
* Symbol  : Not stripped

result of checksec
* RELRO  : Full RELRO
* Canary : Disable
* NX     : Enable
* PIE    : Enable

libc version: 2.27 (distributed with binary)
### Exploit 
In this binary, we can overwrite arbitary address to arbitary value repeatedlly.
Furthermore, we are given the address of puts in libc and stack pointer(rbp-0x18 in main).
But PIE and Full RELRO is enable, so we don't know any address in binary and we can't overwrite the global offset table.
And execution flow is ended with exit() in main, so we can't make ROP chain.
What should I do??

I overwroted the pointer of \_\_rtld\_lock\_lock\_recursive in libc to one-gadget RCE.
I found that gadget by rp++ with option -l1(offset 0xe569f).
This gadget always sucesses in this enviroment (in \_\_rtld\_lock\_lock\_recursive).
(I heard this technique from @ptrYudai. Thanks:) )

So I overwrote memory only one time and got flag.

My exploit code is [solve.py](https://github.com/kam1tsur3/2020_CTF/blob/master/bytebandits/pwn/write/solve.py).

## Reference
https://code.woboq.org/userspace/glibc/elf/dl-fini.c.html#53
