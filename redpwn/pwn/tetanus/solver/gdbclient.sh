gdb -ex 'target remote localhost:8888' -ex 'b *0x55555555f749' -ex 'set print asm-demangle' -ex 'b *0x55555555f8c1' -ex 'b *0x55555557a40'
