# Dark Honya 
460pt ?solves

## TLDR
* Poison null byte
* Unsafe unlink
* Leak libc address
	* Overwrite got\_free to plt\_puts
* Overwrite got\_free to system() address in libc

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

libc version: 2.23
### Exploit 
All address of allocated chunks is stored in table at bss area.
The table can have 16 entries and is located at fixed address 0x6021a0.
We can select command below:
* 1:buy a book
	* malloc(0xf8)
	* write in chunk
		* there is a vulnerability of poison null byte
* 2:put a book
	* free(table\[index\])
	* set table\[index\] to 0
		* prevent from UAF
* 3:write in a book
	* write in chunk
		* there is a vulnerability of poison null byte
* 4:read a book
	* not implemented
* 5:checkout
	* exit

There is a vulnerability of poison null byte when writing in chunk.
I made a fake chunk and used unsafe unlink attack.
Despite we don't have read command, we can know libc address by overwriting got\_free to plt\_puts.

My exploitcode is [solve.py](https://github.com/kam1tsur3/2020_CTF/blob/master/nullcon/pwn/Dark_Honya/solve.py).

When overwriting got\_free, I met some strange crash.
I have no confidence for the reason of crash, but I think this is caused by some alignment restriction.
So I avoided this crash by making overwritten address got\_free-0x8 and writing 0xf bytes(not 0x10 bytes).

## Reference
https://github.com/shellphish/how2heap/blob/master/glibc_2.26/unsafe_unlink.c

Twitter@kam1tsur3
