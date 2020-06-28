# tetanus 

## TLDR
* binary written by rust
* UAF
	* tcache poisoning
	* overwrite the value of free\_hook to one gadget rce

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

libc version: 2.30 (in given dockerfile)

I have solved the rust binary for the first time.  I'm glad to solve this.

### Exploit 
In main function, "lists" is declared, which type is "Vec<VecDeque<i64>>".   

We can choose 7 commands, which is
#### 1.create a list
* Example: 
After creating a list with size=8

```
0x55555578aec0: 0x0000000000000000      0x0000000000000091 <-- chunk of lists
0x55555578aed0: 0x0000000000000000      0x0000000000000000
0x55555578aee0: 0x000055555578ae40      0x0000000000000010 <--- added
0x55555578aef0: 0x0000000000000000      0x0000000000000000
0x55555578af00: 0x0000000000000000      0x0000000000000000
0x55555578af10: 0x0000000000000000      0x0000000000000000
0x55555578af20: 0x0000000000000000      0x0000000000000000
0x55555578af30: 0x0000000000000000      0x0000000000000000
0x55555578af40: 0x0000000000000000      0x0000000000000000
.
.
.
0x55555578ae30: 0x0000000000000000      0x0000000000000091
0x55555578ae40: 0x0000000000000000      0x0000000000000000 
0x55555578ae50: 0x0000000000000000      0x0000000000000000
0x55555578ae60: 0x0000000000000000      0x0000000000000000
0x55555578ae70: 0x0000000000000000      0x0000000000000000
0x55555578ae80: 0x0000000000000000      0x0000000000000000
0x55555578ae90: 0x0000000000000000      0x0000000000000000
0x55555578aea0: 0x0000000000000000      0x0000000000000000
0x55555578aeb0: 0x0000000000000000      0x0000000000000000
```

After creating a list again with size=4   

```
0x55555578aec0: 0x0000000000000000      0x0000000000000091
0x55555578aed0: 0x0000000000000000      0x0000000000000000
0x55555578aee0: 0x000055555578ae40      0x0000000000000010
0x55555578aef0: 0x0000000000000000      0x0000000000000000
0x55555578af00: 0x000055555578af60      0x0000000000000008 <--- added
0x55555578af10: 0x0000000000000000      0x0000000000000000
0x55555578af20: 0x0000000000000000      0x0000000000000000
0x55555578af30: 0x0000000000000000      0x0000000000000000
0x55555578af40: 0x0000000000000000      0x0000000000000000
.
.
.
0x55555578af50: 0x0000000000000000      0x0000000000000051
0x55555578af60: 0x0000000000000000      0x0000000000000000
0x55555578af70: 0x0000000000000000      0x0000000000000000
0x55555578af80: 0x0000000000000000      0x0000000000000000
0x55555578af90: 0x0000000000000000      0x0000000000000000
```

#### 2.delete a list
* free allocated chunk
* chunk ptr is not cleared(vulnerable) 

#### 3. edit a list
* it should be used after 5.append command giving index of lists, index of elements
* use after free

#### 4. prepend to list (I didn't use this)
#### 5. append to list
* Example
After append to list with index=0, number of elements=4, element=\[9,10,100,101\].

```
0x55555578aec0: 0x0000000000000000      0x0000000000000091
0x55555578aed0: 0x0000000000000000      0x0000000000000004 <-- incremented 4 times
0x55555578aee0: 0x000055555578ae40      0x0000000000000010
0x55555578aef0: 0x0000000000000000      0x0000000000000000
0x55555578af00: 0x000055555578af60      0x0000000000000008
.
.
.
0x55555578ae30: 0x0000000000000000      0x0000000000000091
0x55555578ae40: 0x0000000000000009      0x000000000000000a <-- added
0x55555578ae50: 0x0000000000000064      0x0000000000000065 <-- added
0x55555578ae60: 0x0000000000000000      0x0000000000000000
0x55555578ae70: 0x0000000000000000      0x0000000000000000
0x55555578ae80: 0x0000000000000000      0x0000000000000000
0x55555578ae90: 0x0000000000000000      0x0000000000000000
0x55555578aea0: 0x0000000000000000      0x0000000000000000
0x55555578aeb0: 0x0000000000000000      0x0000000000000000
```

#### 6. view an element
* use after free

#### 7. exit
* call exit()

My exploit flow is shown below.

1. Add lists with size=8 (chunk size = 0x90) and append elements each 8times. 
(we append elements to prevent from error when use after free)
2. Delete lists with index from 0 to 7.
Last chunk is connected to unsorted bin.
3. Show a list connected to unsorted bin. We can get the address of libc.
4. Edit a list connected to tcache and make tcache point to the address of free\_hook.
5. Add lists with size=8 2times to get a chunk which is placed in free\_hook.
6. Append 2 elements which is composed of [libc_system, u64( "/bin/sh")].
All input is buffered in this binary. So after appending these elements, free("/bin/sh") is called which means system("/bin/sh").


My exploit code is [solve.py](https://github.com/kam1tsur3/2020_CTF/blob/master/redpwn/pwn/tetanus/solver/solve.py).

## Reference

twitter: @kam1tsur3
