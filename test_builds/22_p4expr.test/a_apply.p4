if (hdr.genhdr_uid1.isValid()){
	#define OUTPUT_HEADER_SIZE 3
	if (hdr.genhdr_uid1.a < hdr.genhdr_uid1.b){
		hdr.genhdr_uid1.c = hdr.genhdr_uid1.b + hdr.genhdr_uid1.a;
	}
	else{
		hdr.genhdr_uid1.c = hdr.genhdr_uid1.c - hdr.genhdr_uid1.a;
	}
	#undef OUTPUT_HEADER_SIZE
}
