if (hdr.genhdr_uid1.isValid()){
	hdr.genhdr_uid2.setValid();
	#define OUTPUT_HEADER_SIZE 4
	if (hdr.genhdr_uid1.op==op_plus){
		hdr.genhdr_uid2.r = hdr.genhdr_uid1.a + hdr.genhdr_uid1.b;
	}
	else if (hdr.genhdr_uid1.op==op_minus){
		hdr.genhdr_uid2.r = hdr.genhdr_uid1.a - hdr.genhdr_uid1.b;
	}
	else{
		hdr.genhdr_uid2.r = 3735936685;
	}
	meta.postprocessing = SENDBACK;
	hdr.genhdr_uid1.setInvalid();
	meta.size_growth = 0;
	meta.size_loss = 5;
	#undef OUTPUT_HEADER_SIZE
}
