BINARY=$1
socat tcp-l:7777,reuseaddr,fork "system:gdbserver localhost\\:8888 $1 $2"
