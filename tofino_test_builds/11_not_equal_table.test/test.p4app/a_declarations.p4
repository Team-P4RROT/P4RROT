bit<32> difference_variable_uid3;
action setter_action_uid4_true() {
	hdr.genhdr_uid1.x = 1;
}
action setter_action_uid4_false() {
	hdr.genhdr_uid1.x = 0;
}
table eval_table_uid2 {
	key = {
		difference_variable_uid3: exact;
	}
	actions = {
		setter_action_uid4_true;
		setter_action_uid4_false;
	}
	size = 1;
	const default_action = setter_action_uid4_true;
	const entries = {
		0 : setter_action_uid4_false();
	}
}
