state parse_genhdr_uid1{
	pkt.extract(hdr.genhdr_uid1);
	transition accept;
}
state parse_genhdr_uid4{
	pkt.extract(hdr.genhdr_uid4);
	transition accept;
}
state check_uid6{
	transition select(hdr.udp.dstPort,hdr.ipv4.src){
		(5555,167772171) : parse_genhdr_uid1;
		default: accept;
	}
}
state check_uid7{
	transition select(hdr.udp.dstPort,hdr.ipv4.src){
		(5555,167772170) : parse_genhdr_uid1;
		default: check_uid6;
	}
}
#define CHAIN_IPV4_UDP
state chain_ipv4_udp{
	transition check_uid7;
}
state check_uid8{
	genstruct_uid9 tmp = pkt.lookahead<genstruct_uid9>();

	transition select(hdr.tcp.dstPort,hdr.ipv4.src,tmp.msg_type){
		(7777,167772172,110) : parse_genhdr_uid4;
		default: accept;
	}
}
#define CHAIN_IPV4_TCP
state chain_ipv4_tcp{
	transition check_uid8;
}
