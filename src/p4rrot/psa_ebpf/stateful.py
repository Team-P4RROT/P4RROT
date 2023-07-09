from p4rrot.known_types import KnownType
from typing import Dict, List, Tuple
from p4rrot.standard_fields import *
from p4rrot.generator_tools import *

class RandomNumberGenerator(SharedElement):
    def __init__(self,vname:str, vtype:KnownType ,min_value=0,max_value=1,env=None) -> None:
        self.vname = vname
        self.vtype = vtype
        self.min_value = min_value
        self.max_value = max_value
        self.env = env
        self.properties = { 'min_value':self.min_value, 'max_value':self.max_value }

        if self.env!=None:
            self.check()

    def check(self):
        assert self.vtype in [ uint8_t, uint16_t ,uint32_t, uint64_t ], 'Not supported random generation'

    
    def get_name(self):
        return self.vname


    def get_type(self):
        return self.vtype

    
    def get_properties(self):
        return self.properties


    def get_generated_code(self):
        gc = GeneratedCode()
        gc.get_decl().writeln('Random< {} >(({}){},({}){}) {};'.format(
            self.vtype.get_p4_type(), 
            self.vtype.get_p4_type(), 
            self.vtype.to_p4_literal(self.min_value), 
            self.vtype.get_p4_type(), 
            self.vtype.to_p4_literal(self.max_value),
            self.vname)
            )
        return gc

    def execute(self,test_env):
        target_type = self.env.get_varinfo(self.vname)['type']
        test_env[self.vname] = random.randint(target_type.cast_value(self.min_value),target_type.cast_value(self.max_value))