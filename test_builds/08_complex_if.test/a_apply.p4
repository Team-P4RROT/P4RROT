if (hdr.genhdr_uid1.isValid()){
	#define OUTPUT_HEADER_SIZE 9
	hdr.genhdr_uid1.x = (BOOL_T)(bit<1>)(hdr.genhdr_uid1.a > hdr.genhdr_uid1.b);
	if (hdr.genhdr_uid1.x==1){
		hdr.genhdr_uid1.a = hdr.genhdr_uid1.a + 5;
		hdr.genhdr_uid1.a = hdr.genhdr_uid1.a + 5;
	}
	else{
		hdr.genhdr_uid1.a = hdr.genhdr_uid1.a - 6;
		hdr.genhdr_uid1.a = hdr.genhdr_uid1.a - 6;
	}
	hdr.genhdr_uid1.a = hdr.genhdr_uid1.a + 7;
	if (hdr.genhdr_uid1.x==1){
		hdr.genhdr_uid1.a = hdr.genhdr_uid1.a + 5;
		hdr.genhdr_uid1.a = hdr.genhdr_uid1.a + 5;
		if (hdr.genhdr_uid1.x==1){
			hdr.genhdr_uid1.a = hdr.genhdr_uid1.a + 9;
			meta.postprocessing = SENDBACK;
		}
	}
	else{
		hdr.genhdr_uid1.a = hdr.genhdr_uid1.a - 6;
		hdr.genhdr_uid1.a = hdr.genhdr_uid1.a - 6;
	}
	#undef OUTPUT_HEADER_SIZE
}
