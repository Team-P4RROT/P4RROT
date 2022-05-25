import sys

sys.path.append("../../src/")

from p4rrot.core.commands import *
from p4rrot.tofino.commands import *


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
    env = Environment([("a", uint32_t)], [], [], [], "inp", "out", "met", None)
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
    env = Environment([("a", uint32_t)], [], [], [], "inp", "out", "met", None)
    decrement_shared_arr = DecrementSharedArray(
        "shared_a_1", uint32_t, uint16_t, 3, read_new_to="a", env=env
    )
    decrement_shared_arr.check()


def test_write_shared_array_code_generation():
    UID.reset()
    env = Environment([("a", uint32_t)], [], [], [], "inp", "out", "met", None)
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
    env = Environment([("b", uint32_t)], [], [], [], "inp", "out", "met", None)
    write_shared_arr = WriteSharedArray(
        "shared_a_1", uint32_t, uint16_t, 3, 100, read_old_to="b", env=env
    )
    write_shared_arr.check()


def test_read_shared_array_code_generation():
    UID.reset()
    env = Environment([("a", uint32_t)], [], [], [], "inp", "out", "met", None)
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
    env = Environment([("b", uint32_t)], [], [], [], "inp", "out", "met", None)
    read_shared_arr = ReadSharedArray(
        "shared_a_1", uint32_t, uint16_t, 3, read_to="b", env=env
    )
    read_shared_arr.check()
