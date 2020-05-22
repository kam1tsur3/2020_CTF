# Challengename
?pt ?solves

## TLDR
* Use after free 
	* something

## Challenge
### Description
result of file command
* Arch    : x86-64
* Library : Dynamically linked
* Symbol  : Not stripped

result of checksec
* RELRO  : Partial RELRO
* Canary : Enable
* NX     : Enable
* PIE    : Disable

libc version: 2.27 (distributed)  

This is some book collection service.  
The challenge binary has 4 commands.  
1. create
	* malloc for book's name
		* the size of chunk is optional
	* malloc for book's summary
		* the size of chunk is optional
	* calloc for book's entry 
		* the size of chunk is 0x20
		* the entry is stored in global pointer table
		* [chunk_ptr+0] stores the function pointer of display_summary
		* [chunk_ptr+0x8] stores the chunk address of name
		* [chunk_ptr+0x10] stores the chunk address of summary
2. delete
	* free a chunk in global pointer table with index
	* the entry is not deleted from table 
		* there is vulnerabirity of UAF
3. change
	* free a chunk of summary
	* malloc new chunk of summary
		* the size of chunk is optional
4. display
	* call the function stored in \[chunk\_ptr+0x10\] (defaultly display\_summary)
		* used for exploit to jump arbitary pointer 
### Exploit 
My exploit code is [solve.py](https://github.com/kam1tsur3/2020_CTF/blob/master/xxx/pwn/xxx/solve.py).

## Reference

twitter: @kam1tsur3
