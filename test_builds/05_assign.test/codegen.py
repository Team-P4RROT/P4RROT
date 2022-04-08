import sys
sys.path.append('../../src/')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.core.commands import *  
    
UID.reset()
fp = FlowProcessor(
        istruct=[('a',uint32_t),('b',uint64_t),('c',uint64_t)],
        ostruct=[('s',uint16_t),('x',bool_t),('y',bool_t)],
        mstruct=[('t',uint8_t)], 
        method='RESPOND'
    )

fp.add(AssignConst('a',5,env=fp.get_env()))
fp.add(AssignConst('b',0,env=fp.get_env()))
fp.add(AssignConst('s',10,env=fp.get_env()))
fp.add(AssignConst('t',110,env=fp.get_env()))
fp.add(StrictAssignVar('c','b',env=fp.get_env()))

fp.add(AssignConst('x',True,env=fp.get_env()))
fp.add(AssignConst('y',False,env=fp.get_env()))
fp.add(StrictAssignVar('y','x',env=fp.get_env()))


fs = FlowSelector(
        'IPV4_UDP',
        [(UdpDstPort,5555)],
        fp
    )

solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump('test.p4app')
