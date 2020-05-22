from pwn import *

context(os='linux', arch='i386')
context.log_level = 'debug'

conn = ssh(host='shell.actf.co', user='team5579', password='c5586f7c213649b0a4ea')
conn.set_working_directory('/problems/2020/taking_off')
pro = conn.process(['./taking_off','3', '9', '2' ,'chicken'])
#pro = conn.process('./taking_off', arg=['./taking_off','3', '9', '2' ,'chicken'],)


#import kmpwn
sys.path.append('/home/vagrant/kmpwn')
from kmpwn import *
#fsb(width, offset, data, padding, roop)

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

FILE_NAME = ""
HOST = ""
PORT = 0

#elf = ELF(FILE_NAME)
#libc = ELF('./')
#
#main_addr = elf.symbols["main"]
#libc_binsh = next(elf.search("/bin/sh"))
#addr_bss = elf.bss()
#addr_dynsym = elf.get_section_by_name('.dynsym').header['sh_addr']

def exploit():
	pro.sendline("please give flag")
	pro.interactive()

if __name__ == "__main__":
	exploit()	
