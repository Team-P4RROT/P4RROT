import sys
sys.path.append('../../src/')

from p4rrot.generator_tools import *
from p4rrot.known_types import *    
    
UID.reset()
fp = FlowProcessor(
        istruct=[('a',uint32_t),('b',uint32_t)],
        ostruct=[('s',uint32_t)],
        mstruct=[('t',uint32_t)],    
        method='RESPOND'
    )

fp2 = FlowProcessor(
        istruct=[('a',uint32_t),('b',uint32_t)],
        mstruct=[('t',uint32_t)],    
        method='READ'
    )

fs = FlowSelector(
        'IPV4_UDP',
        [(UdpDstPort,5555),(SrcIp,0x0a00000a)],
        fp
    )

fs2 = FlowSelector(
        'IPV4_UDP',
        [(UdpDstPort,5555),(SrcIp,0x0a00000b)],
        fp
    )

fs3 = FlowSelector(
        'IPV4_TCP',
        [(TcpDstPort,7777),(SrcIp,0x0a00000c),('msg_type',110)],
        fp2,
        lookahead_struct=[('msg_type',uint8_t)]
    )


solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_processor(fp2)
solution.add_flow_selector(fs)
solution.add_flow_selector(fs2)
solution.add_flow_selector(fs3)

solution.get_generated_code().dump('test.p4app')
