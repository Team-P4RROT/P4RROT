import sys
sys.path.append('../../../src')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.standard_fields import *
from p4rrot.core.commands import *  

UID.reset()
fp = FlowProcessor(
        istruct = [('i_uint64', uint64_t),('i_uint32',uint32_t), ('i_uint16', uint16_t), ('i_uint8', uint8_t)],
        ostruct = [('o_uint64', uint64_t),('o_uint32',uint32_t), ('o_uint16', uint16_t), ('o_uint8', uint8_t)]
    )



(
fp
.add(Decrement('i_uint64', 1))
.add(Decrement('i_uint32', 2))
.add(Decrement('i_uint16', 3))
.add(Decrement('i_uint8', 31))
.add(StrictAssignVar('o_uint64', 'i_uint64'))
.add(StrictAssignVar('o_uint32', 'i_uint32'))
.add(StrictAssignVar('o_uint16', 'i_uint16'))
.add(StrictAssignVar('o_uint8', 'i_uint8'))
.add(SendBack())
)  



fs = FlowSelector(
        'IPV4_UDP',
        # 8 becasue its the length of the UDP header, seems a little unnecessary
        # for me or at least mythic to put a 8 there and not some sort of constant
        [(UdpDstPort,5555), (UdpLen,8+ hdr_len(fp.istruct) )],
        fp
    )


solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump('template')