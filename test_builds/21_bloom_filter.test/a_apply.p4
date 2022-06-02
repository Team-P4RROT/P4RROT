if (hdr.genhdr_uid1.isValid()){
	hdr.genhdr_uid2.setValid();
	#define OUTPUT_HEADER_SIZE 2
	BOOL_T comp_res;
	bit<8> operation;
	operation = 97;
	comp_res = (BOOL_T)(bit<1>)(hdr.genhdr_uid1.op == operation);
	if (comp_res==1){
		hash(_mybloom_hash, HashAlgorithm.crc16, (bit<32>) 0, {hdr.genhdr_uid1.x, (bit<8>) 0}, (bit<32>)1000);
		_mybloom_register.write(_mybloom_hash, (bit<1>) 1);
		hash(_mybloom_hash, HashAlgorithm.crc16, (bit<32>) 0, {hdr.genhdr_uid1.x, (bit<8>) 1}, (bit<32>)1000);
		_mybloom_register.write(_mybloom_hash, (bit<1>) 1);
		hash(_mybloom_hash, HashAlgorithm.crc16, (bit<32>) 0, {hdr.genhdr_uid1.x, (bit<8>) 2}, (bit<32>)1000);
		_mybloom_register.write(_mybloom_hash, (bit<1>) 1);
	}
	operation = 99;
	comp_res = (BOOL_T)(bit<1>)(hdr.genhdr_uid1.op == operation);
	if (comp_res==1){
		hdr.genhdr_uid2.contains = (bit<8>)1;
		hash(_mybloom_hash, HashAlgorithm.crc16, (bit<32>) 0, {hdr.genhdr_uid1.x, (bit<8>) 0}, (bit<32>)1000);
		_mybloom_register.read(_mybloom_result, _mybloom_hash);
		if (_mybloom_result != 1){
			hdr.genhdr_uid2.contains = (bit<8>) 0;
		};
		hash(_mybloom_hash, HashAlgorithm.crc16, (bit<32>) 0, {hdr.genhdr_uid1.x, (bit<8>) 1}, (bit<32>)1000);
		_mybloom_register.read(_mybloom_result, _mybloom_hash);
		if (_mybloom_result != 1){
			hdr.genhdr_uid2.contains = (bit<8>) 0;
		};
		hash(_mybloom_hash, HashAlgorithm.crc16, (bit<32>) 0, {hdr.genhdr_uid1.x, (bit<8>) 2}, (bit<32>)1000);
		_mybloom_register.read(_mybloom_result, _mybloom_hash);
		if (_mybloom_result != 1){
			hdr.genhdr_uid2.contains = (bit<8>) 0;
		};
	}
	meta.postprocessing = SENDBACK;
	hdr.genhdr_uid1.setInvalid();
	meta.size_growth = 0;
	meta.size_loss = 3;
	#undef OUTPUT_HEADER_SIZE
}
