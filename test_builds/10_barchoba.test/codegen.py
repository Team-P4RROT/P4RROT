import sys
sys.path.append('../../')

from generator_tools import *
from known_types import *  
from commands import *  
    
UID.reset()
fp = FlowProcessor(
        istruct=[('guess',uint32_t)],
        mstruct=[('l',bool_t),('solution',uint32_t)],
        ostruct=[('r1',uint8_t),('r2',uint8_t)]
    )

fp\
.add(AssignConst('solution',96))\
.add(AssignConst('r1',ord(':')))\
.add(AssignConst('r2',ord(')')))\
.add(LessThan('l','solution','guess'))\
.add(If('l'))\
        .add(AssignConst('r1',ord('x')))\
        .add(AssignConst('r2',ord('<')))\
    .EndIf()\
.add(GreaterThan('l','solution','guess'))\
.add(If('l'))\
        .add(AssignConst('r1',ord('x')))\
        .add(AssignConst('r2',ord('>')))\
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
