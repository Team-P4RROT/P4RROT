if (hdr.genhdr_uid1.isValid()){
	#define OUTPUT_HEADER_SIZE 4
	hdr.genhdr_uid1.counter_value = increment_register_action_uid2.execute(1);
	#undef OUTPUT_HEADER_SIZE
}
