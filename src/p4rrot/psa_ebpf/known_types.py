from p4rrot.known_types import *  

class timestamp_t(KnownType):

    def get_p4_type() -> str:
        return 'Timestamp_t'

    def get_size() -> int:
        return 8

    def to_p4_literal(v):
        return str(timestamp_t.cast_value(v))
    
    def cast_value(v):
        if type(v)==int:
            return ctypes.c_uint64(v).value
        raise Exception('Can not recognize value {}'.format(v))  