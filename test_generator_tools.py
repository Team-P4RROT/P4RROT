from generator_tools import *
from known_types import *

def test_uid():
    a = UID.get()
    b = UID.get()
    assert a!=b


def test_code_writer_normal_usage():
    cw = CodeWriter()
    assert cw.get_code()==''

    cw.write('apple dog cat')
    cw.write('fish')
    assert cw.get_code()=='apple dog catfish'

    cw.new_line()
    assert cw.get_code()=='apple dog catfish\n'

    cw.increase_indent()
    cw.writeln('apple dog cat')
    assert cw.get_code()=='apple dog catfish\n\tapple dog cat\n'

    cw.decrease_indent()
    cw.write('fish')
    assert cw.get_code()=='apple dog catfish\n\tapple dog cat\nfish'

def test_code_writer_normal_negative_indent():
    cw = CodeWriter()
    for i in range(5):
        cw.decrease_indent()
    cw.write('a')
    assert cw.get_code()=='a'


def test_generated_code_access():
    gc = GeneratedCode()

    gc.get_headers().write('a')
    gc.get_parser().write('b')
    gc.get_decl().write('c')
    gc.get_apply().write('d')

    assert 'a' == gc.get_headers().get_code()
    assert 'b' == gc.get_parser().get_code()
    assert 'c' == gc.get_decl().get_code()
    assert 'd' == gc.get_apply().get_code()


def test_generated_code_concat():
    gc = GeneratedCode()

    gc.get_headers().write('a')
    gc.get_parser().write('b')
    gc.get_decl().write('c')
    gc.get_apply().write('d')
    gc.get_hdrlist().write('x')

    tmp = GeneratedCode()
    tmp.get_headers().write('e')
    tmp.get_parser().write('f')
    tmp.get_decl().write('g')
    tmp.get_apply().write('h')

    gc.concat(tmp)

    assert 'ae' == gc.get_headers().get_code()
    assert 'bf' == gc.get_parser().get_code()
    assert 'cg' == gc.get_decl().get_code()
    assert 'dh' == gc.get_apply().get_code()
    assert 'x' == gc.get_hdrlist().get_code()


def test_struct_generator():
    UID.reset()
    name,code = gen_struct([('id',uint8_t),('height',uint64_t),('width',uint32_t)],name='teststruct')
    assert name=='teststruct_uid1'
    assert code=='struct teststruct_uid1{\n\tbit<8> id;\n\tbit<64> height;\n\tbit<32> width;\n}\n'


def test_decision_state_generator():
    UID.reset()
    name,code = gen_decision_parser_state([(SrcIp,"10.0.0.10"),(UdpDstPort,5555),('pkt_type',7)],
                       "next_state","target_header",
                       [('pkt_type',uint8_t)],
                       "check_custom")
    assert name=="check_custom"
    assert code.get_headers().get_code()=='struct genstruct_uid1{\n\tbit<8> pkt_type;\n}\n'
    assert code.get_parser().get_code()=='state check_custom{\n\tgenstruct_uid1 tmp = pkt.lookahead<genstruct_uid1>();\n\n\ttransition select(hdr.ipv4.src,hdr.udp.dstPort,tmp.pkt_type){\n\t\t(10.0.0.10,5555,7) : target_header;\n\t\tdefault: next_state;\n\t}\n}\n'


def test_header_generator():
    UID.reset()
    name, handle, code = gen_header([('id',uint8_t),('height',uint64_t),('width',uint32_t)])
    assert name=='genhdr_uid1_h'
    assert handle=='genhdr_uid1'
    assert code=='header genhdr_uid1_h{\n\tbit<8> id;\n\tbit<64> height;\n\tbit<32> width;\n}\n'    


def test_header_state_generator():
    UID.reset()
    state_name, gc = gen_header_parser_state('stock_data', state_name="")
    assert state_name == 'parse_uid1'
    assert gc.get_parser().get_code() == 'state parse_uid1{\n\tpkt.extract(hdr.stock_data);\n\ttransition accept;\n}\n'


def test_flow_processor__just_headers():
    UID.reset()
    fp = FlowProcessor(
                istruct=[('a',uint32_t),('b',uint32_t)],
                ostruct=[('s',uint32_t)],
                mstruct=[('t',uint32_t)],    
                method='RESPOND'
        )
    gc = fp.get_generated_code()
    assert gc.get_headers().get_code()=='header genhdr_uid1_h{\n\tbit<32> a;\n\tbit<32> b;\n}\nheader genhdr_uid2_h{\n\tbit<32> s;\n}\nheader genhdr_uid3_h{\n\tbit<32> t;\n}\n'
    assert gc.get_hdrlist().get_code()=='genhdr_uid1_h genhdr_uid1;\ngenhdr_uid2_h genhdr_uid2;\ngenhdr_uid3_h genhdr_uid3;\n'
    #assert gc.get_apply().get_code().replace('\t','')=='if (hdr.genhdr_uid1.isValid()){\n\thdr.genhdr_uid2.setValid();\n\thdr.genhdr_uid3.setValid();\n\thdr.genhdr_uid3.setInvalid();\n\thdr.genhdr_uid1.setInvalid();\n\tmeta.size_growth = 0;\n\tmeta.size_loss = 4;\n}\n'.replace('\t','')
    assert gc.get_parser().get_code()=='state parse_genhdr_uid1{\n\tpkt.extract(hdr.genhdr_uid1);\n\ttransition accept;\n}\n'

def test_flow_selector__simple():
    UID.reset()
    fp = FlowProcessor(
                istruct=[('a',uint32_t),('b',uint32_t)],
                ostruct=[('s',uint32_t)],
                mstruct=[('t',uint32_t)],    
                method='RESPOND'
        )

    fs = FlowSelector('IPV4_UDP',[(UdpDstPort,5555)],fp)
    name,gc = fs.get_generated_code('next_state')
    assert name=='check_uid4'
    assert gc.get_parser().get_code()=='state check_uid4{\n\ttransition select(hdr.udp.dstPort){\n\t\t(5555) : parse_genhdr_uid1;\n\t\tdefault: next_state;\n\t}\n}\n'
    

def test_generate_chain():
    UID.reset()
    fp = FlowProcessor(
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

    f2 = FlowSelector(
            'IPV4_UDP',
            [(UdpDstPort,7777)],
            fp
        )

    assert generate_chain('IPV4_UDP',[fs,f2]).get_parser().get_code() == 'state check_uid4{\n\ttransition select(hdr.udp.dstPort){\n\t\t(7777) : parse_genhdr_uid1;\n\t\tdefault: accept;\n\t}\n}\nstate check_uid5{\n\ttransition select(hdr.udp.dstPort){\n\t\t(5555) : parse_genhdr_uid1;\n\t\tdefault: check_uid4;\n\t}\n}\n#define CHAIN_IPV4_UDP\nstate chain_ipv4_udp{\n\ttransition check_uid5;\n}\n'


