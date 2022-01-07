if (hdr.genhdr_uid1.isValid()){
	#define OUTPUT_HEADER_SIZE 8
	bit<64> tmp;
	hdr.genhdr_uid1.a = 0;
	@atomic{
	ATOMIC_BEGIN
		cnt.read(tmp,0);
		tmp = tmp + 1;
		cnt.write(0,tmp);
	ATOMIC_END
	}
	hdr.genhdr_uid1.a = tmp;
	#undef OUTPUT_HEADER_SIZE
}
