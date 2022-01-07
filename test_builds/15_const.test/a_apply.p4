if (hdr.genhdr_uid1.isValid()){
	hdr.genhdr_uid2.setValid();
	#define OUTPUT_HEADER_SIZE 4
	BOOL_T l;
	l = (BOOL_T)(bit<1>)(hdr.genhdr_uid1.op == op_plus);
	if (l==1){
		hdr.genhdr_uid2.r = hdr.genhdr_uid1.a + hdr.genhdr_uid1.b;
	}
	l = (BOOL_T)(bit<1>)(hdr.genhdr_uid1.op == op_minus);
	if (l==1){
		hdr.genhdr_uid2.r = hdr.genhdr_uid1.a - hdr.genhdr_uid1.b;
	}
	meta.postprocessing = SENDBACK;
	hdr.genhdr_uid1.setInvalid();
	meta.size_growth = 0;
	meta.size_loss = 5;
	#undef OUTPUT_HEADER_SIZE
}
