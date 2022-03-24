bit<32> generated_variable_0;
action generated_setter_action_0_true() {
	hdr.genhdr_uid1.x = 1;
}
action generated_setter_action_0_false() {
	hdr.genhdr_uid1.x = 0;
}
table generated_table_0 {
	actions = {
	generated_setter_action_0_true_true;
	generated_setter_action_0_false_true;
	}
	key = {
		generated_variable_0: ternary;
	}
	size = 2;
	const default_action = generated_setter_action_0_true;
	const entries = {
		0b00000000000000000000000000000000&&&0b11111111111111111111111111111111 : generated_setter_action_0_false();
		0b00000000000000000000000000000000&&&0b10000000000000000000000000000000 : generated_setter_action_0_false();
	}
}
