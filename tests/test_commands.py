import sys

sys.path.append("./src/")

from p4rrot.core.commands import *
from p4rrot.v1model.commands import *


def test_assign_const():
    assert (
        "hdr.inp.a = 5;\n"
        == AssignConst(
            "a",
            5,
            Environment(
                [("a", uint32_t), ("b", uint32_t)],
                [],
                [],
                [],
                None,
                "inp",
                "out",
                "met",
                None,
            ),
        )
        .get_generated_code()
        .get_apply()
        .get_code()
    )


def test_logical_not():
    UID.reset()
    env = Environment(
        [],
        [],
        [],
        [],
        [("some_bool", bool_t)],
        "inp",
        "out",
        "met",
        [SrcIp, UdpSrcPort],
        None,
    )
    logical_not = LogicalNot("some_bool", env)
    gc = logical_not.get_generated_code()
    generated_apply = gc.get_apply().get_code().strip().split("\n")
    expected_apply = ["some_bool = some_bool ^ 1;"]
    assert generated_apply == expected_apply

def test_logical_or():
    UID.reset()
    env = Environment(
        [],
        [],
        [],
        [],
        [("bool_a", bool_t),("bool_b", bool_t),("bool_c", bool_t)],
        "inp",
        "out",
        "met",
        [],
        None,
    )
    logical_or = LogicalOr("bool_a", "bool_b", "bool_c", env)
    gc = logical_or.get_generated_code()
    generated_apply = gc.get_apply().get_code().strip().split("\n")
    expected_apply = ['bool_a = bool_b | bool_c;']
    assert generated_apply == expected_apply

def test_left_shift():
    UID.reset()
    env = Environment(
        [],
        [],
        [],
        [],
        [("some_number", uint32_t)],
        "inp",
        "out",
        "met",
        [],
        None,
    )
    left_shit = LeftShift("some_number", 3, env)
    gc = left_shit.get_generated_code()
    generated_apply = gc.get_apply().get_code().strip().split("\n")
    print(generated_apply)
    expected_apply = ['some_number = some_number << 3;']
    assert generated_apply == expected_apply

def test_right_shift():
    UID.reset()
    env = Environment(
        [],
        [],
        [],
        [],
        [("some_number", uint32_t)],
        "inp",
        "out",
        "met",
        [],
        None,
    )
    right_shit = RightShift("some_number", 3, env)
    gc = right_shit.get_generated_code()
    generated_apply = gc.get_apply().get_code().strip().split("\n")
    expected_apply = ['some_number = some_number >> 3;']
    assert generated_apply == expected_apply

def test_greater_than():
    UID.reset()
    env = Environment(
        [],
        [],
        [],
        [],
        [("a", uint32_t), ("b", uint32_t), ("result", bool_t)],
        "inp",
        "out",
        "met",
        [],
        None,
    )
    greater_than = GreaterThan("result", "a", "b", env)
    gc = greater_than.get_generated_code()
    generated_apply = gc.get_apply().get_code().strip().split("\n")
    print(generated_apply)
    expected_apply = ['result = (BOOL_T)(bit<1>)(a > b);']
    assert generated_apply == expected_apply

def test_less_than():
    UID.reset()
    env = Environment(
        [],
        [],
        [],
        [],
        [("a", uint32_t), ("b", uint32_t), ("result", bool_t)],
        "inp",
        "out",
        "met",
        [],
        None,
    )
    less_than = LessThan("result", "a", "b", env)
    gc = less_than.get_generated_code()
    generated_apply = gc.get_apply().get_code().strip().split("\n")
    expected_apply = ['result = (BOOL_T)(bit<1>)(a < b);']
    assert generated_apply == expected_apply

def test_masked_not_equals_const():
    UID.reset()
    env = Environment(
        [],
        [],
        [],
        [],
        [("number", uint32_t), ("result", bool_t) ],
        "inp",
        "out",
        "met",
        [],
        None,
    )
    masked_not_equals_const = MaskedNotEqualsConst("result", "number", 2, 12, env)
    gc = masked_not_equals_const.get_generated_code()
    generated_apply = gc.get_apply().get_code().strip().split("\n")
    expected_apply = ['result = (BOOL_T)(bit<1>)(number & 2 != 12);']
    assert generated_apply == expected_apply

def test_masked_equals_const():
    UID.reset()
    env = Environment(
        [],
        [],
        [],
        [],
        [("number", uint32_t), ("result", bool_t) ],
        "inp",
        "out",
        "met",
        [],
        None,
    )
    masked_equals_const = MaskedEqualsConst("result", "number", 2, 12, env)
    gc = masked_equals_const.get_generated_code()
    generated_apply = gc.get_apply().get_code().strip().split("\n")
    expected_apply = ['result = (BOOL_T)(bit<1>)(number & 2 == 12);']
    assert generated_apply == expected_apply


def test_get_packet_length():
    UID.reset()
    env = Environment(
        [],
        [],
        [],
        [],
        [("length", uint32_t)],
        "inp",
        "out",
        "met",
        [],
        None,
    )
    get_packet_length = GetPacketLength("length", env)
    gc = get_packet_length.get_generated_code()
    generated_apply = gc.get_apply().get_code().strip().split("\n")
    expected_apply = ['length = standard_metadata.packet_length;']
    assert generated_apply == expected_apply

def test_increment():
    UID.reset()
    env = Environment(
        [],
        [],
        [],
        [],
        [("number", uint32_t)],
        "inp",
        "out",
        "met",
        [],
        None,
    )
    increment = Increment("number", 3, env)
    gc = increment.get_generated_code()
    generated_apply = gc.get_apply().get_code().strip().split("\n")
    expected_apply = ['number = number + 3;']
    assert generated_apply == expected_apply

def test_clone_packet():
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
        [],
        None,
    )
    clone_packet = ClonePacket(250, env)
    gc = clone_packet.get_generated_code()
    generated_apply = gc.get_apply().get_code().strip().split("\n")
    expected_apply = ['clone(CloneType.I2E, 250);']
    assert generated_apply == expected_apply

    
def test_expr_to_p4():
    class FakeEnv(Environment):
        def __init__(self):
            pass

        def get_varinfo(self,v):
            return {'handle':'replaced_'+v}
    assert expr_to_p4('a = a.a + a + b + c/**/',FakeEnv()) == 'replaced_a = a.a + replaced_a + replaced_b + c/**/'

    