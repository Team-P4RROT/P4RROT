bit<8> x;
bit<8> y;
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
		( 5 ) : case_uid2(); 
		( 9 ) : case_uid3(); 
		( 11 ) : case_uid4(); 
	}
}
