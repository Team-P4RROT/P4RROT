import sys
sys.path.append('../../src/')

from p4rrot.generator_tools import *
from p4rrot.known_types import *  
from p4rrot.core.commands import *  
from p4rrot.core.stateful import *
from p4rrot.v1model.commands import *
from p4rrot.v1model.stateful import *
    
UID.reset()

# **** STATEFUL ELEMENTS *****

r_next_id = SharedVariable('r_next_id',uint64_t)

# ***** FLOW PROCESSOR *****

fp = FlowProcessor(
        istruct=[('session',padding_t(10)),('seq_id',uint64_t),('msg_count',uint16_t)],
        locals=[('b',bool_t),('next_id',uint64_t),('tmp_next_id',uint64_t),
                ('missing',uint64_t),('count',uint64_t)],
        state=[r_next_id]
    )

fp\
        .add(ReadFromShared('next_id','r_next_id'))\
        .add(GreaterThan('b','seq_id','next_id'))\
        .add(If('b'))\
                .add(StrictAssignVar('tmp_next_id','next_id'))\
\
                .add(Comment('*** update expected next id ***'))\
                .add(CastVar('count','msg_count'))\
                .add(StrictAddition('next_id','seq_id','count'))\
                .add(WriteToShared('r_next_id','next_id'))\
\
                .add(Comment('*** send back a retransmission request ***'))\
                .add(StrictSubtraction('missing','seq_id','tmp_next_id'))\
                .add(CastVar('msg_count','missing'))\
                .add(StrictAssignVar('seq_id','tmp_next_id'))\
                .add(TruncateRemainng())\
                .add(SetStandardField(UdpSrcPort,7777))\
                .add(ClonePacket(0x0300))\
                .add(SendBack())\
             .Else()\
                .add(Comment('*** update expected next id if required***'))\
                .add(Equals('b','next_id','seq_id'))\
                .add(If('b'))\
                        .add(CastVar('count','msg_count'))\
                        .add(StrictAddition('next_id','seq_id','count'))\
                        .add(WriteToShared('r_next_id','next_id'))\
                     .EndIf()\
        .EndIf()

    
# ***** FLOW SELECTOR *****

fs = FlowSelector(
        'IPV4_UDP',
        [(UdpSrcPort,5555)],
        flow_processor=fp
    )


solution = Solution()

solution.add_flow_processor(fp)
solution.add_flow_selector(fs)

solution.get_generated_code().dump('test.p4app')
