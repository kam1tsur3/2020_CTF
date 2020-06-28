tar xf skywriting.tar.gz && echo fake_flag > bin/flag.txt && docker run -v ${PWD}:/ctf --cap-add=SYS_PTRACE --rm --name redpwnctf-skywriting -itp 1337:9999 $(docker build -q .)
