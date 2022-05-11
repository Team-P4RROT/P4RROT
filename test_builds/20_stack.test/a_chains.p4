state parse_genhdr_uid1{
	pkt.extract(hdr.genhdr_uid1);
	transition accept;
}
state check_uid2{
	transition select(hdr.udp.dstPort){
		(5555) : parse_genhdr_uid1;
		default: accept;
	}
}
#define CHAIN_IPV4_UDP
state chain_ipv4_udp{
	transition check_uid2;
}
