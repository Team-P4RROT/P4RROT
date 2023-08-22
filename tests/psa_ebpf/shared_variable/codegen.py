import sys

sys.path.append('../../../src')

from p4rrot.generator_tools import *
from p4rrot.known_types import *
from p4rrot.standard_fields import *
from p4rrot.core.commands import *
from p4rrot.psa_ebpf.stateful import *

# from p4rrot.core.stateful import *


UID.reset()
fp = FlowProcessor(
    istruct = [('unused', uint8_t)],
    locals = [('tmp', uint8_t), ('one', uint8_t)],
    ostruct = [('out_uint8_t', uint8_t)],
    state = [ SharedVariable('shared', uint8_t)]
)

(
    fp
    .add(AssignConst('one', 1))
    .add(ReadFromShared('tmp', 'shared'))
    .add(StrictAddition('tmp', 'tmp', 'one'))
    .add(WriteToShared('shared', 'tmp'))
    .add(StrictAssignVar('out_uint8_t', 'tmp'))
    .add(SendBack())
)

fs = FlowSelector(
    'IPV4_UDP',
    # 8 becasue its the length of the UDP header, seems a little unnecessary
    # for me or at least mythic to put a 8 there and not some sort of constant
    [(UdpDstPort, 5555)],
    fp
)

solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump('template')
