from p4rrot.known_types import KnownType
from typing import Dict, List, Tuple
from p4rrot.standard_fields import *
from p4rrot.generator_tools import *
from enum import Enum
import random


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


class SharedVariable(SharedElement):
    
    def __init__(self,vname:str,vtype:KnownType):
        self.vaname = vname
        self.vtype = vtype

    def get_name(self):
        return self.vaname

    def get_type(self):
        return (SharedVariable,self.vtype)

    def get_generated_code(self):
        gc = GeneratedCode()
        gc.get_decl().writeln('#pragma netro reglocked register')
        gc.get_decl().writeln('Register<{}, bit<32>>(1) {};'.format(self.vtype.get_p4_type(), self.vaname))
        return gc

    def get_repr(self):
        return [ None ]


class ReadFromShared(Command):
    
    def __init__(self,target:str,source:str,env=None):
        self.target = target
        self.source = source
        self.env = env
        if env!=None:
            self.check()

    def check(self):
        assert self.env.has_var(self.source), 'Undefined name: {}'.format(self.source)
        assert self.env.has_var(self.target), 'Undefined name: {}'.format(self.target)
        assert self.env.get_varinfo(self.source)['type'][0] == SharedVariable, 'This method should be applied on SharedVariables only'
        assert self.env.get_varinfo(self.source)['type'][1] == self.env.get_varinfo(self.target)['type'], 'Type mismatch'

    def get_generated_code(self):
        gc = GeneratedCode()
        s = self.env.get_varinfo(self.source)
        t = self.env.get_varinfo(self.target)
        read_idx_name = "read_idx_"+UID.get()
        gc.get_apply().writeln(f"bit<32> {read_idx_name} = 0;")
        gc.get_apply().writeln('{} = {}.read({});'.format(t['handle'], s['handle'], read_idx_name))
        return gc

    def execute(self,test_env):
        test_env[self.target] = test_env[self.source][0]

class WriteToShared(Command):
    
    def __init__(self,target:str,source:str,env=None):
        self.target = target
        self.source = source
        self.env = env
        if env!=None:
            self.check()

    def check(self):
        assert self.env.has_var(self.source), 'Undefined name: {}'.format(self.source)
        assert self.env.has_var(self.target), 'Undefined name: {}'.format(self.target)
        assert self.env.get_varinfo(self.target)['type'][0] == SharedVariable, 'This method should be applied on SharedVariables only'
        assert self.env.get_varinfo(self.target)['type'][1] == self.env.get_varinfo(self.source)['type'], 'Type mismatch'

    def get_generated_code(self):
        gc = GeneratedCode()
        s = self.env.get_varinfo(self.source)
        t = self.env.get_varinfo(self.target)
        write_idx_name = "write_idx_"+UID.get()
        gc.get_apply().writeln(f"bit<32> {write_idx_name} = 0;")
        gc.get_apply().writeln('{}.write({},{});'.format(t['handle'],write_idx_name, s['handle']))
        return gc

    def execute(self,test_env):
        test_env[self.target][0] = test_env[self.source]
