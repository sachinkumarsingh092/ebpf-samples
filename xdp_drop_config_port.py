#!/usr/bin/python3

from bcc import BPF
import ctypes as ct

# Define BPF program
program = """

#include <linux/if_ether.h>
#include <linux/if_packet.h>
#include <linux/in.h>
#include <linux/ip.h>
#include <linux/tcp.h>

// Total size of the packet
#define TOTSZ (sizeof(struct ethhdr) + sizeof(struct iphdr) + sizeof(struct tcphdr))

BPF_HASH(drop_port, u16, u64, 1);
int drop_tcp_port(struct xdp_md *ctx) {
    // Get the packet data and the end of the packet data
    void *data = (void *)(long)ctx->data;
    void *data_end = (void *)(long)ctx->data_end;
    

    // Get the ethernet header, IP header, and TCP header
    struct iphdr *ip = data + sizeof(struct ethhdr);
    struct tcphdr *tcph = data + sizeof(struct ethhdr) + sizeof(struct iphdr);
    
    // Check if the packet is large enough
    if (data + TOTSZ > data_end) {
        return XDP_PASS;
    }

    // Get the destination port from the packet
    u16 dest_port = ntohs(tcph->dest);

    // Get the configurable port from the userspace
    u64 *config_port = drop_port.lookup(&dest_port);

    // Drop the packet if the destination port matches the configurable port
    if (config_port) {
        if (ip->protocol == IPPROTO_TCP && tcph->dest == htons(*config_port)) {
            return XDP_DROP;
        }
    }

    return XDP_PASS;
}
"""

b = BPF(text=program)

fn = b.load_func("drop_tcp_port", BPF.XDP)

# Define the configurable port (e.g., 8080)
configurable_port = 8080

# Update the drop_port map with the configurable port
drop_port_map = b.get_table("drop_port")
key = ct.c_ushort(configurable_port)
value = ct.c_ulong(configurable_port)
drop_port_map[key] = value

# Attach the program to a network interface (e.g., eth0, lo, veth1)
b.attach_xdp(dev="lo", fn=fn)