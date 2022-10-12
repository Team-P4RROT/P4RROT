if (hdr.genhdr_uid1.isValid()){
	#define OUTPUT_HEADER_SIZE 9
	hdr.genhdr_uid1.y = rate.execute(hdr.genhdr_uid1.x,hdr.genhdr_uid1.i);
	#undef OUTPUT_HEADER_SIZE
}
