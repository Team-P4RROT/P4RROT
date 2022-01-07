import sys
sys.path.append('../../')

from generator_tools import *
from known_types import *  
from commands import *  
from stateful import *
    
UID.reset()
fp = FlowProcessor(
        istruct=[('guess',uint8_t)],
        mstruct=[('l',bool_t),('good',bool_t),('solution',uint8_t)],
        ostruct=[('r1',uint8_t),('r2',uint8_t)],
        state=[ SharedVariable('shared_solution',uint8_t) ]
    )

fp\
.add(Comment('init variables'))\
.add(ReadFromShared('solution','shared_solution'))\
.add(AssignConst('good',True))\
.add(AssignConst('r1',ord(':')))\
.add(AssignConst('r2',ord(')')))\
.add(Comment('check whether solution<guess'))\
.add(LessThan('l','solution','guess'))\
.add(If('l'))\
        .add(AssignConst('r1',ord('x')))\
        .add(AssignConst('r2',ord('<')))\
        .add(AssignConst('good',False))\
    .EndIf()\
.add(Comment('check whether solution>guess'))\
.add(GreaterThan('l','solution','guess'))\
.add(If('l'))\
        .add(AssignConst('r1',ord('x')))\
        .add(AssignConst('r2',ord('>')))\
        .add(AssignConst('good',False))\
    .EndIf()\
.add(Comment('generate a new number if required'))\
.add( If('good') )\
        .add(AssignRandomValue('solution',0,255))\
        .add(WriteToShared('shared_solution','solution'))\
    .EndIf()\
.add(Comment('send back the result'))\
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
