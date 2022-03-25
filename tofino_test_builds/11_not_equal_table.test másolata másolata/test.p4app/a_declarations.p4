bit<32> difference_variable_uid2;
action setter_action_uid2_true() {
	hdr.genhdr_uid1.x = 1;
}
action setter_action_uid2_false() {
	hdr.genhdr_uid1.x = 0;
}
table eval_table_uid2 {
	actions = {
	setter_action_uid2_true;
	setter_action_uid2_false;
	}
	key = {
		difference_variable_uid2: exact;
	}
	size = 1;
	const default_action = setter_action_uid2_true;
	const entries = {
		0 : setter_action_uid2_false();
	}
}
