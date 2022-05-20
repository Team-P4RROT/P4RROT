if (hdr.genhdr_uid1.isValid()){
	#define OUTPUT_HEADER_SIZE 0
	bit<64> tmp;
	tmp = read_shared_array_action_uid2.execute(1);
	tmp = tmp + 1;
	write_shared_array_action_uid3.execute(1);
	#undef OUTPUT_HEADER_SIZE
}
