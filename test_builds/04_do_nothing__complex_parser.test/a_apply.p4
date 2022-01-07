if (hdr.genhdr_uid1.isValid()){
	hdr.genhdr_uid2.setValid();
	#define OUTPUT_HEADER_SIZE 4
	hdr.genhdr_uid3.setValid();
		hdr.genhdr_uid3.setInvalid();
	hdr.genhdr_uid1.setInvalid();
	meta.size_growth = 0;
	meta.size_loss = 4;
	#undef OUTPUT_HEADER_SIZE
}
else if (hdr.genhdr_uid4.isValid()){
	#define OUTPUT_HEADER_SIZE 8
	hdr.genhdr_uid5.setValid();
		hdr.genhdr_uid5.setInvalid();
	#undef OUTPUT_HEADER_SIZE
}
