import sys
sys.path.append('../../')

from generator_tools import *
from known_types import *    
    
UID.reset()
fp = TofinoFlowProcessor(
        istruct=[('a',uint32_t),('b',uint32_t)],
        ostruct=[('s',uint32_t)],
        mstruct=[('t',uint32_t)],    
        method='RESPOND'
    )

fs = FlowSelector(
        'IPV4_UDP',
        [(UdpDstPort,5555)],
        fp
    )

solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
script_dir = os.path.dirname(__file__)
dir_path = os.path.join(script_dir, "test.p4app")
solution.get_generated_code().dump(dir_path)
