#
# Classes representing available types and their P4 equivalent.
#
from typing import Dict, List, Tuple
import ctypes

class KnownType:
    """
    Base class of available types.
    """
    pass


class uint8_t(KnownType):

    def get_p4_type() -> str:
        return 'bit<8>'

    def get_size() -> int:
        return 1

    def to_p4_literal(v):
        return str(uint8_t.cast_value(v))
    
    def cast_value(v):
        if type(v)==int:
            return ctypes.c_uint8(v).value
        raise Exception('Can not recignize value {}'.format(v))        


class uint16_t(KnownType):

    def get_p4_type() -> str:
        return 'bit<16>'

    def get_size() -> int:
        return 2

    def to_p4_literal(v):
        return str(uint16_t.cast_value(v))
    
    def cast_value(v):
        if type(v)==int:
            return ctypes.c_uint16(v).value
        raise Exception('Can not recignize value {}'.format(v))        


class uint32_t(KnownType):

    def get_p4_type() -> str:
        return 'bit<32>'

    def get_size() -> int:
        return 4

    def to_p4_literal(v):
        return str(uint32_t.cast_value(v))
    
    def cast_value(v):
        if type(v)==int:
            return ctypes.c_uint32(v).value
        raise Exception('Can not recignize value {}'.format(v))        


class uint64_t(KnownType):

    def get_p4_type() -> str:
        return 'bit<64>'

    def get_size() -> int:
        return 8

    def to_p4_literal(v):
        return str(uint64_t.cast_value(v))
    
    def cast_value(v):
        if type(v)==int:
            return ctypes.c_uint64(v).value
        raise Exception('Can not recignize value {}'.format(v))        

class bool_t(KnownType):

    def get_p4_type() -> str:
        return 'BOOL_T' # defined as bit<8>

    def get_size() -> int:
        return 1

    def to_p4_literal(v):
        return str(bool_t.cast_value(v))
    
    def cast_value(v):
        if v==True:
            return 1
        if v==False:
            return 0
        raise Exception('Can not recignize value {}'.format(v))     

def padding_t(width:int):
    if width<=0:
        raise ValueError('width must be positive')

    class hidden_padding_t(KnownType):
        def get_p4_type() -> str:
            return 'bit<{}>'.format(width*8) 

        def get_size() -> int:
            return width

        def to_p4_literal(v):
            raise Exception('Padding variables can not be transleted to literals.')
        
        def cast_value(v):
            raise Exception('Padding variables do not have values.')

    return hidden_padding_t    



def hdr_len(description: List[Tuple[str, KnownType]]):
    '''
    Returns the length of the described header in bytes. It does NOT consider alignments.
    '''
    return sum(map(lambda p: p[1].get_size(), description))
