# diylist 
453pt ?solves

## TLDR
* tcache double free 
* overwrite free hook 

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

libc version: 2.27 (not distributed)

### Exploit 
We can add the value which of type is long or double or string(char pointer) to the original list structure. 
And also, we can get, delete and edit the element of the list with given index and type.

There is some bugs in this binary.
One of that we can get the element with type distinct from added one.
So, if we add an element with type of string and get one with type of long, we can get the address of string which is located in heap area.
And we add an element with type of long and get one with type of string, we can get the value of arbitary located memroy.
I use this bug to leak the libc address. 

Used libc in this challenge is not distributed.
So I use libc.blukat.me to specify version of libc.

Another bug is in delete function.
Type of string is managed with another list (named fpool) to memory the address.
If we add an element which of type is string, the address of that is added to fpool.
But, if we delete an element which of type is string, no element is deleted from fpool.
I use this bug to trigger tcache double free.

My exploit code is [solve.py](https://github.com/kam1tsur3/2020_CTF/blob/master/zer0pts/pwn/diylist/solve.py).

## Reference
https://libc.blukat.me/
