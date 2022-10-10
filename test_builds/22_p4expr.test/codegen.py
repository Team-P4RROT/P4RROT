import sys

sys.path.append("../../src/")

from p4rrot.generator_tools import *
from p4rrot.known_types import *
from p4rrot.core.commands import *
from p4rrot.tofino.commands import *
from p4rrot.tofino.stateful import *
from p4rrot.standard_fields import *

UID.reset()

fp = FlowProcessor(istruct = [('a',uint8_t),('b',uint8_t),('c',uint8_t)])
(
fp
.add(IfExpr('a < b'))
        .add(P4Expr('c = b + a'))
    .Else()
        .add(P4Expr('c = c - a'))
    .EndIf()
)  

fs = FlowSelector("IPV4_UDP", [], fp)

solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump("test.p4app")
