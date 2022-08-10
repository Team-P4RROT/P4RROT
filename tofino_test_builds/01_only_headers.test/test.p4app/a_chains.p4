state parse_genhdr_uid1{
	pkt.extract(hdr.genhdr_uid1);
	transition accept;
}
