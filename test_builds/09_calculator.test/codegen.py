import sys
sys.path.append('../../src/')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.core.commands import *  
    
UID.reset()
fp = FlowProcessor(
        istruct=[('a',uint32_t),('b',uint32_t),('op',uint8_t)],
        mstruct=[('l',bool_t),('c',uint8_t)],
        ostruct=[('r',uint32_t)]
    )

fp\
.add(AssignConst('c',ord('+')))\
.add(Equals('l','op','c'))\
.add(If('l'))\
          .add(StrictAddition('r','a','b'))\
     .EndIf()\
.add(AssignConst('c',ord('-')))\
.add(Equals('l','op','c'))\
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
