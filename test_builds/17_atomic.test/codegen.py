import sys
sys.path.append('../../src/')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.core.commands import *  
from p4rrot.core.stateful import *  
from p4rrot.v1model.commands import *
from p4rrot.v1model.stateful import *
    
UID.reset()
fp = FlowProcessor(
        istruct=[('a',uint64_t)],
        locals=[('tmp',uint64_t)],
        state=[SharedVariable('cnt',uint64_t)]
    )

fp\
.add(AssignConst('a',0))\
.add(Atomic())\
        .add(ReadFromShared('tmp','cnt'))\
        .add(Increment('tmp',1))\
        .add(WriteToShared('cnt','tmp'))\
    .EndAtomic()\
.add(StrictAssignVar('a','tmp'))

fs = FlowSelector(
        'IPV4_UDP',
        [(UdpDstPort,5555)],
        fp
    )

solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump('test.p4app')
