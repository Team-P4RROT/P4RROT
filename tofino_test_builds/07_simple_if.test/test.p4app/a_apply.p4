if (hdr.genhdr_uid1.isValid()){
	#define OUTPUT_HEADER_SIZE 5
	hdr.genhdr_uid1.x = 1;
	if (hdr.genhdr_uid1.x==1){
		hdr.genhdr_uid1.a = hdr.genhdr_uid1.a + 5;
	}
	else{
		hdr.genhdr_uid1.a = hdr.genhdr_uid1.a - 5;
	}
	#undef OUTPUT_HEADER_SIZE
}
