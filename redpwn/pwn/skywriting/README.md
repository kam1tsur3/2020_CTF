# skywriting 

## TLDR
* BOF 
	* canary leak
	* libc leak
	* one gadget rce

## Challenge
### Description
result of file command
* Arch    : x86-64
* Library : Dynamically linked
* Symbol  : Stripped

result of checksec
* RELRO  : Partial RELRO
* Canary : Disable
* NX     : Enable
* PIE    : Disable

libc version: 2.27 (in given dockerfile)
### Exploit 
The binary reads user's input repeatedly until the string \"notflag{a_cloud_is_just_someone_elses_computer}\" is read, and writes user input by printf("%s", user\_input).  
And there is a vulnerability of buffer overflow.

Exploit flow is shown below.  
1. Leak canary
2. Leak the address of libc which is return address from main func.  
3. Input payload which begins the string \"notflag{a_cloud_is_just_someone_elses_computer}\" and is padded with the leaked canary and one gadget rce.

My exploit code is [solve.py](https://github.com/kam1tsur3/2020_CTF/blob/master/redpwn/pwn/skywriting/solver/solve.py).

## Reference

twitter: @kam1tsur3
