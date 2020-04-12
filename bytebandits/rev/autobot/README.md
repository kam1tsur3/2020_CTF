# autobot
?pt ?solves

## Challenge
Any files were distributed.  
We were informed the server address and the port number only.

Connect to server, text encrypted with base64 is send.  
After decoding, we know that text is an ELF binary.  
This binary is a simple crackme challenge.  
But some parameters of correct string (length, encrypt key, origin string) are different everytime.  
And to get the flag, we have to solve this crackme challenge dynamically and countinuously 300times.   
### Solution
I wrote that some parameteres is variable, but execution flow, the address of these parameters and the size of binary is fixed.  
So we can write the dynamical solver based these addresses of parameters.

That dynamical solver is [solve.c](https://github.com/kam1tsur3/2020_CTF/blob/master/bytebandits/rev/autobot/solve.c) and commiled being named [solver](https://github.com/kam1tsur3/2020_CTF/blob/master/bytebandits/rev/autobot/solver).  
This is called from [net.py](https://github.com/kam1tsur3/2020_CTF/blob/master/bytebandits/rev/autobot/net.py).

## Reference
