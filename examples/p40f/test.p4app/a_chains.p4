state parse_genhdr_uid11{
	pkt.extract(hdr.genhdr_uid11);
	transition accept;
}
state check_uid21{
	transition parse_genhdr_uid11;
}
#define CHAIN_IPV4_TCP
state chain_ipv4_tcp{
	transition check_uid21;
}
