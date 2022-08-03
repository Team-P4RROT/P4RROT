import sys

sys.path.append("../../src/")

from p4rrot.tofino.helper import *
from p4rrot.generator_tools import *


def test_simple_table():
    expected_lines = [
        "table Teszt {",
        "\tkey = {",
        "\t\thdr.teszt1: exact;",
        "\t}",
        "\tactions = {",
        "\t\tteszt_action;",
        "\t}",
        "\tsize = 100;",
        "}",
    ]
    t = Table(
        "Teszt",
        ["teszt_action"],
        [{"name": "hdr.teszt1", "match_type": "exact"}],
        100,
        [],
    )
    out = t.get_generated_code().get_decl().get_code()
    line_list = out.strip().split("\n")
    assert line_list == expected_lines


def test_table_with_default_action():
    expected_lines = [
        "table Teszt {",
        "\tkey = {",
        "\t\thdr.teszt1: exact;",
        "\t}",
        "\tactions = {",
        "\t\tteszt_action;",
        "\t}",
        "\tsize = 100;",
        "\tconst default_action = teszt_action;",
        "}",
    ]
    t = Table(
        "Teszt",
        ["teszt_action"],
        [{"name": "hdr.teszt1", "match_type": "exact"}],
        100,
        [],
        "teszt_action",
    )
    out = t.get_generated_code().get_decl().get_code()
    line_list = out.strip().split("\n")
    assert line_list == expected_lines


def test_table_with_multiple_actions_and_entries():
    expected_lines = [
        "table Teszt {",
        "\tkey = {",
        "\t\thdr.teszt1: exact;",
        "\t}",
        "\tactions = {",
        "\t\tteszt_action1;",
        "\t\tteszt_action2;",
        "\t}",
        "\tsize = 100;",
        "\tconst default_action = teszt_action;",
        "\tconst entries = {",
        "\t\t12 : teszt_action1(1,2);",
        "\t\t42 : teszt_action2(4,0);",
        "\t}",
        "}",
    ]
    t = Table(
        "Teszt",
        ["teszt_action1", "teszt_action2"],
        [{"name": "hdr.teszt1", "match_type": "exact"}],
        100,
        [
            {"value": 12, "action": "teszt_action1", "parameters": ["1", "2"]},
            {"value": 42, "action": "teszt_action2", "parameters": ["4", "0"]},
        ],
        "teszt_action",
    )
    out = t.get_generated_code().get_decl().get_code()
    line_list = out.strip().split("\n")
    assert line_list == expected_lines


def test_shared_array_action():
    sharred_array_action_params = [
        {"type": uint16_t, "mode": "inout", "name": "register_data"},
        {"type": uint16_t, "mode": "out", "name": "out_data"},
    ]

    apply_lines = ["register_data = register_data + 1;", "out_data = register_data;"]
    using = SharedArrayAction(
        "action_1",
        "shared_a_1",
        uint16_t,
        uint16_t,
        uint16_t,
        sharred_array_action_params,
        apply_lines,
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
