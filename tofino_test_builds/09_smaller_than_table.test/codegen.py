import sys
<<<<<<< Updated upstream
sys.path.append('../../')

from generator_tools import *
from known_types import *  
from commands import *  
=======
sys.path.append('../../src/')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.core.commands import * 
>>>>>>> Stashed changes
    
UID.reset()
fp = FlowProcessor(
        istruct=[('a',uint32_t),('b',uint32_t),('x',bool_t)],
        method='MODIFY'
    )

fp.add(AssignConst('x',True,env=fp.get_env()))
fp.add(SmallerThanTable('x','a','b',env=fp.get_env()))
fp.add(If('x',env=fp.get_env()
        ,then_block=Block(env=fp.get_env()).add(Increment('a',5,env=fp.get_env()))
        ,else_block=Block(env=fp.get_env()).add(Decrement('a',5,env=fp.get_env()))
        )
   )

fs = FlowSelector(
        'IPV4_UDP',
        [(UdpDstPort,5555)],
        fp
    )

solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump('test.p4app')
