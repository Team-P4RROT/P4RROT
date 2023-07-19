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
        istruct = [('op_a', uint8_t), ('op_b', uint8_t)],
        mstruct = [('tmp_bool', bool_t),('bool_op_a', bool_t),('bool_op_b', bool_t)],
        ostruct = [('res_and', uint8_t), ('res_or', uint8_t), ('res_not', uint8_t)]
)

(
        fp
        .add(EqualsConst('bool_op_a', 'op_a', ASCII_T))
        .add(EqualsConst('bool_op_b', 'op_b', ASCII_T))
        .add(LogicalAnd('tmp_bool', 'bool_op_a', 'bool_op_b'))
        .add(If('tmp_bool',
                fp.get_env(),
                then_block=Block(env=fp.get_env()).add(AssignConst('res_and', ASCII_T)),
                else_block=Block(env=fp.get_env()).add(AssignConst('res_and', ASCII_F))))
        .add(LogicalOr('tmp_bool', 'bool_op_a', 'bool_op_b'))
        .add(If('tmp_bool',
                fp.get_env(),
                then_block=Block(env=fp.get_env()).add(AssignConst('res_or', ASCII_T)),
                else_block=Block(env=fp.get_env()).add(AssignConst('res_or', ASCII_F))))
        .add(LogicalNot('bool_op_a'))
        .add(If('bool_op_a',
                fp.get_env(),
                then_block=Block(env=fp.get_env()).add(AssignConst('res_not', ASCII_T)),
                else_block=Block(env=fp.get_env()).add(AssignConst('res_not', ASCII_F))))
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
