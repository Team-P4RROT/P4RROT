if (hdr.genhdr_uid1.isValid()){
	hdr.genhdr_uid2.setValid();
	#define OUTPUT_HEADER_SIZE 4
	hdr.genhdr_uid3.setValid();
	hdr.genhdr_uid3.c = 43;
	hdr.genhdr_uid3.l = (BOOL_T)(bit<1>)(hdr.genhdr_uid1.op == hdr.genhdr_uid3.c);
	if (hdr.genhdr_uid3.l==1){
		hdr.genhdr_uid2.r = hdr.genhdr_uid1.a + hdr.genhdr_uid1.b;
	}
	hdr.genhdr_uid3.c = 45;
	hdr.genhdr_uid3.l = (BOOL_T)(bit<1>)(hdr.genhdr_uid1.op == hdr.genhdr_uid3.c);
	if (hdr.genhdr_uid3.l==1){
		hdr.genhdr_uid2.r = hdr.genhdr_uid1.a - hdr.genhdr_uid1.b;
	}
	meta.postprocessing = SENDBACK;
	hdr.genhdr_uid3.setInvalid();
	hdr.genhdr_uid1.setInvalid();
	meta.size_growth = 0;
	meta.size_loss = 5;
	#undef OUTPUT_HEADER_SIZE
}
