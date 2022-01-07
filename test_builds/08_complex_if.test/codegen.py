import sys
sys.path.append('../../')

from generator_tools import *
from known_types import *  
from commands import *  
    
UID.reset()
fp = FlowProcessor(
        istruct=[('a',uint32_t),('b',uint32_t),('x',bool_t)],
        method='MODIFY'
    )

fp.add(GreaterThan('x','a','b'))\
  .add(If('x'))\
            .add(Increment('a',5))\
            .add(Increment('a',5))\
       .Else()\
            .add(Decrement('a',6))\
            .add(Decrement('a',6))\
       .EndIf()\
  .add(Increment('a',7))\
  .add(If('x'))\
            .add(Increment('a',5))\
            .add(Increment('a',5))\
            .add(If('x'))\
                .add(Increment('a',9))\
                .add(SendBack())\
            .EndIf()\
       .Else()\
            .add(Decrement('a',6))\
            .add(Decrement('a',6))\
       .EndIf()\
   

fs = FlowSelector(
        'IPV4_UDP',
        [(UdpDstPort,5555)],
        fp
    )

solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump('test.p4app')
