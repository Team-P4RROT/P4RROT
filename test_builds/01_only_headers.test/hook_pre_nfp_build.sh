echo  '''
state dummy{
	pkt.extract(hdr.genhdr_uid1);
	pkt.extract(hdr.genhdr_uid2);
	pkt.extract(hdr.genhdr_uid3);
	transition accept;
}
''' > dummy.p4