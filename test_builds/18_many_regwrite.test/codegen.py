import sys
sys.path.append('../../src/')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.core.commands import *  
from p4rrot.core.stateful import *
    
UID.reset()

msgbox = SharedArray('msgbox',uint64_t,10)

fp = FlowProcessor(
        istruct=[('_pad',padding_t(1))],
        locals=[('tmp',uint64_t),('index',uint32_t)],
        state=[msgbox]
    )

for i in range(10):
    fp.add(AssignConst('index',i))
    fp.add(ReadFromSharedAt('tmp','msgbox','index'))
    fp.add(Increment('tmp',1))
    fp.add(WriteToSharedAt('msgbox','index','tmp'))
    for k in range(10):
        fp.add(Increment('tmp',k+1))

fs = FlowSelector(
        'IPV4_UDP',
        [(UdpDstPort,5001)],
        fp
    )

solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump('test.p4app')
