# coffer-overflow-2 

## TLDR
* BOF 

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

### Exploit 
Simple buffer overflow challenge.  
Return to function named \"binFunction\".  

My exploit code is [solve.py](https://github.com/kam1tsur3/2020_CTF/blob/master/redpwn/pwn/coffer-overflow-2/solve.py).

## Reference

twitter: @kam1tsur3
