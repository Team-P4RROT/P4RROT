action p4expr_uid2(){ hdr.genhdr_uid1.b = hdr.genhdr_uid1.b + 1; }
action p4expr_uid3(){ hdr.genhdr_uid1.c = hdr.genhdr_uid1.c + 1; }
table p4exprtable_uid4{
	actions = { p4expr_uid3; }
	const default_action = p4expr_uid3;
}
action p4expr_uid5(){ hdr.genhdr_uid1.c = hdr.genhdr_uid1.c + 1; }
@an_annotation
table p4exprtable_uid6{
	actions = { p4expr_uid5; }
	const default_action = p4expr_uid5;
}
