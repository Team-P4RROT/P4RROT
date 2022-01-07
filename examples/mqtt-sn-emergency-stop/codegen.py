import sys
sys.path.append('../../')

from generator_tools import *
from known_types import *  
from commands import *  
from stateful import *
    
UID.reset()

# **** STATEFUL ELEMENTS *****

s_expect_temp_regack = SharedVariable('expect_temp_regack',bool_t)
s_temp_topic_id = SharedVariable('temp_topic_id',uint16_t)

s_expect_alarm_regack = SharedVariable('expect_alarm_regack',bool_t)
s_alarm_topic_id = SharedVariable('alarm_topic_id',uint16_t)



# ***** READ REGISTER PACKETS *****

fp_reg_reader = FlowProcessor(
        istruct=[('msg_len',uint8_t),('msg_type',uint8_t),
                ('topic_id',uint16_t),('message_id',uint16_t),
                ('topic_name',uint32_t)],
        locals=[('b',bool_t),('topic_guess',uint32_t)],
        state=[s_expect_alarm_regack,s_expect_temp_regack]
    )

fp_reg_reader\
    .add(Comment('*** Processong REG messages'))\
    .add(Comment('test "temp"'))\
    .add(AssignConst('topic_guess',0x74656d70))\
    .add(Equals('b','topic_name','topic_guess'))\
    .add(If('b'))\
            .add(WriteToShared('expect_temp_regack','b'))\
        .EndIf()\
    .add(Comment('test "alar"'))\
    .add(AssignConst('topic_guess',0x616c6172))\
    .add(Equals('b','topic_name','topic_guess'))\
    .add(If('b'))\
            .add(WriteToShared('expect_alarm_regack','b'))\
        .EndIf()\
    

# select register temperature
fs_reg_reader_1 = FlowSelector(
        'IPV4_UDP',
        [(UdpDstPort,10000),('msg_type',0x0a),('msg_len',17)],
        lookahead_struct=[('msg_len',uint8_t),('msg_type',uint8_t)],
        flow_processor=fp_reg_reader
    )

# select register alarm
fs_reg_reader_2 = FlowSelector(
        'IPV4_UDP',
        [(UdpDstPort,10000),('msg_type',0x0a),('msg_len',11)],
        lookahead_struct=[('msg_len',uint8_t),('msg_type',uint8_t)],
        flow_processor=fp_reg_reader
    )



# ***** READ REGACK PACKETS *****

fp_ack_reader = FlowProcessor(
        istruct=[('msg_len',uint8_t),('msg_type',uint8_t),
                ('topic_id',uint16_t),('message_id',uint16_t)],
        locals=[('b',bool_t)],
        state=[s_expect_alarm_regack, s_expect_temp_regack,
                s_temp_topic_id, s_alarm_topic_id]
    )

fp_ack_reader\
    .add(Comment('*** Processong REGACK messages'))\
    .add(ReadFromShared('b','expect_temp_regack'))\
    .add(If('b'))\
            .add(WriteToShared('temp_topic_id','topic_id'))\
            .add(LogicalNot('b'))\
            .add(WriteToShared('expect_temp_regack','b'))\
        .EndIf()\
    .add(ReadFromShared('b','expect_alarm_regack'))\
    .add(If('b'))\
            .add(WriteToShared('alarm_topic_id','topic_id'))\
            .add(LogicalNot('b'))\
            .add(WriteToShared('expect_alarm_regack','b'))\
        .EndIf()\
    

fs_ack_reader = FlowSelector(
        'IPV4_UDP',
        [(UdpSrcPort,10000),('msg_type',0x0b),('msg_len',7)],
        lookahead_struct=[('msg_len',uint8_t),('msg_type',uint8_t)],
        flow_processor=fp_ack_reader
    )



# ***** CHECK PUB PACKETS *****

fp_pub_checker = FlowProcessor(
        istruct=[('msg_len',uint8_t),('msg_type',uint8_t),('flags',uint8_t),
                ('topic_id',uint16_t),('message_id',uint16_t),('sensor_value',uint32_t)],
        locals=[('b',bool_t),('max_value',uint32_t),('tmp',uint16_t)],
        state=[s_expect_alarm_regack, s_expect_temp_regack,
                s_temp_topic_id, s_alarm_topic_id]
    )

fp_pub_checker\
    .add(Comment('*** Processong PUBLISH messages'))\
    .add(ReadFromShared('tmp','temp_topic_id'))\
    .add(Equals('b','topic_id','tmp'))\
    .add(If('b'))\
            .add(AssignConst('max_value',70))\
            .add(GreaterThan('b','sensor_value','max_value'))\
            .add(If('b'))\
                    .add(Comment('publis alarm'))\
                    .add(ReadFromShared('topic_id','alarm_topic_id'))\
                    .add(AssignConst('sensor_value',0x73746f70))\
                    .add(SendBack())\
                .EndIf()\
        .EndIf()  


fs_pub_checker = FlowSelector(
        'IPV4_UDP',
        [(UdpSrcPort,10000),('msg_type',0x0c),('msg_len',11)],
        lookahead_struct=[('msg_len',uint8_t),('msg_type',uint8_t)],
        flow_processor=fp_pub_checker
    )



solution = Solution()

solution.add_flow_processor(fp_reg_reader)
solution.add_flow_selector(fs_reg_reader_1)
solution.add_flow_selector(fs_reg_reader_2)

solution.add_flow_processor(fp_ack_reader)
solution.add_flow_selector(fs_ack_reader)

solution.add_flow_processor(fp_pub_checker)
solution.add_flow_selector(fs_pub_checker)



solution.get_generated_code().dump('test.p4app')
