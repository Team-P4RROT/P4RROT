if (hdr.genhdr_uid1.isValid()){
	#define OUTPUT_HEADER_SIZE 0
	hdr.genhdr_uid2.setValid();
	exact_match_table_uid4.apply();
	unregistered = unregistered ^ 1;
	if (unregistered==1){
		exact_match_table_uid6.apply();
		if (allowed==1){
			set_digest_or_drop_table_uid11.apply();
		}
	}
	hdr.genhdr_uid2.setInvalid();
	#undef OUTPUT_HEADER_SIZE
}
