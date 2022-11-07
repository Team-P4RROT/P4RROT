
from p4rrot.known_types import KnownType
from typing import Dict, List, Tuple
from p4rrot.standard_fields import *
from p4rrot.generator_tools import *


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
        gc.get_decl().writeln('Register< {}, {} >(1) {};'.format(self.vtype.get_p4_type(),uint8_t.get_p4_type(),self.vaname))
        return gc

    def get_repr(self):
        return [ None ]


class SharedArray(SharedElement):

    def __init__(self,vname:str,vtype:KnownType, itype:KnownType, size:int):
        self.vaname = vname
        self.vtype = vtype
        self.itype = itype
        self.size = size

    def get_name(self):
        return self.vaname

    def get_type(self):
        return (SharedArray,self.vtype, self.itype, self.size)

    def get_generated_code(self):
        gc = GeneratedCode()
        gc.get_decl().writeln('Register< {}, {} >({}) {};'.format(self.vtype.get_p4_type(), self.itype.get_p4_type(),self.size,self.vaname))
        return gc

    def get_repr(self):
        return [None]*self.size


class LPF(SharedElement):
    def __init__(self,vname:str,vtype:KnownType,itype:KnownType,size:int):
        self.vaname = vname
        self.vtype = vtype
        self.itype = itype
        self.size = size

    def get_name(self):
        return self.vaname

    def get_type(self):
        return (LPF,self.vtype,self.itype,self.size)

    def get_generated_code(self):
        gc = GeneratedCode()
        gc.get_decl().writeln(f'Lpf< {self.vtype.get_p4_type()}, {self.itype.get_p4_type()} >({self.size}) {self.vaname};')
        return gc

    def get_repr(self):
        raise Exception("Not implemented")