# four-function-heap 

## TLDR
* tcache double free
	* overwrite tcache\_perthread\_struct
	* overwrite the value of free\_hook to one gadget rce
* UAF 
	* leak heap address
	* leak libc address

## Challenge
### Description
result of file command
* Arch    : x86-64
* Library : Dynamically linked
* Symbol  : Stripped

result of checksec
* RELRO  : FullRELRO
* Canary : Enable
* NX     : Enable
* PIE    : Enable

libc version: 2.27 (in given dockerfile)
### Exploit 
In this binary, We can choose 3 commands,  
1. alloc
	* giving three parameters, index, size and data
	* call malloc() and read() into allocated chunk
2. free
	* free allocated chunk
	* freed ptr is not cleared (use after free)
3. show
	* print the value of allocated chunk

We can do these commands only 15 times.  
It makes this challenge more difficult.  

My exploit flow is shown below.  
1. Trigger tcache double free and show heap base.
2. Get a chunk which is overlapped tcache\_perthred\_sturut by using tcache poisoning.
3. Overwrite array count[] in tcache\_perthred\_sturut in order to next freed chunk is connected unsorted bin.
4. Leak libc address by show command
5. Get a chunk which is overlapped free\_hook and overwrite free\_hook to one gadget rce.

My exploit code is [solve.py](https://github.com/kam1tsur3/2020_CTF/blob/master/redpwn/pwn/four-function-heap/solver/solve.py).

## Reference

twitter: @kam1tsur3
