from p4rrot.known_types import KnownType
from typing import Dict, List, Tuple
from p4rrot.standard_fields import *
from p4rrot.generator_tools import *
from enum import Enum


class SupportedHashAlgo(Enum):
    IDENTITY="IDENTITY"
    CRC32 = "CRC32"
    CRC32_CUSTOM = "CRC32_CUSTOM"
    CRC16 = "CRC16"
    CRC16_CUSTOM = "CRC16_CUSTOM"
    ONES_COMPLEMENT16 = "ONES_COMPLEMENT16"
    TARGET_DEFAULT = "TARGET_DEFAULT"

class HashGenerator(SharedElement):
    def __init__(self, vname: str, vtype: KnownType, algo: SupportedHashAlgo, env=None):
        self.vname = vname
        self.vtype = vtype
        self.algo = algo
        self.properties = {
            'algo': algo.value
        }
        if env != None:
            self.check()

    def check(self):
        assert self.vtype in [ uint8_t, uint16_t ,uint32_t, uint64_t ], 'vtype needs to be an unsigned int'

    def get_name(self):
        return self.vname

    def get_type(self):
        return self.vtype

    def get_properties(self):
        return self.properties

    def get_generated_code(self):
        gc = GeneratedCode()
        gc.get_decl().writeln('Hash<{}>(PSA_HashAlgorithm_t.{}) {};'.format(
            self.vtype.get_p4_type(),
            self.algo.value,
            self.vname))
        return gc

    def execute(self):
        raise NotImplementedError
