import sys
sys.path.append('../../src/')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.core.commands import *  
    
UID.reset()
fp = FlowProcessor(
        istruct=[('a',uint32_t),('b',uint8_t)],
    )

fp.add(AssignConst('b',ord('\n')))\
    .add(TruncateRemainng())
   
fs = FlowSelector(
        'IPV4_UDP',
        [(UdpDstPort,5555)],
        fp
    )

solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump('test.p4app')
