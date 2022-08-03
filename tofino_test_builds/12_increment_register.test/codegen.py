import sys

sys.path.append('../../src/')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.core.commands import * 
from p4rrot.tofino.commands import *
from p4rrot.tofino.stateful import *

UID.reset()
fp = FlowProcessor(
    istruct=[("counter_value", uint32_t)],
    state=[ SharedArray('counter_register',uint32_t, uint32_t, 10) ],
    method="MODIFY"
)

fp.add(
    IncrementSharedArray("counter_register", uint32_t, uint32_t, 1, read_new_to = "counter_value", env=fp.get_env())
    )

fs = FlowSelector("IPV4_UDP", [(UdpDstPort, 5555)], fp)

solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump("test.p4app")
