import gdb

gdb.execute("b *0x40080b")
gdb.execute("b *0x40082b")
gdb.execute("b *0x400845")

flag = ""
gdb.execute("r AAAABBBBAAAABBBBAAAABBBB")

for i in range(0, 0x18):
	al = gdb.execute("p $al", to_string=True).split("= ")[1]	
	flag += chr(int(al, 16))
	gdb.execute("set $bl="+al,to_string=True)
	gdb.execute("c")
print(flag)
