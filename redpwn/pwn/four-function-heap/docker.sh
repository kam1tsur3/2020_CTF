tar xf four-function-heap.tar.gz && echo fake_flag > bin/flag.txt && docker run -v ${PWD}:/ctf --cap-add=SYS_PTRACE --rm --name redpwnctf-four-function-heap -itp 1337:9999 $(docker build -q .)
