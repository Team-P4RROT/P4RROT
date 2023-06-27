import sys
sys.path.append('../../../src')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.standard_fields import *
from p4rrot.core.commands import *  

UID.reset()

fp = FlowProcessor(istruct = [('a',uint8_t),('b',uint8_t)],
                   ostruct = [('c',uint8_t)])

(
fp
.add(IfExpr('a < b'))
        .add(P4Expr('c = b + a'))
    .Else()
        .add(P4Expr('c = a - b'))
    .EndIf()
.add(SendBack())
)  

fs = FlowSelector("IPV4_UDP", [], fp)
solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump('template')
