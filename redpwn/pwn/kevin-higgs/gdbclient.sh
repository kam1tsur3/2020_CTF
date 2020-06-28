gdb -ex 'target remote localhost:8888' -ex 'b *0x8049448' -ex 'set environment NUMBER_OF_FLIPS=2'
