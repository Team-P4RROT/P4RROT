import sys
sys.path.append('../../../src')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.standard_fields import *
from p4rrot.core.commands import *  

UID.reset()
fp = FlowProcessor(
        istruct = [('uint8_i', uint8_t)],
        ostruct = [('uint64', uint64_t),('uint32',uint32_t), ('uint16', uint16_t), ('uint8', uint8_t)]
    )



(
fp
.add(AssignConst('uint64',0x4141414142424242))
.add(AssignConst('uint32',0x45454545))
.add(AssignConst('uint16',0x4646))
.add(AssignConst('uint8',0x47))
.add(SendBack())
)  



fs = FlowSelector(
        'IPV4_UDP',
        [(UdpDstPort,5555)],
        fp
    )


solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump('template')
