#include <linux/kconfig.h>
#include <uapi/linux/bpf.h>
#include <bpf/bpf_helpers.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/tcp.h>

BPF_HASH(packet_count, u16);

int trace_packet_count(struct __sk_buff *skb) {
    // Parse packet
    u8 *cursor = 0;
    struct ethhdr *eth = cursor;
    cursor += sizeof(struct ethhdr);
    struct iphdr *ip = cursor;
    if (ip->protocol != IPPROTO_TCP)
        return 0;
    cursor += sizeof(struct iphdr);
    struct tcphdr *tcp = cursor;

    // Filter packets by source IP address
    u32 src_ip = ip->saddr;
    if (src_ip != "172.16.137.2")
        return 0;

    // Update packet count per port
    u16 dport = tcp->dest;
    u64 *count = packet_count.lookup(&dport);
    if (count) {
        (*count)++;
    } else {
        u64 initial_count = 1;
        packet_count.update(&dport, &initial_count);
    }

    return 0;
}

