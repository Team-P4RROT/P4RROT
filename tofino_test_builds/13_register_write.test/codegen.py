import sys
sys.path.append('../../src/')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.core.commands import *  
from p4rrot.core.stateful import *
from p4rrot.tofino.commands import *
from p4rrot.tofino.stateful import *
    
UID.reset()

msgbox_a = SharedArray('msgbox_a',uint64_t,uint64_t,10)
msgbox_b = SharedArray('msgbox_b',uint64_t,uint64_t,10)

fp = FlowProcessor(
        istruct=[],
        locals=[('tmp',uint64_t)],
        state=[msgbox_a, msgbox_b]
    )

fp.add(ReadSharedArray('msgbox_a', uint64_t, uint64_t, 1, 'tmp', env=fp.get_env()))
fp.add(Increment('tmp',1))
fp.add(WriteSharedArray('msgbox_b', uint64_t, uint64_t, 1, 'tmp', env=fp.get_env()))

fs = FlowSelector("IPV4_UDP", [(UdpDstPort, 5555)], fp)

solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump("result.p4app")