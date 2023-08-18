// Template for simple mac based based forwarding

#include <core.p4>
#include <psa.p4>
#define BOOL_T bit<8>

#define SKIP 0
#define SENDBACK 1
#define DROP 2

const bit<16> ETH_TYPE_IPV4 = 0x0800;
const bit<16> ETH_TYPE_ARP = 0x0806;
const bit<8> PROTO_ICMP = 1;
const bit<8> PROTO_TCP = 6;
const bit<8> PROTO_UDP = 17;

const bit<16> ARP_OPCODE_REPLY = 2;

#include "standard_headers.p4"
#include "a_headers.p4"

struct headers {
    ethernet_t   ethernet;
    ipv4_t       ipv4;
    udp_t        udp;
    tcp_t        tcp;

    #include "a_hdrlist.p4"
}

struct metadata {
    bit<16> size_growth;
    bit<16> size_loss;
    bit<8>  postprocessing;

    bit<32> parsed_bytes;
    bit<32> truncated_to;
}

struct empty_t {}
// ---------------------------------------------------------
//                      I N G R E S S
// ---------------------------------------------------------

parser ebpfIngressParser(packet_in packet,
                         out       headers hdr,
                         inout     metadata meta,
                         in        psa_ingress_parser_input_metadata_t istd,
                         in        empty_t resubmit_meta,
                         in        empty_t recirculate_meta) {
    
    state start {
        transition parse_ethernet;
    }

    state parse_ethernet {
        pkt.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            ETH_TYPE_IPV4: parse_ipv4;
            default:       reject;
        }
    }

    state parse_ipv4 {
        pkt.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol) {
            PROTO_ICMP: accept;
            PROTO_TCP:  parse_tcp;
            PROTO_UDP:  parse_udp;
            default:    reject;
        }
    }

    state parse_tcp {
        pkt.extract(hdr.tcp);

        transition accept;
    }
        

    state parse_udp {
        pkt.extract(hdr.udp);
        transition chain_ipv4_udp;
    }

    #include "a_chains.p4"

    #ifndef CHAIN_IPV4_UDP
    state chain_ipv4_udp{
        transition accept;
    }
    #endif

    #ifndef CHAIN_IPV4_TCP
    state chain_ipv4_tcp{
        transition accept;
    }
    #endif

    #ifndef CHAIN_IPV4_RAW
    state chain_ipv4_raw{
        transition accept;
    }
    #endif

    state update_udp_checksum {
        transition accept;
    }
}

control ebpfIngress(inout headers hdr,
                    inout metadata meta,
                    in    psa_ingress_input_metadata_t  istd,
                    inout psa_ingress_output_metadata_t ostd) {

    action forward_to_port (PortId_t p) {
        send_to_port(ostd, p);
    }

    action forward_to_all_ports() {
        
    }

    action drop () {
        ingress_drop(ostd);
    }

    table forward {
        key = {
            hdr.ethernet.dstAddr  : exact;
        }

        actions = {
            drop;
            forward_to_port;
        }
        size=16;
        default_action = drop;
    }

    #include "a_declarations.p4"

    apply {
        #include "a_apply.p4"
        if (hdr.tcp.isValid()){
            hdr.tcp.csum = 0;
        }
        else if (hdr.udp.isValid()){
            hdr.udp.csum = 0;
            hdr.udp.len = hdr.udp.len + meta.size_growth;
            hdr.udp.len = hdr.udp.len - meta.size_loss;
            if (meta.truncated_to!=0){
                hdr.udp.len = (bit<16>) meta.truncated_to - 34;
            }
        }
        if (hdr.ipv4.isValid()){
            hdr.ipv4.totalLen = hdr.ipv4.totalLen + meta.size_growth;
            hdr.ipv4.totalLen = hdr.ipv4.totalLen - meta.size_loss;
            if (meta.truncated_to!=0){
                hdr.ipv4.totalLen = (bit<16>) meta.truncated_to - 14;
            }
            // Note: checksum is updated later
        }
        if (meta.postprocessing == SENDBACK) {
            send_to_port(ostd, istd.ingress_port);
            if (hdr.ethernet.isValid()){
                bit<48> tmp = hdr.ethernet.srcAddr;
                hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
                hdr.ethernet.dstAddr = tmp;
            }
            
            if (hdr.ipv4.isValid()){
                bit<32> tmp = hdr.ipv4.src;
                hdr.ipv4.src = hdr.ipv4.dst;
                hdr.ipv4.dst = tmp;
            }

            if (hdr.udp.isValid()){
                bit<16> tmp = hdr.udp.srcPort;
                hdr.udp.srcPort = hdr.udp.dstPort;
                hdr.udp.dstPort = tmp;
                hdr.udp.csum = 0;
            }

            if (hdr.tcp.isValid()){
                bit<16> tmp = hdr.tcp.srcPort;
                hdr.tcp.srcPort = hdr.tcp.dstPort;
                hdr.tcp.dstPort = tmp;
                hdr.tcp.csum = 0;
            }

        } else if (meta.postprocessing == DROP) {
            ingress_drop(ostd);
        }
    }
}

control ebpfIngressDeparser(packet_out pkt,
                            out        empty_t clone_i2e_meta,
                            out        empty_t resubmit_meta,
                            out        empty_t normal_meta,
                            inout      headers hdr,
                            in         metadata meta,
                            in         psa_ingress_output_metadata_t istd) {
    
    InternetChecksum() ck;

    apply {
        if (hdr.ipv4.isValid()) {
            ck.clear();
            ck.add({
                hdr.ipv4.version,
                hdr.ipv4.ihl,
                hdr.ipv4.diffserv,
                hdr.ipv4.totalLen,
                hdr.ipv4.identification,
                hdr.ipv4.flags,
                hdr.ipv4.fragOffset,
                hdr.ipv4.ttl,
                hdr.ipv4.protocol,
                //hdr.ipv4.hdrChecksum,
                hdr.ipv4.src,
                hdr.ipv4.dst 
            });
            hdr.ipv4.hdrChecksum = ck.get();
        }


        pkt.emit(hdr);
    }
}

// ---------------------------------------------------------
//                      E G R E S S
// ---------------------------------------------------------

parser ebpfEgressParser(packet_in buffer,
                        out       headers hdr,
                        inout     metadata meta,
                        in        psa_egress_parser_input_metadata_t istd,
                        in        empty_t normal_meta,
                        in        empty_t clone_i2e_meta,
                        in        empty_t clone_e2e_meta) {

    state start {
        transition accept;
    }
}

control ebpfEgress(inout headers hdr,
                   inout metadata meta,
                   in    psa_egress_input_metadata_t  istd,
                   inout psa_egress_output_metadata_t ostd) {

    apply {
    }
}

control ebpfEgressDeparser(packet_out packet,
                           out        empty_t clone_e2e_meta,
                           out        empty_t recirculate_meta,
                           inout      headers hdr,
                           in         metadata meta,
                           in         psa_egress_output_metadata_t istd,
                           in         psa_egress_deparser_input_metadata_t edstd) {

    apply {
    }
}

IngressPipeline(ebpfIngressParser(), ebpfIngress(), ebpfIngressDeparser()) ip;
EgressPipeline(ebpfEgressParser(), ebpfEgress(), ebpfEgressDeparser()) ep;

PSA_Switch(ip, PacketReplicationEngine(), ep, BufferingQueueingEngine()) main;
