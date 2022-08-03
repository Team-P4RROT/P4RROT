import sys

sys.path.append("../../src/")

from p4rrot.core.commands import *
from p4rrot.tofino.commands import *
from p4rrot.tofino.stateful import *


class MockUsingBlock:
    def __init__(self):
        self.gc = GeneratedCode()
        self.gc.get_decl().writeln("register_data = register_data + 1;")
        self.gc.get_decl().writeln("out_data = register_data;")

    def get_generated_code(self):
        return self.gc


def test_using_block():
    mock_block = {  # we are only interested in whether the reference gets stored
        "a": 12
    }
    mock_env = {"b": 10}
    u_block = UsingBlock(mock_env, mock_block)
    assert u_block.EndUsing() == mock_block


def test_simple_using_command():
    mock_block = {"a": 12}
    mock_env = {"b": 10}
    u_block = UsingBlock(mock_env, mock_block)
    sharred_array_action_params = [
        {"type": uint16_t, "mode": "inout", "name": "register_data"}
    ]
    using = Using(
        "action_1",
        "shared_a_1",
        uint16_t,
        uint16_t,
        uint16_t,
        sharred_array_action_params,
        u_block,
    )
    generated_lines = (
        using.get_generated_code().get_decl().get_code().strip().split("\n")
    )
    expected_lines = [
        "RegisterAction<bit<16>,bit<16>,bit<16>>(shared_a_1) action_1 = {",
        "void apply(inout bit<16> register_data){",
        "\t\t\t}",
        "};",
    ]
    assert generated_lines == expected_lines


def test_using_command_with_statements():
    mock_block = {"a": 12}
    mock_env = {"b": 10}
    u_block = MockUsingBlock()
    sharred_array_action_params = [
        {"type": uint16_t, "mode": "inout", "name": "register_data"},
        {"type": uint16_t, "mode": "out", "name": "out_data"},
    ]
    using = Using(
        "action_1",
        "shared_a_1",
        uint16_t,
        uint16_t,
        uint16_t,
        sharred_array_action_params,
        u_block,
    )
    generated_lines = (
        using.get_generated_code().get_decl().get_code().strip().split("\n")
    )
    expected_lines = [
        "RegisterAction<bit<16>,bit<16>,bit<16>>(shared_a_1) action_1 = {",
        "void apply(inout bit<16> register_data, out bit<16> out_data){",
        "\t\tregister_data = register_data + 1;",
        "\t\tout_data = register_data;",
        "\t}",
        "};",
    ]
    assert generated_lines == expected_lines


def test_using_command_should_return():

    sharred_array_action_params = [
        {"type": uint16_t, "mode": "inout", "name": "register_data"},
        {"type": uint16_t, "mode": "out", "name": "out_data"},
    ]
    using = Using(
        "action_1",
        "shared_a_1",
        uint16_t,
        uint16_t,
        uint16_t,
        sharred_array_action_params,
    )

    u_block = MockUsingBlock()
    using_b = Using(
        "action_1",
        "shared_a_1",
        uint16_t,
        uint16_t,
        uint16_t,
        sharred_array_action_params,
        u_block,
    )

    assert using.should_return()
    assert not using_b.should_return()


def test_using_command_return_object():

    mock_block = {  # we are only interested in whether the reference gets stored
        "a": 12
    }
    sharred_array_action_params = [
        {"type": uint16_t, "mode": "inout", "name": "register_data"},
        {"type": uint16_t, "mode": "out", "name": "out_data"},
    ]
    using = Using(
        "action_1",
        "shared_a_1",
        uint16_t,
        uint16_t,
        uint16_t,
        sharred_array_action_params,
    )

    returned_object = using.get_return_object(mock_block)
    assert isinstance(returned_object, UsingBlock)
    assert returned_object.parent_block == mock_block


# shared_array, number_type, index_type, index_to_increase, step = 1, read_new_to = None, env=None):


def test_increment_shared_array_code_generation():
    UID.reset()
    increment_shared_arr = IncrementSharedArray("shared_a_1", uint16_t, uint16_t, 3)
    gc = increment_shared_arr.get_generated_code()
    generated_decl = gc.get_decl().get_code().strip().split("\n")
    generated_apply = gc.get_apply().get_code().strip()
    expected_decl = [
        "RegisterAction<bit<16>,bit<16>,bit<16>>(shared_a_1) increment_shared_array_action_uid1 = {",
        "void apply(inout bit<16> to_store){",
        "\t\tto_store = to_store + 1;",
        "\t}",
        "};",
    ]
    expected_apply = "increment_shared_array_action_uid1.execute(3);"
    assert generated_decl == expected_decl
    assert generated_apply == expected_apply


def test_increment_shared_array_check():
    env = Environment([("a", uint32_t)], [], [], [], [], "inp", "out", "met", None)
    increment_shared_arr = IncrementSharedArray(
        "shared_a_1", uint32_t, uint16_t, 3, read_new_to="a", env=env
    )
    increment_shared_arr.check()


def test_decrement_shared_array_code_generation():
    UID.reset()
    decrement_shared_arr = DecrementSharedArray("shared_a_1", uint16_t, uint16_t, 3)
    gc = decrement_shared_arr.get_generated_code()
    generated_decl = gc.get_decl().get_code().strip().split("\n")
    generated_apply = gc.get_apply().get_code().strip()
    expected_decl = [
        "RegisterAction<bit<16>,bit<16>,bit<16>>(shared_a_1) decrement_shared_array_action_uid1 = {",
        "void apply(inout bit<16> to_store){",
        "\t\tto_store = to_store - 1;",
        "\t}",
        "};",
    ]
    expected_apply = "decrement_shared_array_action_uid1.execute(3);"
    assert generated_decl == expected_decl
    assert generated_apply == expected_apply


def test_decrement_shared_array_check():
    env = Environment([("a", uint32_t)], [], [], [], [], "inp", "out", "met", None)
    decrement_shared_arr = DecrementSharedArray(
        "shared_a_1", uint32_t, uint16_t, 3, read_new_to="a", env=env
    )
    decrement_shared_arr.check()


def test_write_shared_array_code_generation():
    UID.reset()
    env = Environment([("a", uint32_t)], [], [], [], [], "inp", "out", "met", None)
    write_shared_arr = WriteSharedArray(
        "shared_a_2", uint32_t, uint16_t, 3, 100, "a", env
    )
    gc = write_shared_arr.get_generated_code()
    generated_decl = gc.get_decl().get_code().strip().split("\n")
    generated_apply = gc.get_apply().get_code().strip()
    expected_decl = [
        "RegisterAction<bit<32>,bit<16>,bit<32>>(shared_a_2) write_shared_array_action_uid1 = {",
        "void apply(inout bit<32> to_store, out bit<32> to_return){",
        "\t\tto_return = to_store;",
        "\t\tto_store = 100;",
        "\t}",
        "};",
    ]
    expected_apply = "hdr.inp.a = write_shared_array_action_uid1.execute(3);"
    assert generated_decl == expected_decl
    assert generated_apply == expected_apply


def test_write_shared_array_check():
    env = Environment([("b", uint32_t)], [], [], [], [], "inp", "out", "met", None)
    write_shared_arr = WriteSharedArray(
        "shared_a_1", uint32_t, uint16_t, 3, 100, read_old_to="b", env=env
    )
    write_shared_arr.check()


def test_read_shared_array_code_generation():
    UID.reset()
    env = Environment([("a", uint32_t)], [], [], [], [], "inp", "out", "met", None)
    read_shared_arr = ReadSharedArray("shared_a_2", uint32_t, uint16_t, 3, "a", env)
    gc = read_shared_arr.get_generated_code()
    generated_decl = gc.get_decl().get_code().strip().split("\n")
    generated_apply = gc.get_apply().get_code().strip()
    expected_decl = [
        "RegisterAction<bit<32>,bit<16>,bit<32>>(shared_a_2) read_shared_array_action_uid1 = {",
        "void apply(inout bit<32> stored_value, out bit<32> to_return){",
        "\t\tto_return = stored_value;",
        "\t}",
        "};",
    ]
    expected_apply = "hdr.inp.a = read_shared_array_action_uid1.execute(3);"
    assert generated_decl == expected_decl
    assert generated_apply == expected_apply


def test_read_shared_array_check():
    env = Environment([("b", uint32_t)], [], [], [], [], "inp", "out", "met", None)
    read_shared_arr = ReadSharedArray(
        "shared_a_1", uint32_t, uint16_t, 3, read_to="b", env=env
    )
    read_shared_arr.check()


def test_greater_than_table_code_generation():
    UID.reset()
    env = Environment(
        [("a", uint32_t), ("b", uint32_t), ("t", bool_t)],
        [],
        [],
        [],
        [],
        "inp",
        "out",
        "met",
        None,
    )
    table = GreaterThanTable("t", "a", "b", env)
    gc = table.get_generated_code()
    generated_decl = gc.get_decl().get_code().strip().split("\n")
    generated_apply = gc.get_apply().get_code().strip().split("\n")
    expected_decl = [
        "bit<32> difference_variable_uid2;",
        "action setter_action_uid3_true() {",
        "\thdr.inp.t = 1;",
        "}",
        "action setter_action_uid3_false() {",
        "\thdr.inp.t = 0;",
        "}",
        "table eval_table_uid1 {",
        "\tkey = {",
        "\t\tdifference_variable_uid2: ternary;",
        "\t}",
        "\tactions = {",
        "\t\tsetter_action_uid3_true;",
        "\t\tsetter_action_uid3_false;",
        "\t}",
        "\tsize = 2;",
        "\tconst default_action = setter_action_uid3_true;",
        "\tconst entries = {",
        "\t\t0b00000000000000000000000000000000&&&0b11111111111111111111111111111111 : setter_action_uid3_false();",
        "\t\t0b00000000000000000000000000000000&&&0b10000000000000000000000000000000 : setter_action_uid3_false();",
        "\t}",
        "}",
    ]
    expected_apply = [
        "difference_variable_uid2 = hdr.inp.a - hdr.inp.b;",
        "eval_table_uid1.apply();",
    ]
    assert generated_decl == expected_decl
    assert generated_apply == expected_apply


def test_smaller_than_table_code_generation():
    UID.reset()
    env = Environment(
        [("a", uint32_t), ("b", uint32_t), ("t", bool_t)],
        [],
        [],
        [],
        [],
        "inp",
        "out",
        "met",
        None,
    )
    table = SmallerThanTable("t", "a", "b", env)
    gc = table.get_generated_code()
    generated_decl = gc.get_decl().get_code().strip().split("\n")
    generated_apply = gc.get_apply().get_code().strip().split("\n")
    expected_decl = [
        "bit<32> difference_variable_uid2;",
        "action setter_action_uid3_true() {",
        "\thdr.inp.t = 1;",
        "}",
        "action setter_action_uid3_false() {",
        "\thdr.inp.t = 0;",
        "}",
        "table eval_table_uid1 {",
        "\tkey = {",
        "\t\tdifference_variable_uid2: ternary;",
        "\t}",
        "\tactions = {",
        "\t\tsetter_action_uid3_true;",
        "\t\tsetter_action_uid3_false;",
        "\t}",
        "\tsize = 2;",
        "\tconst default_action = setter_action_uid3_false;",
        "\tconst entries = {",
        "\t\t0b00000000000000000000000000000000&&&0b11111111111111111111111111111111 : setter_action_uid3_false();",
        "\t\t0b10000000000000000000000000000000&&&0b10000000000000000000000000000000 : setter_action_uid3_true();",
        "\t}",
        "}",
    ]
    expected_apply = [
        "difference_variable_uid2 = hdr.inp.a - hdr.inp.b;",
        "eval_table_uid1.apply();",
    ]

    assert generated_decl == expected_decl
    assert generated_apply == expected_apply


def test_equal_table_code_generation():
    UID.reset()
    env = Environment(
        [("a", uint32_t), ("b", uint32_t), ("t", bool_t)],
        [],
        [],
        [],
        [],
        "inp",
        "out",
        "met",
        None,
    )
    table = EqualTable("t", "a", "b", env)
    gc = table.get_generated_code()
    generated_decl = gc.get_decl().get_code().strip().split("\n")
    generated_apply = gc.get_apply().get_code().strip().split("\n")
    expected_decl = [
        "bit<32> difference_variable_uid2;",
        "action setter_action_uid3_true() {",
        "\thdr.inp.t = 1;",
        "}",
        "action setter_action_uid3_false() {",
        "\thdr.inp.t = 0;",
        "}",
        "table eval_table_uid1 {",
        "\tkey = {",
        "\t\tdifference_variable_uid2: exact;",
        "\t}",
        "\tactions = {",
        "\t\tsetter_action_uid3_true;",
        "\t\tsetter_action_uid3_false;",
        "\t}",
        "\tsize = 1;",
        "\tconst default_action = setter_action_uid3_false;",
        "\tconst entries = {",
        "\t\t0 : setter_action_uid3_true();",
        "\t}",
        "}",
    ]
    expected_apply = [
        "difference_variable_uid2 = hdr.inp.a - hdr.inp.b;",
        "eval_table_uid1.apply();",
    ]

    assert generated_decl == expected_decl
    assert generated_apply == expected_apply


def test_not_equal_table_code_generation():
    UID.reset()
    env = Environment(
        [("a", uint32_t), ("b", uint32_t), ("t", bool_t)],
        [],
        [],
        [],
        [],
        "inp",
        "out",
        "met",
        None,
    )
    table = NotEqualTable("t", "a", "b", env)
    gc = table.get_generated_code()
    generated_decl = gc.get_decl().get_code().strip().split("\n")
    generated_apply = gc.get_apply().get_code().strip().split("\n")
    expected_decl = [
        "bit<32> difference_variable_uid2;",
        "action setter_action_uid3_true() {",
        "\thdr.inp.t = 1;",
        "}",
        "action setter_action_uid3_false() {",
        "\thdr.inp.t = 0;",
        "}",
        "table eval_table_uid1 {",
        "\tkey = {",
        "\t\tdifference_variable_uid2: exact;",
        "\t}",
        "\tactions = {",
        "\t\tsetter_action_uid3_true;",
        "\t\tsetter_action_uid3_false;",
        "\t}",
        "\tsize = 1;",
        "\tconst default_action = setter_action_uid3_true;",
        "\tconst entries = {",
        "\t\t0 : setter_action_uid3_false();",
        "\t}",
        "}",
    ]
    expected_apply = [
        "difference_variable_uid2 = hdr.inp.a - hdr.inp.b;",
        "eval_table_uid1.apply();",
    ]

    assert generated_decl == expected_decl
    assert generated_apply == expected_apply


def test_assign_with_hash():
    env = Environment(
        [("a", uint32_t), ("b", uint32_t), ("t", bool_t)],
        [],
        [],
        [],
        [],
        "inp",
        "out",
        "met",
        None,
    )
    gc = AssignWithHash("a", "b", env).get_generated_code()
    generated_line = gc.get_apply().get_code()
    expected_line = "@in_hash{ hdr.inp.a = hdr.inp.b; }\n"
    assert generated_line == expected_line


def test_Digest():
    UID.reset()
    env = Environment(
        [],
        [],
        [],
        [],
        [],
        "inp",
        "out",
        "met",
        [SrcIp, UdpDstPort, UdpSrcPort],
        None,
    )
    digest = Digest(["hdr.ipv4.src", "hdr.udp.srcPort"], ["hdr.udp.dstPort"], env)
    gc = digest.get_generated_code()
    generated_deparser_decl = (
        gc.get_or_create("ingress_deparser_declaration").get_code().strip().split("\n")
    )
    generated_headers = gc.get_headers().get_code().strip().split("\n")
    generated_deparser_apply = (
        gc.get_or_create("ingress_deparser_apply").get_code().strip().split("\n")
    )
    generated_decl = gc.get_decl().get_code().strip().split("\n")
    expected_deparser_decl = ["Digest<generated_digest_uid4>() generated_digest_uid4;"]
    expected_headers = [
        "struct generated_digest_uid4{",
        "\tbit<32> src_uid2;",
        "\tbit<16> srcPort_uid3;",
        "}",
    ]
    expected_deparser_apply = [
        "if (ig_dprsr_md.digest_type==1){",
        "\tgenerated_digest_uid4.pack({hdr.ipv4.src,hdr.udp.srcPort});",
        "}",
    ]
    expected_decl = [
        "action setter_action_uid6() {",
        "\tig_dprsr_md.digest_type = 1;",
        "}",
        "action drop_packet() {",
        "\tig_dprsr_md.drop_ctl = 0x1;",
        "}",
        "table set_digest_or_drop_table_uid5 {",
        "\tkey = {",
        "\t\thdr.udp.dstPort: exact;",
        "\t}",
        "\tactions = {",
        "\t\tsetter_action_uid6;",
        "\t\tdrop_packet;",
        "\t}",
        "\tsize = 1;",
        "\tconst default_action = drop_packet;",
        "}",
    ]
    assert generated_deparser_decl == expected_deparser_decl
    assert generated_headers == expected_headers
    assert generated_deparser_apply == expected_deparser_apply
    assert generated_decl == expected_decl


def test_check_control_plane_set():
    UID.reset()
    env = Environment(
        [],
        [],
        [],
        [],
        [("allowed", bool_t)],
        "inp",
        "out",
        "met",
        [SrcIp, UdpSrcPort],
        None,
    )
    check_control_plane_set = CheckControlPlaneSet(
        ["hdr.ipv4.src", "hdr.udp.srcPort"], "allowed", env
    )
    gc = check_control_plane_set.get_generated_code()
    generated_decl = gc.get_decl().get_code().strip().split("\n")
    generated_apply = gc.get_apply().get_code().strip().split("\n")
    print(generated_apply)
    expected_decl = [
        "action setter_action_uid2_true() {",
        "\tallowed = 1;",
        "}",
        "action setter_action_uid2_false() {",
        "\tallowed = 0;",
        "}",
        "table exact_match_table_uid1 {",
        "\tkey = {",
        "\t\thdr.ipv4.src: exact;",
        "\t\thdr.udp.srcPort: exact;",
        "\t}",
        "\tactions = {",
        "\t\tsetter_action_uid2_true;",
        "\t\tsetter_action_uid2_false;",
        "\t}",
        "\tsize = 1;",
        "\tconst default_action = setter_action_uid2_false;",
        "}",
    ]
    expected_apply = ["exact_match_table_uid1.apply();"]
    assert generated_decl == expected_decl
    assert generated_apply == expected_apply

def test_xor_shared_array():
    UID.reset()
    env = Environment(
        [],
        [],
        [],
        [],
        [("map", uint32_t)],
        "inp",
        "out",
        "met",
        [SrcIp, UdpSrcPort],
        [SharedArray('register',uint16_t, uint32_t, 100)],
    )
    xor_shared_array = XORSharedArray("register", "map", 0, env = env)
    gc = xor_shared_array.get_generated_code()
    generated_apply = gc.get_apply().get_code().strip().split("\n")
    generated_decl = gc.get_decl().get_code().strip().split("\n")
    expected_decl = ['RegisterAction<bit<32>,bit<16>,bit<32>>(register) xor_shared_array_action_uid1 = {', 'void apply(inout bit<32> to_store){', '\t\tto_store = to_store ^ map;', '\t}', '};']
    expected_apply = ['xor_shared_array_action_uid1.execute(0);']
    assert generated_apply == expected_apply
    assert generated_decl == expected_decl
    
    UID.reset()
    env = Environment(
        [],
        [],
        [],
        [],
        [("map", uint32_t), ("result", uint32_t)],
        "inp",
        "out",
        "met",
        [SrcIp, UdpSrcPort],
        [SharedArray('register',uint16_t, uint32_t, 100)],
    )
    xor_shared_array = XORSharedArray("register", "map", 0, "result", env = env)
    gc = xor_shared_array.get_generated_code()
    generated_apply = gc.get_apply().get_code().strip().split("\n")
    generated_decl = gc.get_decl().get_code().strip().split("\n")
    expected_decl = ['RegisterAction<bit<32>,bit<16>,bit<32>>(register) xor_shared_array_action_uid1 = {', 'void apply(inout bit<32> to_store, out bit<32> to_return){', '\t\tto_store = to_store ^ map;', '\t\tto_return = to_store;', '\t}', '};']
    expected_apply = ['result = xor_shared_array_action_uid1.execute(0);']
    assert generated_apply == expected_apply
    assert generated_decl == expected_decl