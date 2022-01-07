import sys
sys.path.append('../../')

from generator_tools import *
from known_types import *    
    
UID.reset()
fp = FlowProcessor(
        istruct=[('a',uint32_t),('b',uint32_t)],
        ostruct=[('s',uint32_t)],
        mstruct=[('t',uint32_t)],    
        method='RESPOND'
    )
gc = fp.get_generated_code()
gc.dump('./test.p4app')
