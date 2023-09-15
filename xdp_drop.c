#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/if_packet.h>
#include <linux/in.h>
#include <linux/ip.h>
#include <linux/tcp.h>

#define SEC(NAME) __attribute__((section(NAME), used))
#define htons(x) ((__be16)___constant_swab16((x)))
#define TOTSZ (sizeof(struct ethhdr) + sizeof(struct iphdr) + sizeof(struct tcphdr))

SEC("tcp_drop")
int drop_tcp_port(struct xdp_md *ctx) {
    int drop_port;
    void *data = (void *)(long)ctx->data;
    void *data_end = (void *)(long)ctx->data_end;
    
    struct iphdr *ip = data + sizeof(struct ethhdr);
    struct tcphdr *tcph = data + sizeof(struct ethhdr) + sizeof(struct iphdr);
    
    if (data + TOTSZ > data_end) {
        return XDP_PASS;
    }

    if (ip->protocol == IPPROTO_TCP && tcph->dest == htons(8080)) {
        return XDP_DROP;
    }
    
    return XDP_PASS;
}

char _license[] SEC("license") = "GPL";
