from pwn import *
import sys

#config
context(os='linux', arch='i386')
context.log_level = 'debug'

HOST = "pwn.byteband.it"
PORT = 6000 


def exploit():
	conn = remote(HOST, PORT)
	count = 0
	while True:	
		l1 = ""
		encode = "encode" + str(count)
		decode = "decode" + str(count)
		while len(l1) < 8173:
			l = conn.recv()
			l1 += l
		f = open(encode, mode="w")
		print(len(l1))
		f.write(l1)
		f.close()
			
		os.system("base64 -d " + encode +" > " + decode)
		pro = process(["./solver", decode])
		a = pro.recvline()
		conn.send(a)
		pro.close()
		#os.system("rm " + encode + " " +decode)
		count += 1
	conn.interactive()	
	print count

if __name__ == "__main__":
	exploit()	
