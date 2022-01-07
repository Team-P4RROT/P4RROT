if (hdr.genhdr_uid1.isValid()){
	hdr.genhdr_uid2.setValid();
	#define OUTPUT_HEADER_SIZE 4
	hdr.genhdr_uid3.setValid();
	hdr.genhdr_uid3.op_guess = 1;
	hdr.genhdr_uid3.b = (BOOL_T)(bit<1>)(hdr.genhdr_uid1.op == hdr.genhdr_uid3.op_guess);
	if (hdr.genhdr_uid3.b==1){
		msgbox.read(hdr.genhdr_uid2.response,hdr.genhdr_uid1.index);
	}
	hdr.genhdr_uid3.op_guess = 2;
	hdr.genhdr_uid3.b = (BOOL_T)(bit<1>)(hdr.genhdr_uid1.op == hdr.genhdr_uid3.op_guess);
	if (hdr.genhdr_uid3.b==1){
		msgbox.write(hdr.genhdr_uid1.index,hdr.genhdr_uid1.value);
		hdr.genhdr_uid2.response = hdr.genhdr_uid1.value;
	}
	meta.postprocessing = SENDBACK;
	hdr.genhdr_uid3.setInvalid();
	hdr.genhdr_uid1.setInvalid();
	meta.size_growth = 0;
	meta.size_loss = 8;
	#undef OUTPUT_HEADER_SIZE
}
