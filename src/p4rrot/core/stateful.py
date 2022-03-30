
from p4rrot.known_types import KnownType
from typing import Dict, List, Tuple
from p4rrot.standard_fields import *
from p4rrot.generator_tools import *


class Const(SharedElement):
    def __init__(self,vname:str,vtype:KnownType,value):
        self.vaname = vname
        self.vtype = vtype
        self.value = value

    def get_name(self):
        return self.vaname

    def get_type(self):
        return self.vtype

    def get_generated_code(self):
        gc = GeneratedCode()
        gc.get_headers().writeln('const {} {} = {};'.format(self.vtype.get_p4_type(),
                                                         self.vaname, 
                                                         self.vtype.to_p4_literal(self.value)))
        return gc

    def get_repr(self):
        return self.vtype.cast_value(self.value)
