bit<8> x;
bit<16> y;
action case_uid2(){
	y = 7;
}
action case_uid3(){
	y = 5;
}
action case_uid4(){
	y = 11;
}
action default_case_uid5(){
	y = 9;
}
table switch_uid6 {
	key  = {
		x: exact;
		y: exact;
		hdr.genhdr_uid1.z: exact;
	}
	actions  = {
		case_uid2;
		case_uid3;
		case_uid4;
		default_case_uid5;
		NoAction;
	}
	const default_action = default_case_uid5;
	const entries = {
		( 5 , 8 , 1 ) : case_uid2(); 
		( 6 , 9 , 1 ) : case_uid3(); 
		( 7 , 10 , 0 ) : case_uid4(); 
	}
}
