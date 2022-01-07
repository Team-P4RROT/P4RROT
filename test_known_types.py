from known_types import *


def test_hdr_len():
    assert hdr_len([]) == 0
    assert hdr_len([('a',uint8_t)]) == 1
    assert hdr_len([('a',uint16_t)]) == 2
    assert hdr_len([('a',uint16_t),('b',uint32_t)]) == 6  # no alignment 
    assert hdr_len([('a',uint64_t),('b',uint32_t)]) == 12  
    assert hdr_len([('a',bool_t)]) == 1


def test_uint_casts():
    assert uint64_t.cast_value(78657452)==78657452
    assert uint32_t.cast_value(0)==0
    assert uint16_t.cast_value(5)==5
    assert uint8_t.cast_value(-1)==255
    assert uint8_t.cast_value(256)==0

def test_bool_cast():
    assert bool_t.cast_value(True)==1
    assert bool_t.cast_value(False)==0

def test_padding_types():
    assert hdr_len([('_p',padding_t(5))]) == 5
    assert hdr_len([('a',uint8_t),('_p',padding_t(3))]) == 4




