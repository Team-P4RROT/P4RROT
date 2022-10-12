import sys

sys.path.append("../../src/")

from p4rrot.generator_tools import *
from p4rrot.known_types import *
from p4rrot.core.commands import *
from p4rrot.tofino.commands import *
from p4rrot.tofino.stateful import *
from p4rrot.standard_fields import *

UID.reset()

fp = FlowProcessor(
        istruct = [('x',uint32_t),('i',uint8_t),('y',uint32_t)],
        state=[LPF('rate',uint32_t,uint8_t,10)]
    )

fp.add(UpdateLPF('y','rate','i','x'))
  
fs = FlowSelector("IPV4_UDP", [], fp)

solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump("result.p4app")
