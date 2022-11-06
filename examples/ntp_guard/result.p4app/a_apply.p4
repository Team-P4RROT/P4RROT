if (hdr.genhdr_uid1.isValid()){
	#define OUTPUT_HEADER_SIZE 32
	hdr.genhdr_uid2.setValid();
	exact_match_table_uid3.apply();
	if (exploit==1){
		ig_dprsr_md.drop_ctl = 0x1;
	}
	hdr.genhdr_uid2.setInvalid();
	#undef OUTPUT_HEADER_SIZE
}
