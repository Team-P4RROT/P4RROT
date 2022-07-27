state parse_genhdr_uid1{
	pkt.extract(hdr.genhdr_uid1);
	transition accept;
}
state check_uid5{
	transition parse_genhdr_uid1;
}
#define CHAIN_IPV4_UDP
state chain_ipv4_udp{
	transition check_uid5;
}
