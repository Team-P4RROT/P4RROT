action never_call_uid3(bit<32> x){ hdr.genhdr_uid1.x = x; }
table touch_x_uid2{
	key = { hdr.genhdr_uid1.x: exact; }
	actions = { never_call_uid3; NoAction; }
	const default_action = NoAction;
}
