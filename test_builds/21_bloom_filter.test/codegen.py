import sys
sys.path.append('../../')
from stateful import Const, BloomFilter, MaybeContains, PutIntoBloom


from generator_tools import *
from known_types import *  
from commands import *  
    
UID.reset()
fp = FlowProcessor(
        istruct=[('op', uint8_t), ('x',uint32_t)],
        ostruct=[('contains', bool_t), ('err', bool_t)],
        locals=[('comp_res',bool_t), ('operation', uint8_t)],
        state=[ BloomFilter('mybloom',uint32_t, 1000, 3) ]
    )

fp\
.add(AssignConst('operation', ord('a'))) \
.add(Equals('comp_res', 'op', 'operation')) \
.add(If('comp_res')) \
    .add(PutIntoBloom('mybloom', 'x')) \
.EndIf() \
.add(AssignConst('operation',ord('c')))\
.add(Equals('comp_res', 'op', 'operation')) \
.add(If('comp_res')) \
    .add(MaybeContains('contains', 'mybloom', 'x')) \
    .EndIf() \
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
