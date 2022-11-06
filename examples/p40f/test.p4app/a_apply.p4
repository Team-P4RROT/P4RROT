if (hdr.genhdr_uid11.isValid()){
	#define OUTPUT_HEADER_SIZE 0
	hdr.genhdr_uid12.setValid();
	percent_to_sample = 10;
	MAX_OS_LABELS = 1024;
	MAX_OS_LABELS_minus_one = 1023;
	PORT_TO_SAMPLE = 80;
	SYN_FLAG = 2;
	SYN_AND_PSH_FLAG = 10;
	SYN_AND_URG_FLAG = 34;
	SYN_PSH_URG_FLAG = 42;
	fingerprint = (BOOL_T)(bit<1>)(hdr.tcp.ctrl == SYN_FLAG);
	equals_var = (BOOL_T)(bit<1>)(hdr.tcp.ctrl == SYN_AND_URG_FLAG);
	fingerprint = equals_var | fingerprint;
	equals_var = (BOOL_T)(bit<1>)(hdr.tcp.ctrl == SYN_AND_PSH_FLAG);
	fingerprint = equals_var | fingerprint;
	equals_var = (BOOL_T)(bit<1>)(hdr.tcp.ctrl == SYN_PSH_URG_FLAG);
	fingerprint = equals_var | fingerprint;
	binary_search_run = 1;
	binary_search_hi = 64;
	binary_search_lo = 0;
	binary_search_lo_mss = 0;
	binary_search_hi_mss = meta.tcp_metadata.mss;
	binary_search_hi_mss = binary_search_hi_mss << 6;
	if (fingerprint==1){
		if (binary_search_run==1){
			binary_search_mid = binary_search_hi + binary_search_lo;
			binary_search_mid = binary_search_mid >> 1;
			binary_search_mid_mss = binary_search_hi_mss + binary_search_lo_mss;
			binary_search_mid_mss = binary_search_mid_mss >> 1;
			window_smaller_than_mss = (BOOL_T)(bit<1>)(hdr.tcp.window < binary_search_mid_mss);
			if (window_smaller_than_mss==1){
				binary_search_hi = binary_search_mid;
				binary_search_hi_mss = binary_search_mid_mss;
			}
			else{
				window_greater_than_mss = (BOOL_T)(bit<1>)(hdr.tcp.window > binary_search_mid_mss);
				if (window_greater_than_mss==1){
					binary_search_lo = binary_search_mid;
					binary_search_lo_mss = binary_search_mid_mss;
				}
				else{
					wsize_div_mss = binary_search_mid_mss;
					binary_search_run = 0;
				}
			}
		}
		if (binary_search_run==1){
			binary_search_mid = binary_search_hi + binary_search_lo;
			binary_search_mid = binary_search_mid >> 1;
			binary_search_mid_mss = binary_search_hi_mss + binary_search_lo_mss;
			binary_search_mid_mss = binary_search_mid_mss >> 1;
			window_smaller_than_mss = (BOOL_T)(bit<1>)(hdr.tcp.window < binary_search_mid_mss);
			if (window_smaller_than_mss==1){
				binary_search_hi = binary_search_mid;
				binary_search_hi_mss = binary_search_mid_mss;
			}
			else{
				window_greater_than_mss = (BOOL_T)(bit<1>)(hdr.tcp.window > binary_search_mid_mss);
				if (window_greater_than_mss==1){
					binary_search_lo = binary_search_mid;
					binary_search_lo_mss = binary_search_mid_mss;
				}
				else{
					wsize_div_mss = binary_search_mid_mss;
					binary_search_run = 0;
				}
			}
		}
		if (binary_search_run==1){
			binary_search_mid = binary_search_hi + binary_search_lo;
			binary_search_mid = binary_search_mid >> 1;
			binary_search_mid_mss = binary_search_hi_mss + binary_search_lo_mss;
			binary_search_mid_mss = binary_search_mid_mss >> 1;
			window_smaller_than_mss = (BOOL_T)(bit<1>)(hdr.tcp.window < binary_search_mid_mss);
			if (window_smaller_than_mss==1){
				binary_search_hi = binary_search_mid;
				binary_search_hi_mss = binary_search_mid_mss;
			}
			else{
				window_greater_than_mss = (BOOL_T)(bit<1>)(hdr.tcp.window > binary_search_mid_mss);
				if (window_greater_than_mss==1){
					binary_search_lo = binary_search_mid;
					binary_search_lo_mss = binary_search_mid_mss;
				}
				else{
					wsize_div_mss = binary_search_mid_mss;
					binary_search_run = 0;
				}
			}
		}
		if (binary_search_run==1){
			binary_search_mid = binary_search_hi + binary_search_lo;
			binary_search_mid = binary_search_mid >> 1;
			binary_search_mid_mss = binary_search_hi_mss + binary_search_lo_mss;
			binary_search_mid_mss = binary_search_mid_mss >> 1;
			window_smaller_than_mss = (BOOL_T)(bit<1>)(hdr.tcp.window < binary_search_mid_mss);
			if (window_smaller_than_mss==1){
				binary_search_hi = binary_search_mid;
				binary_search_hi_mss = binary_search_mid_mss;
			}
			else{
				window_greater_than_mss = (BOOL_T)(bit<1>)(hdr.tcp.window > binary_search_mid_mss);
				if (window_greater_than_mss==1){
					binary_search_lo = binary_search_mid;
					binary_search_lo_mss = binary_search_mid_mss;
				}
				else{
					wsize_div_mss = binary_search_mid_mss;
					binary_search_run = 0;
				}
			}
		}
	}
	if (binary_search_run==1){
		binary_search_mid = binary_search_hi + binary_search_lo;
		binary_search_mid = binary_search_mid >> 1;
		binary_search_mid_mss = binary_search_hi_mss + binary_search_lo_mss;
		binary_search_mid_mss = binary_search_mid_mss >> 1;
		window_equals_lo_mss = (BOOL_T)(bit<1>)(hdr.tcp.window == binary_search_lo_mss);
		if (window_equals_lo_mss==1){
			wsize_div_mss = binary_search_lo;
		}
		else{
			window_equals_hi_mss = (BOOL_T)(bit<1>)(hdr.tcp.window == binary_search_hi_mss);
			if (window_equals_hi_mss==1){
				wsize_div_mss = binary_search_hi;
			}
			else{
				window_equals_mid_mss = (BOOL_T)(bit<1>)(hdr.tcp.window == binary_search_mid_mss);
				if (window_equals_mid_mss==1){
					wsize_div_mss = binary_search_mid;
				}
				else{
					wsize_div_mss = 0;
				}
			}
		}
		signature_result = 1023;
		CONST_TO_SUBTRACT = 34;
		is_generic_fuzzy = 0;
		drop_ip = 0;
		drop_pkt = 0;
		redirect_to = 0;
		quirk_nz_id_a = (BOOL_T)(bit<1>)(hdr.ipv4.flags & 2 != 0);
		quirk_df = (BOOL_T)(bit<1>)(hdr.ipv4.flags & 2 != 0);
		quirk_nz_id_b = (BOOL_T)(bit<1>)(hdr.ipv4.identification & 2 != 0);
		quirk_nz_id = quirk_nz_id_a & quirk_nz_id_b;
		quirk_nz_id_a = (BOOL_T)(bit<1>)(hdr.ipv4.flags & 2 == 0);
		quirk_nz_id_b = (BOOL_T)(bit<1>)(hdr.ipv4.identification & 2 == 0);
		quirk_zero_id = quirk_nz_id_a & quirk_nz_id_b;
		quirk_ecn = (BOOL_T)(bit<1>)(hdr.ipv4.diffserv & 3 != 0);
		quirk_ecn_b = (BOOL_T)(bit<1>)(hdr.tcp.ecn & 7 != 0);
		quirk_ecn = quirk_ecn | quirk_ecn_b;
		quirk_nz_mbz = (BOOL_T)(bit<1>)(hdr.ipv4.flags & 4 != 0);
		quirk_nz_ack = (BOOL_T)(bit<1>)(hdr.tcp.ctrl & 20 == 0);
		quirk_nz_urg = (BOOL_T)(bit<1>)(hdr.tcp.urgentPtr == 0);
		quirk_nz_urg = quirk_nz_urg ^ 1;
		quirk_nz_urg = quirk_nz_urg & quirk_nz_ack;
		quirk_nz_ack_b = (BOOL_T)(bit<1>)(hdr.tcp.ackNo == 0);
		quirk_zero_ack = (BOOL_T)(bit<1>)(hdr.tcp.ctrl & 16 != 0);
		quirk_zero_ack = quirk_zero_ack & quirk_nz_ack_b;
		quirk_nz_ack_b = quirk_nz_ack_b ^ 1;
		quirk_nz_ack = quirk_nz_ack & quirk_nz_ack_b;
		quirk_urg = (BOOL_T)(bit<1>)(hdr.tcp.ctrl & 20 != 0);
		ip_header_length = (bit<32>) meta.tcp_metadata.olen;
		payload_length = standard_metadata.packet_length;
		tcp_offset_long = (bit<32>) meta.tcp_metadata.olen;
		tcp_offset_long = tcp_offset_long << 2;
		payload_length = payload_length - tcp_offset_long;
		payload_length = payload_length - ip_header_length;
		payload_length = payload_length - CONST_TO_SUBTRACT;
		pclass = (BOOL_T)(bit<1>)(payload_length == 0);
		pclass = pclass ^ 1;
		control_plane_set_table_uid13.apply();
		os_counters.read(os_counter_holder,signature_result);
		os_counter_holder = os_counter_holder + 1;
		os_counters.write(signature_result,os_counter_holder);
		if (drop_pkt==1){
			meta.tcp_metadata.ip_forward = 0;
		}
		if (drop_ip==1){
			hash(_tcpbloom_hash_1uid2, HashAlgorithm.crc16, (bit<32>) 0, {hdr.ipv4.src}, 32w15);
			_tcpbloom_register_1.read(_tcpbloom_result_1uid4, _tcpbloom_hash_1uid2);
			_tcpbloom_result_1uid4 = _tcpbloom_result_1uid4 + 1;
			_tcpbloom_register_1.write(_tcpbloom_result_1uid4, _tcpbloom_hash_1uid2);
		}
		if (should_redirect==1){
			hdr.ipv4.dst = redirect_to;
		}
		random< bit<8> >(random_number,(bit<8>)0,(bit<8>)100);
		equals_port_to_sample = (BOOL_T)(bit<1>)(hdr.tcp.dstPort == PORT_TO_SAMPLE);
		sample_random = (BOOL_T)(bit<1>)(random_number < percent_to_sample);
		sample_SYN = (BOOL_T)(bit<1>)(signature_result == MAX_OS_LABELS_minus_one);
		not_generic_fuzzy = is_generic_fuzzy;
		not_generic_fuzzy = not_generic_fuzzy ^ 1;
		sample_SYN = sample_SYN | not_generic_fuzzy;
		sample_SYN = sample_SYN | sample_random;
		sample_SYN = sample_SYN & equals_port_to_sample;
		if (sample_SYN==1){
			clone(CloneType.I2E, 250);
			hash(_httpbloom_hash_1uid7, HashAlgorithm.crc16, (bit<32>) 0, {hdr.ipv4.src,hdr.ipv4.dst,hdr.tcp.srcPort,hdr.tcp.seqNo}, 32w15);
			_httpbloom_register_1.read(_httpbloom_result_1uid9, _httpbloom_hash_1uid7);
			_httpbloom_result_1uid9 = _httpbloom_result_1uid9 + 1;
			_httpbloom_register_1.write(_httpbloom_result_1uid9, _httpbloom_hash_1uid7);
		}
	}
	if (equals_port_to_sample==1){
		seq_no_plus_one = hdr.tcp.seqNo;
		seq_no_plus_one = seq_no_plus_one + 1;
		hash(_httpbloom_hash_1uid7, HashAlgorithm.crc16, (bit<32>) 0, {hdr.ipv4.src,hdr.ipv4.dst,hdr.tcp.srcPort,seq_no_plus_one}, 32w15);
		_httpbloom_register_1.read(_httpbloom_result_1uid9, _httpbloom_hash_1uid7);
		present_in_bloom = 0;
		if (_httpbloom_result_1uid9 > 0){
			present_in_bloom = 1;
		};
		if (present_in_bloom==1){
			clone(CloneType.I2E, 250);
			meta.tcp_metadata.ip_forward = 0;
		}
	}
	hash(_tcpbloom_hash_1uid2, HashAlgorithm.crc16, (bit<32>) 0, {hdr.ipv4.src}, 32w15);
	_tcpbloom_register_1.read(_tcpbloom_result_1uid4, _tcpbloom_hash_1uid2);
	sample_random = 0;
	if (_tcpbloom_result_1uid4 > 0){
		sample_random = 1;
	};
	hdr.genhdr_uid12.setInvalid();
	#undef OUTPUT_HEADER_SIZE
}
