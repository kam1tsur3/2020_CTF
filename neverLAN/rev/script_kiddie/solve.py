f = open("encrypted_db")

for l in f:
	for i in range(0,len(l)-1,2):
		c = l[i]+l[i+1]
		c = int(c,16)
		print(chr(c),end="")
