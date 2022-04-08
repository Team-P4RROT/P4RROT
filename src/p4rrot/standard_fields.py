#
# Classes and constant objects representing standard fields like udp sourc port and destination ip.
#

from p4rrot.known_types import *

class StandardField:
    
    def __init__(self,handle:str,ftype:KnownType):
        self.handle = handle
        self.ftype = ftype
    
    def get_handle(self):
        return self.handle
    
    def get_type(self):
        return self.ftype
    
SrcIp = StandardField('hdr.ipv4.src',uint32_t)
DstIp = StandardField('hdr.ipv4.dst',uint32_t)
UdpSrcPort = StandardField('hdr.udp.srcPort',uint16_t)
UdpDstPort = StandardField('hdr.udp.dstPort',uint16_t)
TcpSrcPort = StandardField('hdr.tcp.srcPort',uint16_t)
TcpDstPort = StandardField('hdr.tcp.dstPort',uint16_t)

Ipv4TTL = StandardField('hdr.ipv4.ttl',uint8_t)
Ipv4Protocol = StandardField('hdr.ipv4.protocol',uint8_t)
Ipv4TotalLen = StandardField('hdr.ipv4.totalLen',uint16_t)

UdpLen = StandardField('hdr.udp.len',uint16_t)