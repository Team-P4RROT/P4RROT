import sys
sys.path.append('../../')

from generator_tools import *
from known_types import *  
from commands import *  
from stateful import *
    
UID.reset()

msgbox = SharedArray('msgbox',uint32_t,6)

fp = FlowProcessor(
        istruct=[('value',uint32_t),('index',uint32_t),('op',uint32_t)],
        mstruct=[('op_guess',uint32_t),('b',bool_t)],
        ostruct=[('response',uint32_t)],
        state=[msgbox]
    )

fp\
.add(AssignConst('op_guess',1))\
.add(Equals('b','op','op_guess'))\
.add(If('b'))\
    .add(ReadFromSharedAt('response','msgbox','index'))\
.EndIf()\
.add(AssignConst('op_guess',2))\
.add(Equals('b','op','op_guess'))\
.add(If('b'))\
    .add(WriteToSharedAt('msgbox','index','value'))\
    .add(StrictAssignVar('response','value'))\
.EndIf()\
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
