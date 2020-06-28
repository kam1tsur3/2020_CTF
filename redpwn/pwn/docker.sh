tar xf dead-canary.tar.gz && echo fake_flag > bin/flag.txt && docker run -v ${PWD}:/ctf --cap-add=SYS_PTRACE --rm --name redpwnctf-dead-canary -itp 1337:9999 $(docker build -q .)
