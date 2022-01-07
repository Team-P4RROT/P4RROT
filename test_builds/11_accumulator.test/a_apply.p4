if (hdr.genhdr_uid1.isValid()){
	hdr.genhdr_uid2.setValid();
	#define OUTPUT_HEADER_SIZE 4
	hdr.genhdr_uid3.setValid();
	c.read(hdr.genhdr_uid3.x,0);
	hdr.genhdr_uid2.s = hdr.genhdr_uid3.x + hdr.genhdr_uid1.v;
	c.write(0,hdr.genhdr_uid2.s);
	meta.postprocessing = SENDBACK;
	hdr.genhdr_uid3.setInvalid();
	hdr.genhdr_uid1.setInvalid();
	meta.size_growth = 0;
	meta.size_loss = 0;
	#undef OUTPUT_HEADER_SIZE
}
