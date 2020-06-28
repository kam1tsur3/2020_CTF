# dead-canary 

## TLDR
* FSB
	* leak the address of libc
	* GOT overwrite
* BOF
	* to call \_\_stack\_chk\_fail

## Challenge
### Description
result of file command
* Arch    : x86-64
* Library : Dynamically linked
* Symbol  : Stripped

result of checksec
* RELRO  : Partial RELRO
* Canary : Enable 
* NX     : Enable
* PIE    : Disable

libc version: 2.27 (in given dockerfile)
### Exploit 
There are vulnerabilities of buffer over flow and format string bug.  

I took a 3step to exploit.  

1. Send a payload which overwrites the value of got\_stack\_chk\_fail to the address of main ,triggeres buffer overflow and leaks the address of libc by fsb.
By sending this payload, you can return to main function if stack overflow has been occured.  
2. Overwrite the value of got\_write which is never called unless some errores happen to one gadget rce and trigger buffer overflow again.
We can jump to one gadget rce if write is called.
3. Overwrite the value of got\_stack\_fail to plt\_write and trigger buffer overflow again.
We can get shell.

My exploit code is [solve.py](https://github.com/kam1tsur3/2020_CTF/blob/master/redpwn/pwn/dead-canary/solver/solve.py).

## Reference

twitter: @kam1tsur3
