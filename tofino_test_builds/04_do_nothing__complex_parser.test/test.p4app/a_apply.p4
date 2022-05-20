if (hdr.genhdr_uid1.isValid()){
	hdr.genhdr_uid2.setValid();
	hdr.genhdr_uid3.setValid();
		hdr.genhdr_uid3.setInvalid();
	hdr.genhdr_uid1.setInvalid();
}
else if (hdr.genhdr_uid4.isValid()){
	hdr.genhdr_uid5.setValid();
		hdr.genhdr_uid5.setInvalid();
}
