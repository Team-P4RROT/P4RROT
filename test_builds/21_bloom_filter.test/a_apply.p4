if (hdr.genhdr_uid1.isValid()){
	#define OUTPUT_HEADER_SIZE 5
	hdr.genhdr_uid1.b = 10;
	truncate(meta.parsed_bytes + OUTPUT_HEADER_SIZE);
	meta.truncated_to = meta.parsed_bytes + OUTPUT_HEADER_SIZE;
	#undef OUTPUT_HEADER_SIZE
}
