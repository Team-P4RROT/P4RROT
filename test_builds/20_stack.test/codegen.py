import sys
sys.path.append('../../')
from stateful import PopFromStack, PushToStack, SharedStack


from generator_tools import *
from known_types import *  
from commands import *  
    
UID.reset()
fp = FlowProcessor(
        istruct=[('a',uint32_t), ('aa', uint32_t)],
        ostruct=[('b',uint32_t), ('bb', uint32_t)],
        state=[ SharedStack('shared_stack',uint32_t, 10) ]
    )

fp\
.add(PushToStack('shared_stack', 'a'))\
.add(PushToStack('shared_stack', 'aa'))\
.add(PopFromStack('shared_stack', 'b'))\
.add(PopFromStack('shared_stack', 'bb'))\
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
