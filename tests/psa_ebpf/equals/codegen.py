import sys
sys.path.append('../../../src')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.standard_fields import *
from p4rrot.core.commands import *  

UID.reset()
fp = FlowProcessor(
        istruct = [('i_uint64_1', uint64_t),('i_uint32_1',uint32_t),
         ('i_uint16_1', uint16_t), ('i_uint8_1', uint8_t),
         ('i_uint64_2', uint64_t),('i_uint32_2',uint32_t),
         ('i_uint16_2', uint16_t), ('i_uint8_2', uint8_t),
         ('i_uint64_3', uint64_t),('i_uint32_3',uint32_t),
         ('i_uint16_3', uint16_t), ('i_uint8_3', uint8_t),],
        ostruct = [('o_b1_1', bool_t),('o_b2_1', bool_t),
         ('o_b3_1',bool_t ), ('o_b4_1', bool_t),
         ('o_b1_2',bool_t ), ('o_b2_2', bool_t),
         ('o_b3_2',bool_t ), ('o_b4_2', bool_t),
         ('o_b1_3',bool_t ), ('o_b2_3', bool_t),
         ('o_b3_3',bool_t ), ('o_b4_3', bool_t),
         ('o_b1_4',bool_t ), ('o_b2_4', bool_t),
         ('o_b3_4',bool_t ), ('o_b4_4', bool_t),
         ('o_b1_5',bool_t ), ('o_b2_5', bool_t),
         ('o_b3_5',bool_t ), ('o_b4_5', bool_t),
         ('o_b1_6',bool_t ), ('o_b2_6', bool_t),
         ('o_b3_6',bool_t ), ('o_b4_6', bool_t),
         ('o_b1_7',bool_t ), ('o_b2_7', bool_t),
         ('o_b3_7',bool_t ), ('o_b4_7', bool_t),
         ]
    )



(
fp
.add(Comment("Equals Test"))
.add(Equals('o_b1_1', 'i_uint64_1', 'i_uint64_2'))
.add(Equals('o_b2_1', 'i_uint32_1', 'i_uint32_2'))
.add(Equals('o_b3_1', 'i_uint16_1', 'i_uint16_2'))
.add(Equals('o_b4_1', 'i_uint8_1', 'i_uint8_2'))
.add(Equals('o_b1_2', 'i_uint64_1', 'i_uint64_3'))
.add(Equals('o_b2_2', 'i_uint32_1', 'i_uint32_3'))
.add(Equals('o_b3_2', 'i_uint16_1', 'i_uint16_3'))
.add(Equals('o_b4_2', 'i_uint8_1', 'i_uint8_3'))
.add(EqualsConst('o_b1_3', 'i_uint64_1', 0x4141414142424242))
.add(EqualsConst('o_b2_3', 'i_uint32_1', 0x43434343))
.add(EqualsConst('o_b3_3', 'i_uint16_1', 0x4444))
.add(EqualsConst('o_b4_3', 'i_uint8_1', 0x45))
.add(MaskedEqualsConst('o_b1_4', 'i_uint64_1', 0x00ff00000000ffff, 0x0041000000004242))
.add(MaskedEqualsConst('o_b2_4', 'i_uint32_1', 0x00ffff00, 0x00434300))
.add(MaskedEqualsConst('o_b3_4', 'i_uint16_1',0xf00f, 0x4004))
.add(MaskedEqualsConst('o_b4_4', 'i_uint8_1', 0x01,0x01))
.add(MaskedEqualsConst('o_b1_5', 'i_uint64_3', 0x00ff00000000ffff, 0x0041000000004242))
.add(MaskedEqualsConst('o_b2_5', 'i_uint32_3', 0x00ffff00, 0x00434300))
.add(MaskedEqualsConst('o_b3_5', 'i_uint16_3',0xf00f, 0x4004))
.add(MaskedEqualsConst('o_b4_5', 'i_uint8_3', 0x01,0x01))
.add(MaskedNotEqualsConst('o_b1_6', 'i_uint64_1', 0x00ff00000000ffff, 0x0041000000004242))
.add(MaskedNotEqualsConst('o_b2_6', 'i_uint32_1', 0x00ffff00, 0x00434300))
.add(MaskedNotEqualsConst('o_b3_6', 'i_uint16_1',0xf00f, 0x4004))
.add(MaskedNotEqualsConst('o_b4_6', 'i_uint8_1', 0x01,0x01))
.add(MaskedNotEqualsConst('o_b1_7', 'i_uint64_3', 0x00ff00000000ffff, 0x0041000000004242))
.add(MaskedNotEqualsConst('o_b2_7', 'i_uint32_3', 0x00ffff00, 0x00434300))
.add(MaskedNotEqualsConst('o_b3_7', 'i_uint16_3',0xf00f, 0x4004))
.add(MaskedNotEqualsConst('o_b4_7', 'i_uint8_3', 0x01,0x01))
.add(SendBack())
)  



fs = FlowSelector(
        'IPV4_UDP',
        # 8 becasue its the length of the UDP header, seems a little unnecessary
        # for me or at least mythic to put a 8 there and not some sort of constant
        [(UdpDstPort,5555), (UdpLen,8+ hdr_len(fp.istruct))],
        fp
    )


solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump('template')