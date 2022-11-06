BOOL_T exploit;
action setter_action_uid4_true() {
	exploit = 1;
}
action setter_action_uid4_false() {
	exploit = 0;
}
table exact_match_table_uid3 {
	key = {
		hdr.genhdr_uid1.origin_timestamp: exact;
	}
	actions = {
		setter_action_uid4_true;
		setter_action_uid4_false;
	}
	size = 1;
	const default_action = setter_action_uid4_false;
}
