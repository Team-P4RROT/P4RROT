#pragma netro reglocked register
register< bit<32> >(1000) _tcpbloom_register_1;
bit<32> _tcpbloom_value_checkuid1;
bit<32> _tcpbloom_hash_1uid2;
bit<32> _tcpbloom_result_1uid4;
#pragma netro reglocked register
register< bit<32> >(1000) _httpbloom_register_1;
bit<32> _httpbloom_value_checkuid6;
bit<32> _httpbloom_hash_1uid7;
bit<32> _httpbloom_result_1uid9;
#pragma netro reglocked register
register< bit<32> >(1024) os_counters;
BOOL_T fingerprint;
bit<6> SYN_FLAG;
bit<6> SYN_AND_URG_FLAG;
bit<6> SYN_AND_PSH_FLAG;
bit<6> SYN_PSH_URG_FLAG;
BOOL_T equals_var;
BOOL_T binary_search_run;
bit<16> binary_search_lo;
bit<16> binary_search_hi;
bit<16> binary_search_mid;
bit<16> binary_search_lo_mss;
bit<16> binary_search_hi_mss;
bit<16> binary_search_mid_mss;
BOOL_T window_smaller_than_mss;
BOOL_T window_greater_than_mss;
bit<16> wsize_div_mss;
BOOL_T window_equals_lo_mss;
BOOL_T window_equals_hi_mss;
BOOL_T window_equals_mid_mss;
bit<8> random_number;
bit<8> percent_to_sample;
BOOL_T sample_random;
bit<32> signature_result;
BOOL_T is_generic_fuzzy;
BOOL_T drop_ip;
BOOL_T drop_pkt;
bit<32> redirect_to;
BOOL_T sample_SYN;
BOOL_T not_generic_fuzzy;
bit<32> MAX_OS_LABELS;
bit<32> MAX_OS_LABELS_minus_one;
bit<32> seq_no_plus_one;
bit<16> PORT_TO_SAMPLE;
BOOL_T equals_port_to_sample;
BOOL_T present_in_bloom;
BOOL_T quirk_df;
BOOL_T quirk_nz_id_a;
BOOL_T quirk_nz_id_b;
BOOL_T quirk_nz_id;
BOOL_T quirk_zero_id;
BOOL_T quirk_ecn_b;
BOOL_T quirk_ecn;
BOOL_T quirk_nz_mbz;
BOOL_T quirk_nz_ack;
BOOL_T quirk_nz_ack_b;
bit<32> zero;
BOOL_T quirk_zero_ack;
BOOL_T quirk_nz_urg;
BOOL_T urg_ptr;
BOOL_T quirk_urg;
BOOL_T pclass;
bit<32> ip_header_length;
bit<32> payload_length;
bit<32> tcp_offset_long;
bit<32> CONST_TO_SUBTRACT;
BOOL_T should_redirect;
bit<32> os_counter_holder;
action setter_action_uid14(bit<32>  paramuid15,BOOL_T  paramuid16,BOOL_T  paramuid17,BOOL_T  paramuid18,BOOL_T  paramuid19,bit<32>  paramuid20) {
	signature_result = paramuid15;
	is_generic_fuzzy = paramuid16;
	drop_ip = paramuid17;
	drop_pkt = paramuid18;
	should_redirect = paramuid19;
	redirect_to = paramuid20;
}
table control_plane_set_table_uid13 {
	key = {
		hdr.ipv4.version: ternary;
		hdr.ipv4.ttl: range;
		meta.tcp_metadata.olen: exact;
		meta.tcp_metadata.mss: ternary;
		hdr.tcp.window: ternary;
		wsize_div_mss: ternary;
		meta.tcp_metadata.scale: ternary;
		meta.tcp_metadata.olayout: exact;
		quirk_df: ternary;
		quirk_nz_id: ternary;
		quirk_zero_id: ternary;
		quirk_ecn: ternary;
		quirk_nz_mbz: exact;
		hdr.tcp.seqNo: exact;
		quirk_nz_ack: exact;
		quirk_zero_ack: exact;
		quirk_nz_urg: exact;
		quirk_urg: exact;
		meta.tcp_metadata.quirk_opt_zero_ts1: exact;
		meta.tcp_metadata.quirk_opt_nz_ts2: exact;
		meta.tcp_metadata.quirk_opt_eol_nz: exact;
		meta.tcp_metadata.quirk_opt_exws: exact;
		pclass: ternary;
	}
	actions = {
		setter_action_uid14;
	}
	size = 1;
}
