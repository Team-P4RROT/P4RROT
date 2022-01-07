if (hdr.genhdr_uid1.isValid()){
	hdr.genhdr_uid2.setValid();
	#define OUTPUT_HEADER_SIZE 2
	hdr.genhdr_uid3.setValid();
	hdr.genhdr_uid3.solution = 96;
	hdr.genhdr_uid2.r1 = 58;
	hdr.genhdr_uid2.r2 = 41;
	hdr.genhdr_uid3.l = (BOOL_T)(bit<1>)(hdr.genhdr_uid3.solution < hdr.genhdr_uid1.guess);
	if (hdr.genhdr_uid3.l==1){
		hdr.genhdr_uid2.r1 = 120;
		hdr.genhdr_uid2.r2 = 60;
	}
	hdr.genhdr_uid3.l = (BOOL_T)(bit<1>)(hdr.genhdr_uid3.solution > hdr.genhdr_uid1.guess);
	if (hdr.genhdr_uid3.l==1){
		hdr.genhdr_uid2.r1 = 120;
		hdr.genhdr_uid2.r2 = 62;
	}
	meta.postprocessing = SENDBACK;
	hdr.genhdr_uid3.setInvalid();
	hdr.genhdr_uid1.setInvalid();
	meta.size_growth = 0;
	meta.size_loss = 2;
	#undef OUTPUT_HEADER_SIZE
}
