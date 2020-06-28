# the-library 

## TLDR
* BOF
* ROP
	* leak the address of libc 
	* return to one gadget rce

## Challenge
### Description
result of file command
* Arch    : x86-64
* Library : Dynamically linked
* Symbol  : Not stripped

result of checksec
* RELRO  : Partial RELRO
* Canary : Disable
* NX     : Enable
* PIE    : Disable

libc version: 2.27
### Exploit 
There is a vulnerability of buffer overflow.  
I made ROP chain by which I leaked the address of libc and returned to main func.  
At the seccond time of main routine, I triggered BOF again and returned to one gagdet rce.  

My exploit code is [solve.py](https://github.com/kam1tsur3/2020_CTF/blob/master/redpwn/pwn/the-library/solve.py).

## Reference

twitter: @kam1tsur3
