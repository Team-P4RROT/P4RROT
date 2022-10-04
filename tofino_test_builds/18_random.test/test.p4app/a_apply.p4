if (hdr.genhdr_uid1.isValid()){
	#define OUTPUT_HEADER_SIZE 15
	hdr.genhdr_uid1.a = rnd_uid2.get();
	hdr.genhdr_uid1.b = rnd_uid3.get();
	hdr.genhdr_uid1.c = rnd_uid4.get();
	hdr.genhdr_uid1.d = rnd_uid5.get();
	#undef OUTPUT_HEADER_SIZE
}
