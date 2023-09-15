#!/usr/bin/python3

from bcc import BPF
import ctypes as ct

program = """

#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/tcp.h>
#include <linux/sched.h>

BPF_HASH(pid_filter, u32, char);

int block_port(struct xdp_md *ctx) {
    // Get the packet data and the end of the packet data
    void *data = (void *)(long)ctx->data;
    void *data_end = (void *)(long)ctx->data_end;

    // Get the ethernet header, IP header, and TCP header
    struct iphdr *ip = data + sizeof(struct ethhdr);
    struct tcphdr *tcph = data + sizeof(struct ethhdr) + sizeof(struct iphdr);

    u32 pid = bpf_get_current_pid_tgid();
    char comm[TASK_COMM_LEN];

    bpf_get_current_comm(&comm, sizeof(comm));

    bpf_trace_printk("Debug message: variable = %d\\n", comm);

    if (tcph->dest != 4040) {
        // Drop traffic for other ports
        if (pid_filter.lookup(&pid) && !strcmp(comm, "myprocess")) {
            return XDP_DROP;
        }
    }

    return XDP_PASS;
}
"""


b = BPF(text=program)

fn = b.load_func("block_port", BPF.XDP)

pid_filter = b.get_table("pid_filter")
pid = 5878
key = ct.c_uint(pid)
value = ct.c_ulong(pid)
pid_filter[pid] = value

# Attach the program to a network interface (e.g., eth0, lo, veth1)
b.attach_xdp(dev="lo", fn=fn)