import sys
sys.path.append('../../../src/')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.standard_fields import *
from p4rrot.core.commands import *  
from p4rrot.tcp_fields import *
from p4rrot.psa_ebpf.commands import *



UID.reset()
fp = FlowProcessor(
        istruct = [],
        ostruct = [],
        standard_fields = [UdpDstPort]
)



(
fp
.add(Clone([UdpDstPort.handle], table_name="clone_table", action_name="assign_clone"))
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
