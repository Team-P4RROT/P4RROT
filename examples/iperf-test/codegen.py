import sys
sys.path.append('../../')

from generator_tools import *
from known_types import *  
from commands import *  
from stateful import *
    
UID.reset()

# **** STATEFUL ELEMENTS *****

counter1 = SharedVariable('counter1', uint64_t)
counter2 = SharedVariable('counter2', uint64_t)

ZERO = Const('ZERO',uint8_t,0)
ONE = Const('ONE',uint8_t,0)

# ***** REQUIRED PROCESSING ***** 

# MODIFY UDP FLOW

fp = FlowProcessor(
        istruct=[('_padding',padding_t(36)),('a',uint32_t),('b',uint32_t)],
        locals=[('r',uint8_t),('tmp1',uint64_t),('tmp2',uint64_t),('l',bool_t)],
        state=[counter1,counter2,ZERO,ONE]
    )

fp\
    .add(Comment('*** generate random value ***'))\
    .add(AssignRandomValue('r',0,3))\
    .add(Comment('*** updateing counters and performing calculation based on the random value ***'))\
    .add(Switch('r'))\
                .Case('ZERO')\
                        .add(Comment('increment counter1'))\
                        .add(Atomic())\
                                .add(ReadFromShared('tmp1','counter1'))\
                                .add(Increment('tmp1',1))\
                                .add(WriteToShared('counter1','tmp1'))\
                            .EndAtomic()\
                        .add(Comment('increment counter2'))\
                        .add(Atomic())\
                                .add(ReadFromShared('tmp2','counter2'))\
                                .add(Increment('tmp2',1))\
                                .add(WriteToShared('counter2','tmp2'))\
                            .EndAtomic()\
                        .add(Comment('calculate some stuff'))\
                        .add(StrictAddition('b','b','b'))\
                        .add(StrictAddition('a','b','b'))\
                        .add(StrictAddition('a','a','a'))\
                .Case('ONE')\
                        .add(Comment('increment counter2'))\
                        .add(Atomic())\
                                .add(ReadFromShared('tmp2','counter2'))\
                                .add(Increment('tmp2',1))\
                                .add(WriteToShared('counter2','tmp2'))\
                            .EndAtomic()\
                        .add(Comment('calculate some stuff'))\
                        .add(StrictAddition('b','b','b'))\
                        .add(StrictAddition('a','b','b'))\
                        .add(StrictAddition('a','a','a'))\
                        .add(Comment('increment counter1'))\
                        .add(Atomic())\
                                .add(ReadFromShared('tmp1','counter1'))\
                                .add(Increment('tmp1',1))\
                                .add(WriteToShared('counter1','tmp1'))\
                            .EndAtomic()\
                .Default()\
                        .add(Comment('increment both counters'))\
                        .add(Atomic())\
                                .add(ReadFromShared('tmp1','counter1'))\
                                .add(Increment('tmp1',1))\
                                .add(WriteToShared('counter1','tmp1'))\
                                .add(ReadFromShared('tmp2','counter2'))\
                                .add(Increment('tmp2',1))\
                                .add(WriteToShared('counter2','tmp2'))\
                            .EndAtomic()\
        .EndSwitch()


fp_ping = FlowProcessor(
        istruct=[('msg_type',uint8_t),('code',uint8_t),('csum',uint16_t),('_padding',padding_t(4+8+16)),('a',uint32_t),('b',uint32_t)],
        locals=[('r',uint8_t),('tmp1',uint64_t),('tmp2',uint64_t),('l',bool_t),('tmp_a',uint32_t),('tmp_b',uint32_t)],
        state=[counter1,counter2,ZERO,ONE]
    )

fp_ping\
    .add(Comment('*** send back as an echo-response ***'))\
    .add(AssignConst('msg_type',0))\
    .add(AssignConst('code',0))\
    .add(AssignConst('csum',0))\
    .add(StrictAssignVar('tmp_a','a'))\
    .add(StrictAssignVar('tmp_b','b'))\
    .add(SendBack())\
    .add(Comment('*** generate random value ***'))\
    .add(AssignRandomValue('r',0,3))\
    .add(Comment('*** updateing counters and performing calculation based on the random value ***'))\
    .add(Switch('r'))\
                .Case('ZERO')\
                        .add(Comment('increment counter1'))\
                        .add(Atomic())\
                                .add(ReadFromShared('tmp1','counter1'))\
                                .add(Increment('tmp1',1))\
                                .add(WriteToShared('counter1','tmp1'))\
                            .EndAtomic()\
                        .add(Comment('increment counter2'))\
                        .add(Atomic())\
                                .add(ReadFromShared('tmp2','counter2'))\
                                .add(Increment('tmp2',1))\
                                .add(WriteToShared('counter2','tmp2'))\
                            .EndAtomic()\
                        .add(Comment('calculate some stuff'))\
                        .add(StrictAddition('b','b','b'))\
                        .add(StrictAddition('a','b','b'))\
                        .add(StrictAddition('a','a','a'))\
                .Case('ONE')\
                        .add(Comment('increment counter2'))\
                        .add(Atomic())\
                                .add(ReadFromShared('tmp2','counter2'))\
                                .add(Increment('tmp2',1))\
                                .add(WriteToShared('counter2','tmp2'))\
                            .EndAtomic()\
                        .add(Comment('calculate some stuff'))\
                        .add(StrictAddition('b','b','b'))\
                        .add(StrictAddition('a','b','b'))\
                        .add(StrictAddition('a','a','a'))\
                        .add(Comment('increment counter1'))\
                        .add(Atomic())\
                                .add(ReadFromShared('tmp1','counter1'))\
                                .add(Increment('tmp1',1))\
                                .add(WriteToShared('counter1','tmp1'))\
                            .EndAtomic()\
                .Default()\
                        .add(Comment('increment both counters'))\
                        .add(Atomic())\
                                .add(ReadFromShared('tmp1','counter1'))\
                                .add(Increment('tmp1',1))\
                                .add(WriteToShared('counter1','tmp1'))\
                                .add(ReadFromShared('tmp2','counter2'))\
                                .add(Increment('tmp2',1))\
                                .add(WriteToShared('counter2','tmp2'))\
                            .EndAtomic()\
        .EndSwitch()\
        .add(Comment('*** rewrite original packet data ***'))\
        .add(StrictAssignVar('a','tmp_a'))\
        .add(StrictAssignVar('b','tmp_b'))\



# ***** SELECTOR *****  

fs = FlowSelector(
        'IPV4_UDP',
        [(UdpDstPort,5001)],
        flow_processor=fp
    )

fs_ping = FlowSelector(
        'IPV4_RAW',
        [(Ipv4Protocol,1),(Ipv4TTL,255),('msg_type',8)],
        lookahead_struct=[('msg_type',uint8_t)],
        flow_processor=fp_ping
    )

solution = Solution()

solution.add_flow_processor(fp)
solution.add_flow_processor(fp_ping)
solution.add_flow_selector(fs)
solution.add_flow_selector(fs_ping)
solution.get_generated_code().dump('test.p4app')
