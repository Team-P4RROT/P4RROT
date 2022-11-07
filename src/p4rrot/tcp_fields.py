#
# Classes and constant objects representing standard fields like udp sourc port and destination ip.
#

from p4rrot.known_types import *
from p4rrot.standard_fields import *


class uint4_t(KnownType):
    def get_p4_type() -> str:
        return "bit<4>"

    def get_size() -> int:
        return 1

    def to_p4_literal(v):
        return str(uint4_t.cast_value(v))

    def cast_value(v):
        if type(v) == int:
            return ctypes.c_uint4(v).value
        raise Exception("Can not recignize value {}".format(v))


class uint6_t(KnownType):
    def get_p4_type() -> str:
        return "bit<6>"

    def get_size() -> int:
        return 1

    def to_p4_literal(v):
        return str(uint6_t.cast_value(v))

    def cast_value(v):
        if type(v) == int:
            return v % 2 ** 6
        raise Exception("Can not recignize value {}".format(v))


class uint9_t(KnownType):
    def get_p4_type() -> str:
        return "bit<9>"

    def get_size() -> int:
        return 1

    def to_p4_literal(v):
        return str(uint6_t.cast_value(v))

    def cast_value(v):
        if type(v) == int:
            return v % 2 ** 9
        raise Exception("Can not recignize value {}".format(v))


class uint3_t(KnownType):
    def get_p4_type() -> str:
        return "bit<3>"

    def get_size() -> int:
        return 1

    def to_p4_literal(v):
        return str(uint3_t.cast_value(v))

    def cast_value(v):
        if type(v) == int:
            return ctypes.c_uint3(v).value
        raise Exception("Can not recignize value {}".format(v))


class uint160_t(KnownType):
    def get_p4_type() -> str:
        return "bit<160>"

    def get_size() -> int:
        return 1

    def to_p4_literal(v):
        return str(uint160_t.cast_value(v))

    def cast_value(v):
        if type(v) == int:
            return v  # int is 32 bit long, so there is no point in using the modulo operation here
        raise Exception("Can not recignize value {}".format(v))


TCPWindow = StandardField("hdr.tcp.window", uint16_t)
TCPSeqNo = StandardField("hdr.tcp.seqNo", uint32_t)
TCPAckNo = StandardField("hdr.tcp.ackNo", uint32_t)
TCPDataOffset = StandardField("hdr.tcp.dataOffset", uint4_t)
TCPRes = StandardField("hdr.tcp.res", uint3_t)
TCPEcn = StandardField("hdr.tcp.ecn", uint3_t)
TCPCtrl = StandardField("hdr.tcp.ctrl", uint6_t)
TCPChecksum = StandardField("hdr.tcp.checksum", uint16_t)
TCPUrgentPtr = StandardField("hdr.tcp.urgentPtr", uint16_t)
TCPOlen = StandardField("meta.tcp_metadata.olen", uint9_t)
TCPMss = StandardField("meta.tcp_metadata.mss", uint16_t)
TCPScale = StandardField("meta.tcp_metadata.scale", uint8_t)
TCPOlayout = StandardField("meta.tcp_metadata.olayout", uint160_t)
IPFlags = StandardField("hdr.ipv4.flags", uint3_t)
IPIdentification = StandardField("hdr.ipv4.identification", uint16_t)
IPDiffserv = StandardField("hdr.ipv4.diffserv", uint8_t)
TCPOptZeroTs_1 = StandardField("meta.tcp_metadata.quirk_opt_zero_ts1", bool_t)
TCPOptNZTs_2 = StandardField("meta.tcp_metadata.quirk_opt_nz_ts2", bool_t)
TCPOptEolNz = StandardField("meta.tcp_metadata.quirk_opt_eol_nz", bool_t)
TCPQuirkOptExws = StandardField("meta.tcp_metadata.quirk_opt_exws", bool_t)
MetaIPForward = StandardField("meta.tcp_metadata.ip_forward", bool_t)

IPv4Version = StandardField("hdr.ipv4.version", uint4_t)
IPv4IHL = StandardField("hdr.ipv4.ihl", uint4_t)
