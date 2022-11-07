import sys

sys.path.append("../../src/")

from p4rrot.generator_tools import *
from p4rrot.known_types import *
from p4rrot.core.commands import *
from p4rrot.v1model.commands import *
from p4rrot.v1model.stateful import *
from p4rrot.tcp_fields import *

PERCENT_TO_SAMPLE = 10

UID.reset()
fp = FlowProcessor(
    istruct=[],
    helpers=[("fingerprint", bool_t), ("SYN_FLAG", uint6_t), ("SYN_AND_URG_FLAG", uint6_t), ("SYN_AND_PSH_FLAG", uint6_t), ("SYN_PSH_URG_FLAG", uint6_t),
        ("equals_var", bool_t), ("binary_search_run", bool_t), ("binary_search_lo", uint16_t), ("binary_search_hi", uint16_t), ("binary_search_mid", uint16_t),
        ("binary_search_lo_mss", uint16_t), ("binary_search_hi_mss", uint16_t), ("binary_search_mid_mss", uint16_t), ("window_smaller_than_mss", bool_t),
        ("window_greater_than_mss", bool_t), ("wsize_div_mss", uint16_t), ("window_equals_lo_mss", bool_t), ("window_equals_hi_mss", bool_t), ("window_equals_mid_mss", bool_t),
        ("random_number", uint8_t), ("percent_to_sample", uint8_t), ("sample_random", bool_t), ("signature_result", uint32_t), ("is_generic_fuzzy", bool_t), ("drop_ip", bool_t),
        ("drop_pkt", bool_t), ("redirect_to", uint32_t), ("sample_SYN", bool_t), ("not_generic_fuzzy", bool_t), ("MAX_OS_LABELS", uint32_t), ("MAX_OS_LABELS_minus_one", uint32_t),
        ("seq_no_plus_one", uint32_t),("PORT_TO_SAMPLE", uint16_t), ("equals_port_to_sample", bool_t), ("present_in_bloom", bool_t), ("quirk_df", bool_t), ("quirk_nz_id_a", bool_t),
        ("quirk_nz_id_b", bool_t), ("quirk_nz_id", bool_t), ("quirk_zero_id", bool_t), ("quirk_ecn_b", bool_t), ("quirk_ecn", bool_t), ("quirk_nz_mbz", bool_t),
        ("quirk_nz_ack", bool_t), ("quirk_nz_ack_b", bool_t), ("zero", uint32_t), ("quirk_zero_ack", bool_t), ("quirk_nz_urg", bool_t), ("urg_ptr", bool_t),
        ("quirk_urg", bool_t), ("pclass", bool_t), ("ip_header_length", uint32_t), ("payload_length", uint32_t), ("tcp_offset_long", uint32_t), ("CONST_TO_SUBTRACT", uint32_t),
        ("should_redirect", bool_t), ("os_counter_holder", uint32_t)],
    mstruct=[],
    state=[ GeneralBloomFilter('tcpbloom',uint32_t, 1000, 3), GeneralBloomFilter('httpbloom',uint32_t, 1000, 3), SharedArray("os_counters", uint32_t, 1024) ],
    standard_fields = [TCPCtrl, TCPWindow, IPv4Version, Ipv4TTL, IPv4IHL, SrcIp, DstIp, TcpDstPort, TcpSrcPort, TCPSeqNo, TCPOlen, TCPMss, TCPScale, TCPOlayout, MetaIPForward,
    IPFlags, IPIdentification, IPDiffserv, TCPEcn, TCPAckNo, TCPUrgentPtr, TCPOptZeroTs_1, TCPOptNZTs_2, TCPOptEolNz, TCPQuirkOptExws],
)
(
fp
.add(AssignConst("percent_to_sample", 10))
.add(AssignConst("MAX_OS_LABELS", 1024))
.add(AssignConst("MAX_OS_LABELS_minus_one", 1023))
.add(AssignConst("PORT_TO_SAMPLE", 80))
.add(AssignConst("SYN_FLAG", 1 << 1))
.add(AssignConst("SYN_AND_PSH_FLAG", 1 << 3 | 1 << 1))
.add(AssignConst("SYN_AND_URG_FLAG", 1 << 5 | 1 << 1))
.add(AssignConst("SYN_PSH_URG_FLAG", 1 << 5 | 1 << 3 | 1 << 1))
.add(Equals("fingerprint", "hdr.tcp.ctrl", "SYN_FLAG"))
.add(Equals("equals_var", "hdr.tcp.ctrl", "SYN_AND_URG_FLAG"))
.add(LogicalOr("fingerprint", "equals_var", "fingerprint"))
.add(Equals("equals_var", "hdr.tcp.ctrl", "SYN_AND_PSH_FLAG"))
.add(LogicalOr("fingerprint", "equals_var", "fingerprint"))
.add(Equals("equals_var", "hdr.tcp.ctrl", "SYN_PSH_URG_FLAG"))
.add(LogicalOr("fingerprint", "equals_var", "fingerprint"))
.add(AssignConst("binary_search_run",1))
.add(AssignConst("binary_search_hi",64))
.add(AssignConst("binary_search_lo",0))
.add(AssignConst("binary_search_lo_mss",0))
.add(StrictAssignVar("binary_search_hi_mss", "meta.tcp_metadata.mss"))
.add(LeftShift("binary_search_hi_mss",6))
)
tb = fp.add(If("fingerprint"))
for i in range(4):
    (
    tb
        .add(If("binary_search_run"))
            .add(StrictAddition("binary_search_mid", "binary_search_hi", "binary_search_lo"))
            .add(RightShift("binary_search_mid", 1))
            .add(StrictAddition("binary_search_mid_mss", "binary_search_hi_mss", "binary_search_lo_mss"))
            .add(RightShift("binary_search_mid_mss", 1))
            .add(LessThan("window_smaller_than_mss", "hdr.tcp.window", "binary_search_mid_mss"))
            .add(If("window_smaller_than_mss"))
                .add(StrictAssignVar("binary_search_hi", "binary_search_mid"))
                .add(StrictAssignVar("binary_search_hi_mss", "binary_search_mid_mss"))
            .Else()
                .add(GreaterThan("window_greater_than_mss", "hdr.tcp.window", "binary_search_mid_mss"))
                .add(If("window_greater_than_mss"))
                    .add(StrictAssignVar("binary_search_lo", "binary_search_mid"))
                    .add(StrictAssignVar("binary_search_lo_mss", "binary_search_mid_mss"))
                .Else()
                    .add(StrictAssignVar("wsize_div_mss", "binary_search_mid_mss"))
                    .add(AssignConst("binary_search_run", 0))
            .EndIf()
        .EndIf()
    )
(
fp
    .add(If("binary_search_run"))
        .add(StrictAddition("binary_search_mid", "binary_search_hi", "binary_search_lo"))
        .add(RightShift("binary_search_mid", 1))
        .add(StrictAddition("binary_search_mid_mss", "binary_search_hi_mss", "binary_search_lo_mss"))
        .add(RightShift("binary_search_mid_mss", 1))
        .add(Equals("window_equals_lo_mss", "hdr.tcp.window", "binary_search_lo_mss"))
        .add(If("window_equals_lo_mss"))
            .add(StrictAssignVar("wsize_div_mss", "binary_search_lo"))
        .Else()
            .add(Equals("window_equals_hi_mss", "hdr.tcp.window", "binary_search_hi_mss"))
            .add(If("window_equals_hi_mss"))
                .add(StrictAssignVar("wsize_div_mss", "binary_search_hi"))
            .Else()
                .add(Equals("window_equals_mid_mss", "hdr.tcp.window", "binary_search_mid_mss"))
                .add(If("window_equals_mid_mss"))
                    .add(StrictAssignVar("wsize_div_mss", "binary_search_mid"))
                .Else()
                    .add(AssignConst("wsize_div_mss",0))
                .EndIf()
        .EndIf()
    .EndIf()
    
    .add(AssignConst("signature_result", 1023))
    .add(AssignConst("CONST_TO_SUBTRACT", 34))
    .add(AssignConst("is_generic_fuzzy", 0))
    .add(AssignConst("drop_ip", 0))
    .add(AssignConst("drop_pkt", 0))
    .add(AssignConst("redirect_to", 0))
    .add(MaskedNotEqualsConst("quirk_nz_id_a", "hdr.ipv4.flags", 2, 0))
    .add(MaskedNotEqualsConst("quirk_df", "hdr.ipv4.flags", 2, 0))
    .add(MaskedNotEqualsConst("quirk_nz_id_b", "hdr.ipv4.identification", 2, 0))
    .add(LogicalAnd("quirk_nz_id", "quirk_nz_id_a", "quirk_nz_id_b"))
    .add(MaskedEqualsConst("quirk_nz_id_a", "hdr.ipv4.flags", 2, 0))
    .add(MaskedEqualsConst("quirk_nz_id_b", "hdr.ipv4.identification", 2, 0))
    .add(LogicalAnd("quirk_zero_id", "quirk_nz_id_a", "quirk_nz_id_b"))
    .add(MaskedNotEqualsConst("quirk_ecn", "hdr.ipv4.diffserv", 3, 0))
    .add(MaskedNotEqualsConst("quirk_ecn_b", "hdr.tcp.ecn", 7, 0))
    .add(LogicalOr("quirk_ecn", "quirk_ecn", "quirk_ecn_b"))
    .add(MaskedNotEqualsConst("quirk_nz_mbz", "hdr.ipv4.flags", 4, 0))
    .add(MaskedEqualsConst("quirk_nz_ack", "hdr.tcp.ctrl", 20, 0))
    .add(EqualsConst("quirk_nz_urg","hdr.tcp.urgentPtr", 0))
    .add(LogicalNot("quirk_nz_urg"))
    .add(LogicalAnd("quirk_nz_urg", "quirk_nz_urg", "quirk_nz_ack"))
    .add(EqualsConst("quirk_nz_ack_b", "hdr.tcp.ackNo", 0))
    .add(MaskedNotEqualsConst("quirk_zero_ack", "hdr.tcp.ctrl", 16, 0))
    .add(LogicalAnd("quirk_zero_ack", "quirk_zero_ack", "quirk_nz_ack_b"))
    .add(LogicalNot("quirk_nz_ack_b"))
    .add(LogicalAnd("quirk_nz_ack", "quirk_nz_ack", "quirk_nz_ack_b"))
    .add(MaskedNotEqualsConst("quirk_urg", "hdr.tcp.ctrl", 20, 0))
    .add(CastVar("ip_header_length", "meta.tcp_metadata.olen"))
    .add(GetPacketLength("payload_length"))
    .add(CastVar("tcp_offset_long","meta.tcp_metadata.olen"))
    .add(LeftShift("tcp_offset_long",2))
    .add(StrictSubtraction("payload_length", "payload_length", "tcp_offset_long"))
    .add(StrictSubtraction("payload_length", "payload_length", "ip_header_length"))
    .add(StrictSubtraction("payload_length", "payload_length", "CONST_TO_SUBTRACT"))    #subtract eth header length and part of ip header length in one step
    .add(EqualsConst("pclass", "payload_length", 0))
    .add(LogicalNot("pclass"))
    .add(ReadFromControlPlaneSet([{"name":"hdr.ipv4.version", "match_type":"ternary"}, {"name":"hdr.ipv4.ttl", "match_type":"range"},
    {"name":"meta.tcp_metadata.olen", "match_type":"exact"}, {"name":"meta.tcp_metadata.mss", "match_type":"ternary"},
    {"name":"hdr.tcp.window", "match_type":"ternary"}, {"name":"wsize_div_mss", "match_type":"ternary"}, {"name":"meta.tcp_metadata.scale", "match_type":"ternary"},
    {"name":"meta.tcp_metadata.olayout", "match_type":"exact"}, {"name":"quirk_df", "match_type":"ternary"}, {"name":"quirk_nz_id", "match_type":"ternary"},
    {"name":"quirk_zero_id", "match_type":"ternary"}, {"name":"quirk_ecn", "match_type":"ternary"}, {"name":"quirk_nz_mbz", "match_type":"exact"},
    {"name":"hdr.tcp.seqNo", "match_type":"exact"}, {"name":"quirk_nz_ack", "match_type":"exact"}, {"name":"quirk_zero_ack", "match_type":"exact"},
    {"name":"quirk_nz_urg", "match_type":"exact"}, {"name":"quirk_urg", "match_type":"exact"}, {"name":"meta.tcp_metadata.quirk_opt_zero_ts1", "match_type":"exact"},
    {"name":"meta.tcp_metadata.quirk_opt_nz_ts2", "match_type":"exact"}, {"name":"meta.tcp_metadata.quirk_opt_eol_nz", "match_type":"exact"},
    {"name":"meta.tcp_metadata.quirk_opt_exws", "match_type":"exact"}, {"name":"pclass", "match_type":"ternary"}
    ], ["signature_result", "is_generic_fuzzy", "drop_ip", "drop_pkt", "should_redirect", "redirect_to"]))
    .add(ReadFromSharedAt("os_counter_holder", "os_counters", "signature_result"))
    .add(Increment("os_counter_holder", 1))
    .add(WriteToSharedAt("os_counters", "signature_result", "os_counter_holder"))
    .add(If("drop_pkt"))
        .add(AssignConst("meta.tcp_metadata.ip_forward", 0))
    .EndIf()
    .add(If("drop_ip"))
        .add(GeneralPutIntoBloom("tcpbloom", ["hdr.ipv4.src"]))
    .EndIf()
    .add(If("should_redirect"))
        .add(StrictAssignVar("hdr.ipv4.dst", "redirect_to"))
    .EndIf()
    .add(AssignRandomValue("random_number", 0, 100))
    .add(Equals("equals_port_to_sample", "hdr.tcp.dstPort", "PORT_TO_SAMPLE"))
    .add(LessThan("sample_random", "random_number", "percent_to_sample"))
    .add(Equals("sample_SYN", "signature_result", "MAX_OS_LABELS_minus_one"))
    .add(StrictAssignVar("not_generic_fuzzy", "is_generic_fuzzy"))
    .add(LogicalNot("not_generic_fuzzy"))
    .add(LogicalOr("sample_SYN", "sample_SYN", "not_generic_fuzzy"))
    .add(LogicalOr("sample_SYN", "sample_SYN", "sample_random"))
    .add(LogicalAnd("sample_SYN", "sample_SYN", "equals_port_to_sample"))
    .add(If("sample_SYN"))
        .add(ClonePacket(250))
        .add(GeneralPutIntoBloom("httpbloom", ["hdr.ipv4.src", "hdr.ipv4.dst","hdr.tcp.srcPort", "hdr.tcp.seqNo"]))
    .EndIf()
.EndIf()
.add(If("equals_port_to_sample"))
    .add(StrictAssignVar("seq_no_plus_one","hdr.tcp.seqNo"))
    .add(Increment("seq_no_plus_one", 1))
    .add(GeneralMaybeContains("present_in_bloom", "httpbloom", ["hdr.ipv4.src", "hdr.ipv4.dst","hdr.tcp.srcPort", "seq_no_plus_one"]))
    .add(If("present_in_bloom"))
        .add((ClonePacket(250)))
        .add(AssignConst("meta.tcp_metadata.ip_forward", 0))
    .EndIf()
.EndIf()
.add(GeneralMaybeContains("sample_random", "tcpbloom", ["hdr.ipv4.src"]))
)
fs = FlowSelector("IPV4_TCP", [], fp)

solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump("test.p4app")
