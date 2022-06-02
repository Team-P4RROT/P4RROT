if (hdr.genhdr_uid1.isValid()){
	hdr.genhdr_uid2.setValid();
	#define OUTPUT_HEADER_SIZE 8
	_shared_stack_idx.read(_shared_stack_temp,0);
	shared_stack.write(_shared_stack_temp,hdr.genhdr_uid1.a);
	_shared_stack_temp = _shared_stack_temp + 1;
	_shared_stack_idx.write(0,_shared_stack_temp);
	_shared_stack_idx.read(_shared_stack_temp,0);
	shared_stack.write(_shared_stack_temp,hdr.genhdr_uid1.aa);
	_shared_stack_temp = _shared_stack_temp + 1;
	_shared_stack_idx.write(0,_shared_stack_temp);
	_shared_stack_idx.read(_shared_stack_temp,0);
	_shared_stack_temp = _shared_stack_temp - 1;
	shared_stack.read(hdr.genhdr_uid2.b,_shared_stack_temp);
	_shared_stack_idx.write(0,_shared_stack_temp);
	_shared_stack_idx.read(_shared_stack_temp,0);
	_shared_stack_temp = _shared_stack_temp - 1;
	shared_stack.read(hdr.genhdr_uid2.bb,_shared_stack_temp);
	_shared_stack_idx.write(0,_shared_stack_temp);
	meta.postprocessing = SENDBACK;
	hdr.genhdr_uid1.setInvalid();
	meta.size_growth = 0;
	meta.size_loss = 0;
	#undef OUTPUT_HEADER_SIZE
}
