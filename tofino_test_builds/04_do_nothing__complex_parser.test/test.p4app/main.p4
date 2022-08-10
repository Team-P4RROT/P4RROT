#include <core.p4>
#if __TARGET_TOFINO__ == 2
#include <t2na.p4>
#else
#include <tna.p4>
#endif


// HEADERS AND TYPES ************************************************************
#define BOOL_T bit<8>

#include "standard_headers.p4"

#include "a_headers.p4"

// #meta
struct ingress_metadata_t {

    bit<16> size_growth;
    bit<16> size_loss;

}

struct egress_metadata_t {
}


struct header_t {
    ethernet_t ethernet;
    ipv4_t ipv4;
    udp_t udp;
	tcp_t tcp;
	
	#include "a_hdrlist.p4"
}

// INGRESS ************************************************************

parser TofinoIngressParser(
        packet_in pkt,
        out header_t hdr,
        out ingress_intrinsic_metadata_t meta) {

    state start {
        pkt.extract(meta);
        transition select(meta.resubmit_flag) {
            0 : parse_port_metadata;
        }
    }

    state parse_port_metadata {
#if __TARGET_TOFINO__ == 2
        pkt.advance(192);
#else
        pkt.advance(64);
#endif
        transition accept;
    }
}


parser TofinoEgressParser(
        packet_in pkt,
        out egress_intrinsic_metadata_t eg_intr_md) {

    state start {
        pkt.extract(eg_intr_md);
        transition accept;
    }

}


parser SwitchIngressParser(
        packet_in pkt,
        out header_t hdr,
        out ingress_metadata_t ig_md,
        out ingress_intrinsic_metadata_t meta) {


    TofinoIngressParser() tofino_parser;
	
    state start {
	    tofino_parser.apply(pkt, hdr, meta);
        transition parse_ethernet;
    }

    state parse_ethernet {
        pkt.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            16w0x800: parse_ipv4;
            default: accept;
        }
    }

    state parse_ipv4 {
        pkt.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol){
            17 : parse_udp;
            6  : parse_tcp;
            default: chain_ipv4_raw;
        }
    }

    state parse_udp{
        pkt.extract(hdr.udp);
        transition chain_ipv4_udp;
    }

    state parse_tcp{
        pkt.extract(hdr.tcp);
        transition chain_ipv4_tcp;
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

}

control SwitchIngress(
        inout header_t hdr,
        inout ingress_metadata_t ig_md,
        in ingress_intrinsic_metadata_t meta,
        in ingress_intrinsic_metadata_from_parser_t ig_prsr_md,
        inout ingress_intrinsic_metadata_for_deparser_t ig_dprsr_md,
        inout ingress_intrinsic_metadata_for_tm_t ig_tm_md) {

	#include "a_declarations.p4"

    // #ingress
    apply {
	
		#include "a_apply.p4"

    }
}

control SwitchIngressDeparser(
        packet_out pkt,
        inout header_t hdr,
        in ingress_metadata_t ig_md,
        in ingress_intrinsic_metadata_for_deparser_t ig_dprsr_md) {

    apply {
        pkt.emit(hdr);
    }
}

// EGRESS ************************************************************

parser SwitchEgressParser(
        packet_in pkt,
        out header_t hdr,
        out egress_metadata_t eg_md,
        out egress_intrinsic_metadata_t eg_intr_md) {

    TofinoEgressParser() tofino_parser;

    state start {
	    tofino_parser.apply(pkt, eg_intr_md);
        transition parse_ethernet;
    }

    state parse_ethernet {
        pkt.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            16w0x800: parse_ipv4;
            default: accept;
        }
    }

    state parse_ipv4 {
        pkt.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol){
            17 : parse_udp;
            6  : parse_tcp;
            default: chain_ipv4_raw;
        }
    }

    state parse_udp{
        pkt.extract(hdr.udp);
        transition chain_ipv4_udp;
    }

    state parse_tcp{
        pkt.extract(hdr.tcp);
        transition chain_ipv4_tcp;
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
}

control SwitchEgress(
        inout header_t hdr,
        inout egress_metadata_t eg_md,
        in egress_intrinsic_metadata_t eg_intr_md,
        in egress_intrinsic_metadata_from_parser_t eg_intr_from_prsr,
        inout egress_intrinsic_metadata_for_deparser_t eg_intr_md_for_dprsr,
        inout egress_intrinsic_metadata_for_output_port_t eg_intr_md_for_oport) {

    apply {

    }
}

control SwitchEgressDeparser(
        packet_out pkt,
        inout header_t hdr,
        in egress_metadata_t eg_md,
        in egress_intrinsic_metadata_for_deparser_t eg_dprsr_md) {

    Checksum() ipv4_checksum;

    apply {

        hdr.ipv4.hdrChecksum = ipv4_checksum.update({
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

        pkt.emit(hdr);
    }
}

Pipeline(SwitchIngressParser(),
         SwitchIngress(),
         SwitchIngressDeparser(),
         SwitchEgressParser(),
         SwitchEgress(),
         SwitchEgressDeparser()) pipe;

Switch(pipe) main;

