Problem Statement: Write an eBPF code to drop the TCP packets on a port (def: 4040). Additionally, if you can make the port number configurable from the userspace, that will be a big plus.

Solution:
As I'm pretty new to eBPF space, I learned a lot while solving this problem. I'll try to explain the solution in detail.
This directory has 2 files: `xdp_drop.c` and `xdp_drop_config_port.py`. The former is the eBPF code and the latter is the userspace code.
The first part of the problem is in the C code while the second part is in the python code.
I made a Makefile to compile and load the eBPF module. The Makefile also has a target to unload the module.

To test the solution I used `netcat`. I ran `nc -l 8080` on one terminal and `nc localhost 8080` on another terminal. I sent some data from the second terminal to the first one and it was dropped as expected.
To test it for yourself, simply do a `make compile` followed by a `make load` and then run the `nc` commands as mentioned above.

The python code does this all. Just change desired port nummber in the `configurable_port` variable. To test it simple do a `sudo ./xdp_drop_config_port.py` and then run the `nc` commands as mentioned above.

References:
https://codilime.com/blog/how-to-drop-a-packet-in-linux-in-more-ways-than-one/
https://www.tigera.io/learn/guides/ebpf/ebpf-xdp/
https://github.com/iovisor/bcc/blob/master/docs/reference_guide.md#2-bpf_hash
...
and a lots of googling.
