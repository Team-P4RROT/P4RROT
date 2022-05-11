if (hdr.genhdr_uid1.isValid()){
	#define OUTPUT_HEADER_SIZE 9
	hdr.genhdr_uid1.x = 1;
	difference_variable_uid3 = hdr.genhdr_uid1.a - hdr.genhdr_uid1.b;
	eval_table_uid2.apply();
	if (hdr.genhdr_uid1.x==1){
		hdr.genhdr_uid1.a = hdr.genhdr_uid1.a + 5;
	}
	else{
		hdr.genhdr_uid1.a = hdr.genhdr_uid1.a - 5;
	}
	#undef OUTPUT_HEADER_SIZE
}
