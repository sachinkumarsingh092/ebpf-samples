compile:
	clang -I/usr/include/x86_64-linux-gnu -O2 -g -Wall -target bpf -c xdp_drop.c -o xdp_drop.o

load:
	sudo ip link set lo xdpgeneric obj xdp_drop.o sec tcp_drop

unload:
	sudo ip link set lo xdpgeneric off

status:
	sudo ./xdp-tools/xdp-loader/xdp-loader status
