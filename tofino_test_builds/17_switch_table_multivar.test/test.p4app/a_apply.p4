if (hdr.genhdr_uid1.isValid()){
	#define OUTPUT_HEADER_SIZE 1
	switch_uid6.apply();
	#undef OUTPUT_HEADER_SIZE
}
