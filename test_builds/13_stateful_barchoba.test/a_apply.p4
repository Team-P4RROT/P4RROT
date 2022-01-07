if (hdr.genhdr_uid1.isValid()){
	hdr.genhdr_uid2.setValid();
	#define OUTPUT_HEADER_SIZE 2
	hdr.genhdr_uid3.setValid();
	// init variables 
	shared_solution.read(hdr.genhdr_uid3.solution,0);
	hdr.genhdr_uid3.good = 1;
	hdr.genhdr_uid2.r1 = 58;
	hdr.genhdr_uid2.r2 = 41;
	// check whether solution<guess 
	hdr.genhdr_uid3.l = (BOOL_T)(bit<1>)(hdr.genhdr_uid3.solution < hdr.genhdr_uid1.guess);
	if (hdr.genhdr_uid3.l==1){
		hdr.genhdr_uid2.r1 = 120;
		hdr.genhdr_uid2.r2 = 60;
		hdr.genhdr_uid3.good = 0;
	}
	// check whether solution>guess 
	hdr.genhdr_uid3.l = (BOOL_T)(bit<1>)(hdr.genhdr_uid3.solution > hdr.genhdr_uid1.guess);
	if (hdr.genhdr_uid3.l==1){
		hdr.genhdr_uid2.r1 = 120;
		hdr.genhdr_uid2.r2 = 62;
		hdr.genhdr_uid3.good = 0;
	}
	// generate a new number if required 
	if (hdr.genhdr_uid3.good==1){
		random< bit<8> >(hdr.genhdr_uid3.solution,(bit<8>)0,(bit<8>)255);
		shared_solution.write(0,hdr.genhdr_uid3.solution);
	}
	// send back the result 
	meta.postprocessing = SENDBACK;
	hdr.genhdr_uid3.setInvalid();
	hdr.genhdr_uid1.setInvalid();
	meta.size_growth = 1;
	meta.size_loss = 0;
	#undef OUTPUT_HEADER_SIZE
}
