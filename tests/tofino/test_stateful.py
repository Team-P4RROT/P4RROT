import sys

sys.path.append("../../src/")

from p4rrot.tofino.stateful import *
from p4rrot.generator_tools import *


def test_shared_variable_name():
    shared = SharedVariable("shared_v_1", uint8_t)
    assert "shared_v_1" == shared.get_name()


def test_shared_variable_type():
    shared = SharedVariable("shared_v_2", uint8_t)
    print(shared.get_type())
    assert (SharedVariable, uint8_t) == shared.get_type()


def test_shared_variable_generated_code():
    shared = SharedVariable("shared_v_3", uint16_t)
    generated = shared.get_generated_code().get_decl().get_code()
    out_line = generated.strip()
    assert out_line == "Register< bit<16>, bit<8> >(1) shared_v_3;"


def test_shared_variable_repr():
    shared = SharedVariable("shared_v_3", uint16_t)
    assert shared.get_repr() == [None]


# vname:str,vtype:KnownType, itype:KnownType, size:int):


def test_shared_array_name():
    shared = SharedArray("shared_a_1", uint32_t, uint16_t, 1000)
    assert "shared_a_1" == shared.get_name()


def test_shared_array_type():
    shared = SharedArray("shared_a_2", uint32_t, uint16_t, 1000)
    assert (SharedArray, uint32_t, uint16_t, 1000) == shared.get_type()


def test_shared_array_generated_code():
    shared = SharedArray("shared_a_3", uint32_t, uint16_t, 1000)
    generated = shared.get_generated_code().get_decl().get_code()
    out_line = generated.strip()
    print(out_line)
    assert out_line == "Register< bit<32>, bit<16> >(1000) shared_a_3;"

def test_shared_array_repr():
    shared = SharedArray("shared_a_4", uint32_t, uint8_t, 10)
    assert shared.get_repr() == [None] * 10
