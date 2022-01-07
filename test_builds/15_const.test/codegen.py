import sys
sys.path.append('../../')

from generator_tools import *
from known_types import *  
from commands import *  
from stateful import *  
    
UID.reset()
fp = FlowProcessor(
        istruct=[('a',uint32_t),('b',uint32_t),('op',uint8_t)],
        locals=[('l',bool_t)],
        ostruct=[('r',uint32_t)],
        state=[Const('op_plus',uint8_t,ord('+')),Const('op_minus',uint8_t,ord('-'))]
    )

fp\
.add(Equals('l','op','op_plus'))\
.add(If('l'))\
          .add(StrictAddition('r','a','b'))\
     .EndIf()\
.add(Equals('l','op','op_minus'))\
.add(If('l'))\
          .add(StrictSubtraction('r','a','b'))\
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
