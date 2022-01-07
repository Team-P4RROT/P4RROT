if (hdr.genhdr_uid1.isValid()){
	hdr.genhdr_uid2.setValid();
	#define OUTPUT_HEADER_SIZE 4
	hdr.genhdr_uid3.setValid();
	hdr.genhdr_uid1.a = 5;
	hdr.genhdr_uid1.b = 0;
	hdr.genhdr_uid2.s = 10;
	hdr.genhdr_uid3.t = 110;
	hdr.genhdr_uid1.c = hdr.genhdr_uid1.b;
	hdr.genhdr_uid2.x = 1;
	hdr.genhdr_uid2.y = 0;
	hdr.genhdr_uid2.y = hdr.genhdr_uid2.x;
	hdr.genhdr_uid3.setInvalid();
	hdr.genhdr_uid1.setInvalid();
	meta.size_growth = 0;
	meta.size_loss = 16;
	#undef OUTPUT_HEADER_SIZE
}
