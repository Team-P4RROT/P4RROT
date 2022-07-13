BOOL_T allowed;
action setter_action_uid5_true() {
	allowed = 1;
}
action setter_action_uid5_false() {
	allowed = 0;
}
table exact_match_table_uid4 {
	key = {
		hdr.ipv4.src: exact;
		hdr.udp.srcPort: exact;
	}
	actions = {
		setter_action_uid5_true;
		setter_action_uid5_false;
	}
	size = 1;
	const default_action = setter_action_uid5_false;
}
action setter_action_uid10() {
	ig_dprsr_md.digest_type = 3;
}
action drop_packet() {
	ig_dprsr_md.drop_ctl = 0x1;
}
table set_digest_or_drop_table_uid9 {
	key = {
		hdr.udp.dstPort: exact;
	}
	actions = {
		setter_action_uid10;
		drop_packet;
	}
	size = 1;
	const default_action = drop_packet;
}
