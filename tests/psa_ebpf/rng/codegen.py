import sys
sys.path.append('../../../src/')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.standard_fields import *
from p4rrot.core.commands import *  
from p4rrot.psa_ebpf.commands import *
from p4rrot.psa_ebpf.stateful import *

fp = FlowProcessor(
istruct = [],
ostruct = [('o1',uint8_t)],
)

fp \
.add(AssignRandomValue('o1', 0, 255))\
.add(SendBack())

fs = FlowSelector(
        'IPV4_UDP',
        [(UdpDstPort,5555)],
        fp
)

solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump('.')
