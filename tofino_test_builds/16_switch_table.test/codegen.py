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
        istruct = [('rtype',uint16_t),('rclass',uint16_t)],
        helpers = [('x',uint8_t),('y',uint8_t)],
        locals  = [('l',bool_t)],
    )

(
fp
.add(SwitchTable(['x']))
    .Case([5])
        .add(AssignConst('y',7))
    .Case([9])
        .add(AssignConst('y',5))
    .Case([11])
        .add(AssignConst('y',11))
    .Default()
        .add(AssignConst('y',9))
.EndSwitch()
)  

fs = FlowSelector("IPV4_UDP", [], fp)

solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump("result.p4app")
