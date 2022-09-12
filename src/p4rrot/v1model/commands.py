
from p4rrot.known_types import KnownType
from typing import Dict, List, Tuple
from p4rrot.standard_fields import *
from p4rrot.generator_tools import *
from p4rrot.checks import *
import random


class GetPacketLength(Command):
    
    def __init__(self,vname:str,env=None):
        self.vname = vname
        self.env = env

        if self.env!=None:
            self.check()

    def check(self):
        var_exists(self.vname,self.env)
        assert self.env.get_varinfo(self.vname)['type'] in [ uint8_t, uint16_t ,uint32_t, uint64_t ], 'Not supported type'
        is_writeable(self.vname,self.env)

    def get_generated_code(self):
        gc = GeneratedCode()
        vi = self.env.get_varinfo(self.vname)
        gc.get_apply().writeln('{} = standard_metadata.packet_length;'.format(vi['handle']))
        return gc

    def execute(self,test_env):
        pass

class AssignRandomValue(Command):
    
    def __init__(self,vname:str,min_value=0,max_value=1,env=None) -> None:
        self.vname = vname
        self.min_value = min_value
        self.max_value = max_value
        self.env = env

        if self.env!=None:
            self.check()

    def check(self):
        var_exists(self.vname,self.env)
        assert self.env.get_varinfo(self.vname)['type'] in [ uint8_t, uint16_t ,uint32_t, uint64_t ], 'Not supported random generation'
        target_type = self.env.get_varinfo(self.vname)['type']
        assert target_type.cast_value(self.min_value) < target_type.cast_value(self.max_value), 'Max is not greater than max. (Check for overflows too)'
        target_type.to_p4_literal(self.min_value)
        target_type.to_p4_literal(self.max_value)
        is_writeable(self.vname,self.env)

    def get_generated_code(self):
        gc = GeneratedCode()
        vi = self.env.get_varinfo(self.vname)
        gc.get_apply().writeln('random< {} >({},({}){},({}){});'.format(
            vi['type'].get_p4_type(), 
            vi['handle'], 
            vi['type'].get_p4_type(), 
            vi['type'].to_p4_literal(self.min_value), 
            vi['type'].get_p4_type(), 
            vi['type'].to_p4_literal(self.max_value))
            )
        return gc

    def execute(self,test_env):
        target_type = self.env.get_varinfo(self.vname)['type']
        test_env[self.vname] = random.randint(target_type.cast_value(self.min_value),target_type.cast_value(self.max_value))


class Truncate(Command):
    
    def __init__(self,length,env=None):
        self.length = length
        self.env = env
    
        if self.env!=None:
            self.check()
            
    def check(self):
        assert self.length>=0
    
    def get_generated_code(self):
        gc = GeneratedCode()
        gc.get_apply().writeln('truncate({});'.format(self.length))
        return gc
    
    def execute(self,test_env):
        pass



class TruncateRemainng(Command):
    
    def __init__(self,env=None):
        self.env = env
    
        if self.env!=None:
            self.check()
            
    def check(self):
        pass

    def get_generated_code(self):
        gc = GeneratedCode()
        gc.get_apply().writeln('truncate(meta.parsed_bytes + OUTPUT_HEADER_SIZE);')
        gc.get_apply().writeln('meta.truncated_to = meta.parsed_bytes + OUTPUT_HEADER_SIZE;')
        return gc
    
    def execute(self,test_env):
        pass


class ClonePacket(Command):
    
    def __init__(self,session,env=None):
        self.session = session
        self.env = env
    
        if self.env!=None:
            self.check()
            
    def check(self):
        pass

    def get_generated_code(self):
        gc = GeneratedCode()
        gc.get_apply().writeln('clone(CloneType.I2E, {});'.format(self.session))
        return gc
    
    def execute(self,test_env):
        pass