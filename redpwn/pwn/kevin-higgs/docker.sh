docker run -v ${PWD}:/ctf --cap-add=SYS_PTRACE --rm --name redpwnctf-kevin-higgs -itp 1337:9999 $(docker build -q .)
