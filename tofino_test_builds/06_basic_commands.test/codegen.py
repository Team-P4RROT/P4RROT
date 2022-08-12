import sys
sys.path.append('../../src/')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.core.commands import *  
    
UID.reset()
fp = FlowProcessor(
        istruct=[('a',uint32_t),('b',uint32_t),('c',uint32_t),('d',uint32_t),('x',bool_t),('y',bool_t),('z',bool_t)],
        method='MODIFY'
    )

fp.add(Increment('a',5,env=fp.get_env()))
fp.add(Decrement('b',5,env=fp.get_env()))
fp.add(StrictAddition('c','a','b',env=fp.get_env()))
fp.add(StrictSubtraction('d','a','b',env=fp.get_env()))

fp.add(LogicalAnd('z','x','y',env=fp.get_env()))
fp.add(LogicalOr('z','x','y',env=fp.get_env()))
#Stuff that doesn't compile
#fp.add(LogicalNot('z',env=fp.get_env()))

#fp.add(GreaterThan('x','a','b',env=fp.get_env()))
#fp.add(LessThan('y','a','b',env=fp.get_env()))
#fp.add(Equals('z','a','b',env=fp.get_env()))


fs = FlowSelector(
        'IPV4_UDP',
        [(UdpDstPort,5555)],
        fp
    )

solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
script_dir = os.path.dirname(__file__)
dir_path = os.path.join(script_dir, "result.p4app")
solution.get_generated_code().dump('result.p4app')
