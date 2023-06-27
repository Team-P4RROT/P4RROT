import sys
sys.path.append('../../../src')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.standard_fields import *
from p4rrot.core.commands import *  

UID.reset()
fp = FlowProcessor(
        istruct = [('i_uint64', uint64_t)],
        locals = [('b', bool_t), ('cmp', uint64_t)],
        ostruct = [('o_uint64', uint64_t)]
    )



(
fp
.add(AssignConst('cmp', 0x4141414141414141))
.add(Equals('b', 'cmp', 'i_uint64'))
.add(If('b', fp.get_env(),
    then_block=Block(env=fp.get_env()).add(AssignConst('o_uint64', 0x4242424242424242)).add(SendBack()),
    else_block=Block(env=fp.get_env()).add(Drop())))  
)

fs = FlowSelector(
        'IPV4_UDP',
        # 8 becasue its the length of the UDP header, seems a little unnecessary
        # for me or at least mythic to put a 8 there and not some sort of constant
        [(UdpDstPort,5555), (UdpLen,8+ hdr_len(fp.istruct))],
        fp
    )

solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump('template')
