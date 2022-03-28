
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
        gc.get_decl().writeln('#pragma netro reglocked register')
        gc.get_decl().writeln('register< {} >(1) {};'.format(self.vtype.get_p4_type(),self.vaname))
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
        gc.get_apply().writeln('{}.read({},0);'.format(s['handle'],t['handle']))
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
        gc.get_apply().writeln('{}.write(0,{});'.format(t['handle'],s['handle']))
        return gc

    def execute(self,test_env):
        test_env[self.target][0] = test_env[self.source]



class SharedArray(SharedElement):

    def __init__(self,vname:str,vtype:KnownType,size:int):
        self.vaname = vname
        self.vtype = vtype
        self.size = size

    def get_name(self):
        return self.vaname

    def get_type(self):
        return (SharedArray,self.vtype,self.size)

    def get_generated_code(self):
        gc = GeneratedCode()
        gc.get_decl().writeln('#pragma netro reglocked register')
        gc.get_decl().writeln('register< {} >({}) {};'.format(self.vtype.get_p4_type(),self.size,self.vaname))
        return gc

    def get_repr(self):
        return [None]*self.size



class ReadFromSharedAt(Command):
    
    def __init__(self,target:str,source:str,idx_vname:str,env=None):
        self.target = target
        self.source = source
        self.idx_vname = idx_vname
        self.env = env
        if env!=None:
            self.check()

    def check(self):
        assert self.env.has_var(self.source), 'Undefined name: {}'.format(self.source)
        assert self.env.has_var(self.target), 'Undefined name: {}'.format(self.target)
        assert self.env.has_var(self.idx_vname), 'Undefined name: {}'.format(self.idx_vname)
        assert self.env.get_varinfo(self.idx_vname)['type'] == uint32_t , 'Index should be uint32_t'
        assert self.env.get_varinfo(self.source)['type'][0] == SharedArray, 'This method should be applied on SharedVariables only'
        assert self.env.get_varinfo(self.source)['type'][1] == self.env.get_varinfo(self.target)['type'], 'Type mismatch'

    def get_generated_code(self):
        gc = GeneratedCode()
        s = self.env.get_varinfo(self.source)
        t = self.env.get_varinfo(self.target)
        idx = self.env.get_varinfo(self.idx_vname)
        gc.get_apply().writeln('{}.read({},{});'.format(s['handle'],t['handle'],idx['handle']))
        return gc

    def execute(self,test_env):
        s = self.env.get_varinfo(self.source)
        if test_env[self.idx_vname]>=s['type'][2]:
            raise Exception('{}[{}] : Value {} is out of range 0..{}'.format(self.source),test_env[self.idx_vname],test_env[self.idx_vname],s['type'][2]-1)
        test_env[self.target] = test_env[self.source][test_env[self.idx_vname]]



class WriteToSharedAt(Command):
    
    def __init__(self,target:str,idx_vname:str,source:str,env=None):
        self.target = target
        self.source = source
        self.idx_vname = idx_vname
        self.env = env
        if env!=None:
            self.check()

    def check(self):
        assert self.env.has_var(self.source), 'Undefined name: {}'.format(self.source)
        assert self.env.has_var(self.target), 'Undefined name: {}'.format(self.target)
        assert self.env.has_var(self.idx_vname), 'Undefined name: {}'.format(self.idx_vname)
        assert self.env.get_varinfo(self.idx_vname)['type'] == uint32_t , 'Index should be uint32_t'
        assert self.env.get_varinfo(self.target)['type'][0] == SharedArray, 'This method should be applied on SharedVariables only'
        assert self.env.get_varinfo(self.target)['type'][1] == self.env.get_varinfo(self.source)['type'], 'Type mismatch'

    def get_generated_code(self):
        gc = GeneratedCode()
        s = self.env.get_varinfo(self.source)
        t = self.env.get_varinfo(self.target)
        idx = self.env.get_varinfo(self.idx_vname)
        gc.get_apply().writeln('{}.write({},{});'.format(t['handle'],idx['handle'],s['handle']))
        return gc

    def execute(self,test_env):
        t = self.env.get_varinfo(self.target)
        if test_env[self.idx_vname]>=t['type'][2]:
            raise Exception('{}[{}] : Value {} is out of range 0..{}'.format(self.target),test_env[self.idx_vname],test_env[self.idx_vname],t['type'][2]-1)
        test_env[self.target][test_env[self.idx_vname]] = test_env[self.source]



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
