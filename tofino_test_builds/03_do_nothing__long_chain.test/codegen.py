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

selectors = []
for port in range(5555,5555+25): 
    fs= FlowSelector(
            'IPV4_UDP',
            [(UdpDstPort,port)],
            fp
        )
    selectors.append(fs)

solution = Solution()
solution.add_flow_processor(fp)
for fs in selectors:
    solution.add_flow_selector(fs)

script_dir = os.path.dirname(__file__)
dir_path = os.path.join(script_dir, "test.p4app")
solution.get_generated_code().dump(dir_path)
