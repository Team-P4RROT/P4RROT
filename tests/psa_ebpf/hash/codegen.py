import sys
sys.path.append('../../../src')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.standard_fields import *
from p4rrot.core.commands import *
from p4rrot.psa_ebpf.commands import *
from p4rrot.psa_ebpf.stateful import *

UID.reset()
fp = FlowProcessor(
        istruct = [('i_uint64', uint64_t)],
        ostruct = [('o_uint32', uint32_t)],
        state = [HashGenerator('hash_gen', uint32_t, SupportedHashAlgo.CRC32)]
    )

(
fp
.add(AssignHash('o_uint32', 'i_uint64', 'hash_gen'))
.add(SendBack())
)  



fs = FlowSelector(
        'IPV4_UDP',
        # 8 becasue its the length of the UDP header, seems a little unnecessary
        # for me or at least mythic to put a 8 there and not some sort of constant
        [(UdpDstPort,5555), (UdpLen,8+ hdr_len(fp.istruct) )],
        fp
    )


solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump('template')