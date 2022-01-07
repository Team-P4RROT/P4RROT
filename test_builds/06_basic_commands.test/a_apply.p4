if (hdr.genhdr_uid1.isValid()){
	#define OUTPUT_HEADER_SIZE 19
	hdr.genhdr_uid1.a = hdr.genhdr_uid1.a + 5;
	hdr.genhdr_uid1.b = hdr.genhdr_uid1.b - 5;
	hdr.genhdr_uid1.c = hdr.genhdr_uid1.a + hdr.genhdr_uid1.b;
	hdr.genhdr_uid1.d = hdr.genhdr_uid1.a - hdr.genhdr_uid1.b;
	hdr.genhdr_uid1.z = hdr.genhdr_uid1.x & hdr.genhdr_uid1.y;
	hdr.genhdr_uid1.z = hdr.genhdr_uid1.x | hdr.genhdr_uid1.y;
	hdr.genhdr_uid1.z = hdr.genhdr_uid1.z ^ 1;
	hdr.genhdr_uid1.x = (BOOL_T)(bit<1>)(hdr.genhdr_uid1.a > hdr.genhdr_uid1.b);
	hdr.genhdr_uid1.y = (BOOL_T)(bit<1>)(hdr.genhdr_uid1.a < hdr.genhdr_uid1.b);
	hdr.genhdr_uid1.z = (BOOL_T)(bit<1>)(hdr.genhdr_uid1.a == hdr.genhdr_uid1.b);
	#undef OUTPUT_HEADER_SIZE
}
