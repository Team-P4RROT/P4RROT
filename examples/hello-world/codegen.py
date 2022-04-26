import sys
sys.path.append('../../src/')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.core.commands import *  



UID.reset()
fp = FlowProcessor(
        istruct = [('msg_in',string_t(12))],
        locals  = [('l',bool_t),('msg_tmp',string_t(12))],
        ostruct = [('msg_out',string_t(12))]
    )



(
fp
.add(AssignConst('msg_tmp',b'Hello World!'))
.add(Equals('l','msg_in','msg_tmp'))
.add(If('l'))
          .add(AssignConst('msg_out',b'HELLO! :)   '))
          .add(SendBack())
     .Else()
          .add(StrictAssignVar('msg_out','msg_in'))
     .EndIf()
)  



fs = FlowSelector(
        'IPV4_UDP',
        [(UdpDstPort,5555),(UdpLen,8+13)],
        fp
    )


solution = Solution()
solution.add_flow_processor(fp)
solution.add_flow_selector(fs)
solution.get_generated_code().dump('test.p4app')
