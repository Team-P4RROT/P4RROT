import sys
sys.path.append('../../../src')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.standard_fields import *
from p4rrot.core.commands import *

ASCII_T = 0x54
ASCII_F = 0x46

UID.reset()
fp = FlowProcessor(
        istruct = [('op_a', uint8_t),('op_b', uint8_t)],
        mstruct = [('tmp_bool', bool_t)],
        ostruct = [('res_greater', uint8_t),('res_less', uint8_t),('res_equals', uint8_t)]
)

(
fp
.add(Equals('tmp_bool', 'op_a', 'op_b'))
.add(If('tmp_bool',
        fp.get_env(),
        then_block=Block(env=fp.get_env()).add(AssignConst('res_equals', ASCII_T)),
        else_block=Block(env=fp.get_env()).add(AssignConst('res_equals', ASCII_F))))
.add(GreaterThan('tmp_bool', 'op_a', 'op_b'))
.add(If('tmp_bool',
        fp.get_env(),
        then_block=Block(env=fp.get_env()).add(AssignConst('res_greater', ASCII_T)),
        else_block=Block(env=fp.get_env()).add(AssignConst('res_greater', ASCII_F))))
.add(LessThan('tmp_bool', 'op_a', 'op_b'))
.add(If('tmp_bool',
        fp.get_env(),
        then_block=Block(env=fp.get_env()).add(AssignConst('res_less', ASCII_T)),
        else_block=Block(env=fp.get_env()).add(AssignConst('res_less', ASCII_F))))
.add(SendBack())
)



fs = FlowSelector(
        'IPV4_UDP',
        [(UdpDstPort,5555)],
        fp
    )


solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump('template')
