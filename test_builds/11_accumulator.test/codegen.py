import sys
sys.path.append('../../src/')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.core.commands import *  
from p4rrot.core.stateful import *
from p4rrot.v1model.commands import *
from p4rrot.v1model.stateful import *
    
UID.reset()

counter = SharedVariable('c',uint32_t)

fp = FlowProcessor(
        istruct=[('v',uint32_t)],
        mstruct=[('x',uint32_t)],
        ostruct=[('s',uint32_t)],
        state=[counter]
    )

fp\
.add(ReadFromShared('x','c'))\
.add(StrictAddition('s','x','v'))\
.add(WriteToShared('c','s'))\
.add(SendBack())
   

fs = FlowSelector(
        'IPV4_UDP',
        [(UdpDstPort,5555)],
        fp
    )

solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump('test.p4app')
