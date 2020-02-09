# KiDPwN 
437pt ?solves(?/?)

## TLDR
* Set $rsp to higher address 
	* use misusing movsx operation
* Overwrite the return address from main() to rop gadget in libc
	* bruteforce attack against 4bits
* Leak the binary address and the libc address
* Overwrite got\_printf to one\_gadget
	* format string attack

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
* PIE    : Enable

### Exploit 
The binary has vulnerability of format string attack(0x97a) and misuses movsx operation(0x905).

```
905:   48 0f bf 45 fe          movsx  rax,WORD PTR [rbp-0x2]
90a:   48 8d 50 0f             lea    rdx,[rax+0xf]
90e:   b8 10 00 00 00          mov    eax,0x10
913:   48 83 e8 01             sub    rax,0x1
917:   48 01 d0                add    rax,rdx
91a:   b9 10 00 00 00          mov    ecx,0x10
91f:   ba 00 00 00 00          mov    edx,0x0
924:   48 f7 f1                div    rcx
927:   48 6b c0 10             imul   rax,rax,0x10
92b:   48 29 c4                sub    rsp,rax
92e:   48 89 e0                mov    rax,rsp
931:   48 83 c0 0f             add    rax,0xf
935:   48 c1 e8 04             shr    rax,0x4
939:   48 c1 e0 04             shl    rax,0x4
93d:   48 89 c2                mov    rdx,rax
940:   48 8d 05 19 07 20 00    lea    rax,[rip+0x200719]        # 201060 <__cxa_finalize@plt+0x200920>
947:   48 89 10                mov    QWORD PTR [rax],rdx
94a:   0f b7 45 fe             movzx  eax,WORD PTR [rbp-0x2]
94e:   0f b7 d0                movzx  edx,ax
951:   48 8d 05 08 07 20 00    lea    rax,[rip+0x200708]        # 201060 <__cxa_finalize@plt+0x200920>
958:   48 8b 00                mov    rax,QWORD PTR [rax]
95b:   48 89 c6                mov    rsi,rax
95e:   bf 00 00 00 00          mov    edi,0x0
963:   e8 a8 fd ff ff          call   710 <read@plt>
968:   48 8d 05 f1 06 20 00    lea    rax,[rip+0x2006f1]        # 201060 <__cxa_finalize@plt+0x200920>
96f:   48 8b 00                mov    rax,QWORD PTR [rax]
972:   48 89 c7                mov    rdi,rax
975:   b8 00 00 00 00          mov    eax,0x0
97a:   e8 81 fd ff ff          call   700 <printf@plt>
```
Normally, rsp register is set to lower address to store user input (at 0x92b), which of length is defined by user at fgets (0x8d9).
But, for example, if the length of user input is 65424(0xff90), rsp is set to higher address.
So we can change rsp to arbitary address and overwrite the return address from main().

However it is difficult to set rip to the ideal address, because PIE is enbale.
I found the usable address on stack at rbp+0x18. It is main() address.
So I wanted to change the return address to rop gadget (3 pop and ret)
By default, the return address from main() is an address in libc\_start\_main.
In distributed libc.so, offset of libc\_start\_main\_ret is 0x20830.
I searched rop gadget in libc, which of offset is near 0x20830. 
And I found it(at 0x202e3).

Using this gadget, I overwrote lower 2bytes of the return address.
So we have to do bruteforce attack against 4bits.

The following memory dump is captured on my local enviroment using libc-2.27.so.
So the address of libc\_start\_main\_ret is different from contest server's one.

In the dump:
binary base = 0x555555554000  
rbp = 0x7fffffffe370  
return address from main() = 0x7ffff7a05b97  
main() address = 0x555555554880  

```
0x7fffffffe360: 0x00007fffffffe450      0xff90000000000000
0x7fffffffe370: 0x00005555555549e0      0x00007ffff7a05b97
0x7fffffffe380: 0x0000000000000001      0x00007fffffffe458
0x7fffffffe390: 0x0000000100008000      0x0000555555554880
0x7fffffffe3a0: 0x0000000000000000      0x944fb65297d91336
0x7fffffffe3b0: 0x0000555555554750      0x00007fffffffe450
0x7fffffffe3c0: 0x0000000000000000      0x0000000000000000
0x7fffffffe3d0: 0xc11ae307c3191336      0xc11af3b8b2871336
0x7fffffffe3e0: 0x00007fff00000000      0x0000000000000000
0x7fffffffe3f0: 0x0000000000000000      0x00007ffff7de5733
```

Using this trick, I set rsp to $rbp-0x10.
And leaked the binary base address and the libc base address.

After [3 pop; ret] gadget, I overwrite got\_printf to one\_gadget by format string attack.

