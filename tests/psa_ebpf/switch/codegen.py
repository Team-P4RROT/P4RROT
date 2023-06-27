import sys

sys.path.append('../../../src')

from p4rrot.generator_tools import *
from p4rrot.known_types import *
from p4rrot.standard_fields import *
from p4rrot.core.commands import *

# from p4rrot.core.stateful import *


UID.reset()
fp = FlowProcessor(
    istruct = [('i_uint64', uint64_t),('i_uint32',uint32_t), ('i_uint16', uint16_t), ('i_uint8', uint8_t)],
    locals = [('ping_uint64', uint64_t),('ping_uint32',uint32_t), ('ping_uint16', uint16_t), ('ping_uint8', uint8_t),
              ('pong_uint64', uint64_t),('pong_uint32',uint32_t), ('pong_uint16', uint16_t), ('pong_uint8', uint8_t)],
    ostruct = [('o_uint64', uint64_t),('o_uint32',uint32_t), ('o_uint16', uint16_t), ('o_uint8', uint8_t)]
)

(
    fp
    .add(AssignConst('ping_uint64', int.from_bytes("PINGPING".encode(), byteorder='big')))
    .add(AssignConst('ping_uint32', int.from_bytes("PING".encode(), byteorder='big')))
    .add(AssignConst('ping_uint16', int.from_bytes("PI".encode(), byteorder='big')))
    .add(AssignConst('ping_uint8', int.from_bytes("?".encode(), byteorder='big')))
    .add(AssignConst('pong_uint64', int.from_bytes("PONGPONG".encode(), byteorder='big')))
    .add(AssignConst('pong_uint32', int.from_bytes("PONG".encode(), byteorder='big')))
    .add(AssignConst('pong_uint16', int.from_bytes("PO".encode(), byteorder='big')))
    .add(AssignConst('pong_uint8', int.from_bytes("!".encode(), byteorder='big')))
    .add(Switch('i_uint64'))
    .Case('ping_uint64').add(StrictAssignVar('o_uint64', 'pong_uint64'))
    .Case('pong_uint64').add(StrictAssignVar('o_uint64', 'ping_uint64'))
    .Default().add(AssignConst('o_uint64',int.from_bytes("????????".encode(), byteorder='big')))
    .EndSwitch()
    .add(Switch('i_uint32'))
    .Case('ping_uint32').add(StrictAssignVar('o_uint32', 'pong_uint32'))
    .Case('pong_uint32').add(StrictAssignVar('o_uint32', 'ping_uint32'))
    .Default().add(AssignConst('o_uint32',int.from_bytes("????".encode(), byteorder='big') ))
    .EndSwitch()
    .add(Switch('i_uint16'))
    .Case('ping_uint16').add(StrictAssignVar('o_uint16', 'pong_uint16'))
    .Case('pong_uint16').add(StrictAssignVar('o_uint16', 'ping_uint16'))
    .Default().add(AssignConst('o_uint16',int.from_bytes("??".encode(), byteorder='big') ))
    .EndSwitch()
    .add(Switch('i_uint8'))
    .Case('ping_uint8').add(StrictAssignVar('o_uint8', 'pong_uint8'))
    .Case('pong_uint8').add(StrictAssignVar('o_uint8', 'ping_uint8'))
    .Default().add(AssignConst('o_uint8',int.from_bytes("?".encode(), byteorder='big') ))
    .EndSwitch()
    .add(SendBack())
)

fs = FlowSelector(
    'IPV4_UDP',
    # 8 becasue its the length of the UDP header, seems a little unnecessary
    # for me or at least mythic to put a 8 there and not some sort of constant
    [(UdpDstPort, 5555), (UdpLen, 8 + hdr_len(fp.istruct))],
    fp
)

solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump('template')
