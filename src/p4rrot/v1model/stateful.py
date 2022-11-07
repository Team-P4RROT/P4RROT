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


# A stack storing a given type of element with a fixed maximum capacity
class SharedStack(SharedElement):

    def __init__(self,vname:str,vtype:KnownType,capacity:int):
        self.vaname = vname
        self.index_name = '_' + self.vaname + '_idx'
        self.temp_name = '_'+ self.vaname + "_temp"
        self.vtype = vtype
        self.capacity = capacity
        self.current_size = 0

    def get_name(self):
        return self.vaname

    def get_type(self):
        return (SharedStack,self.vtype,self.capacity)

    def get_generated_code(self):
        gc = GeneratedCode()
        gc.get_decl().writeln('#pragma netro reglocked register')
        gc.get_decl().writeln('register< {} >({}) {};'.format(self.vtype.get_p4_type(),self.capacity,self.vaname))
        gc.get_decl().writeln('register< {} >(1) {};'.format(uint32_t.get_p4_type(), self.index_name))
        gc.get_decl().writeln('{} {};'.format(uint32_t.get_p4_type(), self.temp_name))
        return gc


# Pops an element from a SharedStack, putting its value to the variable specified in the value parameter
class PopFromStack(Command):

    def __init__(self,stack:str,value:str,env=None):
        self.stack = stack
        self.value = value
        self.index_name = '_' + self.stack + '_idx'
        self.temp_name = '_' + self.stack + '_temp'
        self.env = env
        if env!=None:
            self.check()

    def check(self):
        True

    def get_generated_code(self):
        gc = GeneratedCode()
        v = self.env.get_varinfo(self.value)
        s = self.env.get_varinfo(self.stack)
        gc.get_apply().writeln('{}.read({},0);'.format(self.index_name, self.temp_name))
        gc.get_apply().writeln('{} = {} - 1;'.format(self.temp_name, self.temp_name))
        gc.get_apply().writeln('{}.read({},{});'.format(s['handle'],v['handle'], self.temp_name))
        gc.get_apply().writeln('{}.write(0,{});'.format(self.index_name,self.temp_name))
        return gc



# Adds an element on top of a SharedStack
class PushToStack(Command):

    def __init__(self,stack:str,value:str,env=None):
        self.stack = stack
        self.value = value
        self.index_name = '_' + self.stack + '_idx'
        self.temp_name = '_' + self.stack + '_temp'
        self.env = env
        if env!=None:
            self.check()

    def check(self):
       True

    def get_generated_code(self):
        gc = GeneratedCode()
        s = self.env.get_varinfo(self.stack)
        v = self.env.get_varinfo(self.value)
        gc.get_apply().writeln('{}.read({},0);'.format(self.index_name, self.temp_name))
        gc.get_apply().writeln('{}.write({},{});'.format(s['handle'],self.temp_name, v['handle']))
        gc.get_apply().writeln('{} = {} + 1;'.format(self.temp_name, self.temp_name))
        gc.get_apply().writeln('{}.write(0,{});'.format(self.index_name,self.temp_name))
        return gc

#Improvement on the original BloomFilter implementation to accept a tuple of values and possibly use 2 hash functions
class GeneralBloomFilter(SharedElement):

    def __init__(self,vname:str,vtype:KnownType,capacity:int, number_of_hashes: int, use_two_hash_funcs: bool = False):
        self.vaname = vname
        self.reg_name_1 = '_' + vname + '_register_1'
        self.reg_name_2 = '_' + vname + '_register_2'
        self.vtype = vtype
        self.capacity = capacity
        self.two_hash_funcs = use_two_hash_funcs
        
        self.value_check = '_' + self.vaname + '_value_check' + UID.get()
        self.hash_name_1 = '_' + self.vaname + '_hash_1' + UID.get()
        self.hash_name_2 = '_' + self.vaname + '_hash_2' + UID.get()
        self.hashres_name_1 = '_' + self.vaname + '_result_1' + UID.get()
        self.hashres_name_2 = '_' + self.vaname + '_result_2' + UID.get()
        self.properties = {'capacity': capacity, 'hash_name_1' : self.hash_name_1, 'two_hash_funcs' : self.two_hash_funcs,
        "reg_name_1" : self.reg_name_1, "reg_name_2" : self.reg_name_2, "hashres_name_1" : self.hashres_name_1, "hashres_name_2" : self.hashres_name_2}

    def get_properties(self):
        return self.properties

    def get_name(self):
        return self.vaname

    def get_type(self):
        return (SharedStack,self.vtype,self.capacity)

    def get_generated_code(self):
        gc = GeneratedCode()
        gc.get_decl().writeln('#pragma netro reglocked register')
        gc.get_decl().writeln('register< bit<32> >({}) {};'.format(self.capacity, self.reg_name_1))
        gc.get_decl().writeln('{} {};'.format(uint32_t.get_p4_type(), self.value_check))
        gc.get_decl().writeln('{} {};'.format(uint32_t.get_p4_type(), self.hash_name_1))
        if self.two_hash_funcs:
            gc.get_decl().writeln('register< bit<32> >({}) {};'.format(self.capacity, self.reg_name_2))
            gc.get_decl().writeln('{} {};'.format(uint32_t.get_p4_type(), self.hash_name_2))
            gc.get_decl().writeln('bit<32> {};'.format(self.hashres_name_2))
        gc.get_decl().writeln('bit<32> {};'.format(self.hashres_name_1))
        return gc

class GeneralMaybeContains(Command):
    
    def __init__(self,result: str, bloom_filter:str,values:List,env=None):
        self.bloom_filter = bloom_filter
        self.values = values
        self.env = env
        self.result_var_name = result
        if env!=None:
            self.check()

    def check(self):
        pass
        
    def get_generated_code(self):
        gc = GeneratedCode()
        bloom_filter = self.env.get_varinfo(self.bloom_filter)
        values = [(self.env.get_varinfo(value)["handle"]) for value in self.values]
        properties = bloom_filter['properties']
        self.result = self.env.get_varinfo(self.result_var_name)['handle']        
        gc.get_apply().writeln('hash({}, HashAlgorithm.crc16, (bit<32>) 0, {{{}}}, 32w15);'.format(properties["hash_name_1"], ",".join(values)))
        if properties["two_hash_funcs"]:
            gc.get_apply().writeln('hash({}, HashAlgorithm.csum16, (bit<32>) 0, {{{}}}, 32w15);'.format(bloomfilter.hash_name_2, ",".join(values)))
        gc.get_apply().writeln('{}.read({}, {});'.format(properties["reg_name_1"], properties["hashres_name_1"], properties["hash_name_1"]))
        if properties["two_hash_funcs"]:
            gc.get_apply().writeln('{}.read({}, {});'.format(properties["reg_name_2"], properties["hashres_name_2"], properties["hash_name_2"]))
        gc.get_apply().writeln( '{} = 0;'.format(self.result_var_name))
        if properties["two_hash_funcs"]:            
            gc.get_apply().writeln('if ({} > 0 && {} > 0)'.format(bloomfilter.hashres_name_1, bloomfilter.hashres_name_2) + '{')
        else:
            gc.get_apply().writeln('if ({} > 0)'.format(properties["hashres_name_1"]) + '{')
        gc.get_apply().increase_indent()
        gc.get_apply().writeln( '{} = 1;'.format(self.result_var_name))
        gc.get_apply().decrease_indent()
        gc.get_apply().writeln('};')

        return gc

class GeneralPutIntoBloom(Command):
    
    def __init__(self, bloom_filter:str,values:str,env=None):
        self.bloom_filter = bloom_filter
        self.values = values
        self.env = env
        if env!=None:
            self.check()

    def check(self):
        True
        
    def get_generated_code(self):
        gc = GeneratedCode()
        bloom_filter = self.env.get_varinfo(self.bloom_filter)
        values = [(self.env.get_varinfo(value)["handle"]) for value in self.values]
        properties = bloom_filter['properties']      
        gc.get_apply().writeln('hash({}, HashAlgorithm.crc16, (bit<32>) 0, {{{}}}, 32w15);'.format(properties["hash_name_1"], ",".join(values)))
        if properties["two_hash_funcs"]:
            gc.get_apply().writeln('hash({}, HashAlgorithm.csum16, (bit<32>) 0, {{{}}}, 32w15);'.format(bloomfilter.hash_name_2, ",".join(values)))
        gc.get_apply().writeln('{}.read({}, {});'.format(properties["reg_name_1"], properties["hashres_name_1"], properties["hash_name_1"]))
        gc.get_apply().writeln('{} = {} + 1;'.format(properties["hashres_name_1"], properties["hashres_name_1"]))
        gc.get_apply().writeln('{}.write({}, {});'.format(properties["reg_name_1"], properties["hashres_name_1"], properties["hash_name_1"]))
        if properties["two_hash_funcs"]:
            gc.get_apply().writeln('{}.read({}, {});'.format(properties["reg_name_2"], properties["hashres_name_2"], properties["hash_name_2"]))
            gc.get_apply().writeln('{} = {} + 1;'.format(properties["hashres_name_2"], properties["hashres_name_2"]))
            gc.get_apply().writeln('{}.write({}, {});'.format(properties["reg_name_2"], properties["hashres_name_2"], properties["hash_name_2"]))

        return gc

# A Bloom filter is a probabilistic data structure.
# False positive matches are possible, but false negatives are not.
# Elements can be added to the set, but not removed.
# This implementation uses the crc16 hash algorithm with a salt. You can specify in the parameter how many hashes to use.
# The bits are stored in a register, whose size can be specified in the capacity parameter.
class BloomFilter(SharedElement):

    def __init__(self,vname:str,vtype:KnownType,capacity:int, number_of_hashes: int):
        self.vaname = vname
        self.reg_name = '_' + vname + '_register'
        self.index_name = '_' + self.reg_name + '_idx'
        self.temp_name = '_' + self.reg_name + "_temp"
        self.vtype = vtype
        self.capacity = capacity
        
        self.value_check = '_' + self.vaname + '_value_check'
        self.hash_name = '_' + self.vaname + '_hash'
        self.salt_name = '_' + self.vaname + '_salt'
        self.hashres_name = '_' + self.vaname + '_result'
        self.properties = {'capacity': capacity, 'number_of_hashes': number_of_hashes}

    def get_properties(self):
        return self.properties

    def get_name(self):
        return self.vaname

    def get_type(self):
        return (SharedStack,self.vtype,self.capacity)

    def get_generated_code(self):
        gc = GeneratedCode()
        gc.get_decl().writeln('#pragma netro reglocked register')
        gc.get_decl().writeln('register< bit<1> >({}) {};'.format(self.capacity, self.reg_name))
        gc.get_decl().writeln('{} {};'.format(uint32_t.get_p4_type(), self.value_check))
        gc.get_decl().writeln('{} {};'.format(uint32_t.get_p4_type(), self.index_name))
        gc.get_decl().writeln('{} {};'.format(uint32_t.get_p4_type(), self.temp_name))
        gc.get_decl().writeln('{} {};'.format(uint32_t.get_p4_type(), self.hash_name))
        gc.get_decl().writeln('bit<1> {};'.format(self.hashres_name))
        return gc


# Checks whether a value (of a variable) is possibly in the bloom filter.
# May return true even when the element is not in it (false positive) but never returns false for an element it contains.
class MaybeContains(Command):
    
    def __init__(self,result: str, bloom_filter:str,value:str,env=None):
        self.bloom_filter = bloom_filter
        self.value = value
        self.value_check = '_' + self.bloom_filter + '_value_check'
        self.reg_name = '_' + self.bloom_filter + '_register'
        self.index_name = '_' + self.bloom_filter + '_idx'
        self.temp_name = '_' + self.bloom_filter + '_temp'
        self.hash_name = '_' + self.bloom_filter + '_hash'
        self.salt_name = '_' + self.bloom_filter + '_salt'
        self.hashres_name = '_' + self.bloom_filter + '_result'
        self.env = env
        self.result_var_name = result
        if env!=None:
            self.check()

    def check(self):
        True
        
    def get_generated_code(self):
        gc = GeneratedCode()
        properties = (self.env.get_varinfo(self.bloom_filter))['properties']
        val_to_check = self.env.get_varinfo(self.value)
        self.result = self.env.get_varinfo(self.result_var_name)['handle']
        # start with True
        gc.get_apply().writeln('{} = {};'.format(self.result, '(bit<8>)1'))         

        for i in range(properties['number_of_hashes']):
            gc.get_apply().writeln('hash({}, HashAlgorithm.crc16, (bit<32>) 0, '.format(self.hash_name) + '{' + \
                '{}, (bit<8>) {}'.format(val_to_check['handle'], str(i)) + '}, (bit<32>)' +  '{});'.format(str(properties['capacity'])))
            gc.get_apply().writeln('{}.read({}, {});'.format(self.reg_name, self.hashres_name, self.hash_name))
            gc.get_apply().writeln('if ({} != 1)'.format(self.hashres_name) + '{')
            gc.get_apply().increase_indent()
            gc.get_apply().writeln( '{} = (bit<8>) 0;'.format(self.result))
            gc.get_apply().decrease_indent()
            gc.get_apply().writeln('};')

        return gc


# Puts a new element into the bloom filter.
class PutIntoBloom(Command):
    
    def __init__(self, bloom_filter:str,value:str,env=None):
        self.bloom_filter = bloom_filter
        self.value = value
        self.reg_name = '_' + self.bloom_filter + '_register'
        self.hash_name = '_' + self.bloom_filter + '_hash'
        self.env = env
        if env!=None:
            self.check()

    def check(self):
        True
        
    def get_generated_code(self):
        gc = GeneratedCode()
        properties = (self.env.get_varinfo(self.bloom_filter))['properties']
        val_to_check = self.env.get_varinfo(self.value)

        for i in range(properties['number_of_hashes']):
            gc.get_apply().writeln('hash({}, HashAlgorithm.crc16, (bit<32>) 0, '.format(self.hash_name) + '{' + \
                '{}, (bit<8>) {}'.format(val_to_check['handle'], str(i)) + '}, (bit<32>)' + '{});'.format(properties['capacity']))
            gc.get_apply().writeln('{}.write({}, (bit<1>) 1);'.format(self.reg_name, self.hash_name))

        return gc
