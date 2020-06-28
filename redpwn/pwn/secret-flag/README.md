# secret-flag 

## TLDR
* FSB
	* Read flag string on stack

## Challenge
### Description
result of file command
* Arch    : x86-64
* Library : Dynamically linked
* Symbol  : Stripped

result of checksec
* RELRO  : Full RELRO
* Canary : Enable 
* NX     : Enable
* PIE    : Enable

### Exploit 
There is a format string bug in the binary.  
\"flag.txt\" is opened and read into the chunk which allocated before.  
And the address of the chunk is stored on the stack.  
So we can read flag strings using a format string like "%X$s".  

My exploit code is [solve.py](https://github.com/kam1tsur3/2020_CTF/blob/master/redpwn/pwn/secret-flag/solve.py).

## Reference

twitter: @kam1tsur3
