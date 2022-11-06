
from p4rrot.known_types import KnownType
from typing import Dict, List, Tuple
from p4rrot.standard_fields import *
from p4rrot.generator_tools import *
from p4rrot.checks import *
    

class AssignConst(Command):
    
    def __init__(self,vname,value,env=None):
        self.vname = vname
        self.value = value
        self.env = env
    
        if self.env!=None:
            self.check()
            
    def check(self):
        var_exists(self.vname,self.env)
        is_writeable(self.vname,self.env)
        self.env.get_varinfo(self.vname)['type'].to_p4_literal(self.value)
    
    def get_generated_code(self):
        gc = GeneratedCode()
        vi  = self.env.get_varinfo(self.vname)
        gc.get_apply().writeln('{} = {};'.format(vi['handle'],vi['type'].to_p4_literal(self.value)))
        return gc
    
    def execute(self,test_env):
        vi = self.env.get_varinfo(self.vname)
        test_env[self.vname] = vi['type'].cast_value(self.value)



class Increment(Command):
    
    def __init__(self,vname,value:int,env=None):
        self.vname = vname
        self.value = value
        self.env = env
    
        if self.env!=None:
            self.check()
            
    def check(self):
        var_exists(self.vname,self.env)
        assert self.value>0
        is_writeable(self.vname,self.env)
        self.env.get_varinfo(self.vname)['type'].to_p4_literal(self.value)
    
    def get_generated_code(self):
        gc = GeneratedCode()
        vi  = self.env.get_varinfo(self.vname)
        gc.get_apply().writeln('{} = {} + {};'.format(vi['handle'],vi['handle'],vi['type'].to_p4_literal(self.value)))
        return gc
    
    def execute(self,test_env):
        vi = self.env.get_varinfo(self.vname)
        test_env[self.vname] += vi['type'].cast_value(self.value)
        test_env[self.vname] = vi['type'].cast_value(test_env[self.vname])



class Decrement(Command):
    
    def __init__(self,vname,value:int,env=None):
        self.vname = vname
        self.value = value
        self.env = env
    
        if self.env!=None:
            self.check()
            
    def check(self):
        var_exists(self.vname,self.env)
        assert self.value>0
        is_writeable(self.vname,self.env)
        self.env.get_varinfo(self.vname)['type'].to_p4_literal(self.value)
    
    def get_generated_code(self):
        gc = GeneratedCode()
        vi  = self.env.get_varinfo(self.vname)
        gc.get_apply().writeln('{} = {} - {};'.format(vi['handle'],vi['handle'],vi['type'].to_p4_literal(self.value)))
        return gc
    
    def execute(self,test_env):
        vi = self.env.get_varinfo(self.vname)
        test_env[self.vname] -= vi['type'].cast_value(self.value)
        test_env[self.vname] = vi['type'].cast_value(test_env[self.vname])



class StrictAssignVar(Command):
    
    def __init__(self,target,source,env=None):
        self.target = target
        self.source = source
        self.env = env

        if self.env!=None:
            self.check()

    def check(self):
        var_exists(self.source,self.env)
        var_exists(self.target,self.env)
        vars_have_the_same_type(self.source,self.target,self.env)
        is_writeable(self.target,self.env)

    def get_generated_code(self):
        gc = GeneratedCode()
        s  = self.env.get_varinfo(self.source)
        t  = self.env.get_varinfo(self.target)
        gc.get_apply().writeln('{} = {};'.format(t['handle'],s['handle']))
        return gc
    
    def execute(self,test_env):
        si = self.env.get_varinfo(self.source)
        ti = self.env.get_varinfo(self.target)
        test_env[self.target] = si['type'].cast_value(test_env[self.source])



class StrictTwoOperandCommand(Command):
    
    def __init__(self,target,operand_a,operand_b,env=None):
        self.target = target
        self.operand_a = operand_a
        self.operand_b = operand_b
        self.env = env

        if self.env!=None:
            self.check()

    def check(self):
        var_exists(self.target,self.env)
        var_exists(self.operand_a,self.env)
        var_exists(self.operand_b,self.env)
        is_writeable(self.target,self.env)

    def get_generated_code(self):
        raise Exception('Not implemented by subclass')

    def get_allowed_types(self):
        raise Exception('Not implemented by subclass')
    
    def execute(self,test_env):
        raise Exception('Not implemented by subclass')


class StrictNumericTwoOperandCommand(StrictTwoOperandCommand):
    
    def check(self):
        super().check()
        vars_have_the_same_type(self.target,self.operand_a,env=self.env)
        vars_have_the_same_type(self.operand_b,self.operand_a,env=self.env)
        assert self.env.get_varinfo(self.target)['type'] in self.get_allowed_types()

    def get_allowed_types(self):
        return [ uint8_t, uint16_t, uint32_t, uint64_t ]


class StrictAddition(StrictNumericTwoOperandCommand):

    def get_generated_code(self):
        gc = GeneratedCode()
        t  = self.env.get_varinfo(self.target)
        a  = self.env.get_varinfo(self.operand_a)
        b  = self.env.get_varinfo(self.operand_b)
        gc.get_apply().writeln('{} = {} + {};'.format(t['handle'],a['handle'],b['handle']))        
        return gc

    def execute(self,test_env):
        ti = self.env.get_varinfo(self.target)
        test_env[self.target] = ti['type'].cast_value(test_env[self.operand_a] + test_env[self.operand_b])

class LeftShift(Command):

    def __init__(self,vname,value,env=None):
        self.vname = vname
        self.value = value
        self.env = env
    
        if self.env!=None:
            self.check()
            
    def check(self):
        var_exists(self.vname,self.env)
        is_writeable(self.vname,self.env)
        self.env.get_varinfo(self.vname)['type'].to_p4_literal(self.value)
    
    def get_generated_code(self):
        gc = GeneratedCode()
        vi  = self.env.get_varinfo(self.vname)
        gc.get_apply().writeln('{} = {} << {};'.format(vi['handle'],vi['handle'],vi['type'].to_p4_literal(self.value)))
        return gc
    
    def execute(self,test_env):
        vi = self.env.get_varinfo(self.vname)
        test_env[self.target] = ti['type'].cast_value(test_env[self.vname] << self.value)

class RightShift(Command):

    def __init__(self,vname,value,env=None):
        self.vname = vname
        self.value = value
        self.env = env
    
        if self.env!=None:
            self.check()
            
    def check(self):
        var_exists(self.vname,self.env)
        is_writeable(self.vname,self.env)
        self.env.get_varinfo(self.vname)['type'].to_p4_literal(self.value)
    
    def get_generated_code(self):
        gc = GeneratedCode()
        vi  = self.env.get_varinfo(self.vname)
        gc.get_apply().writeln('{} = {} >> {};'.format(vi['handle'],vi['handle'],vi['type'].to_p4_literal(self.value)))
        return gc
    
    def execute(self,test_env):
        vi = self.env.get_varinfo(self.vname)
        test_env[self.target] = ti['type'].cast_value(test_env[self.vname] >> self.value)


class StrictSubtraction(StrictNumericTwoOperandCommand):

    def get_generated_code(self):
        gc = GeneratedCode()
        t  = self.env.get_varinfo(self.target)
        a  = self.env.get_varinfo(self.operand_a)
        b  = self.env.get_varinfo(self.operand_b)
        gc.get_apply().writeln('{} = {} - {};'.format(t['handle'],a['handle'],b['handle']))        
        return gc

    def execute(self,test_env):
        ti = self.env.get_varinfo(self.target)
        test_env[self.target] = ti['type'].cast_value(test_env[self.operand_a] - test_env[self.operand_b])


class StrictBooleanTwoOperandCommand(StrictTwoOperandCommand):
    
    def check(self):
        super().check()
        assert self.env.get_varinfo(self.target)['type'] in self.get_allowed_types()
        assert self.env.get_varinfo(self.operand_b)['type'] in self.get_allowed_types()
        assert self.env.get_varinfo(self.operand_b)['type'] in self.get_allowed_types()

    def get_allowed_types(self):
        return [ bool_t ]


class LogicalAnd(StrictBooleanTwoOperandCommand):

    def get_generated_code(self):
        gc = GeneratedCode()
        t  = self.env.get_varinfo(self.target)
        a  = self.env.get_varinfo(self.operand_a)
        b  = self.env.get_varinfo(self.operand_b)
        gc.get_apply().writeln('{} = {} & {};'.format(t['handle'],a['handle'],b['handle']))        
        return gc

    def execute(self,test_env):
        test_env[self.target] = test_env[self.operand_a] and test_env[self.operand_b]


class LogicalOr(StrictBooleanTwoOperandCommand):

    def get_generated_code(self):
        gc = GeneratedCode()
        t  = self.env.get_varinfo(self.target)
        a  = self.env.get_varinfo(self.operand_a)
        b  = self.env.get_varinfo(self.operand_b)
        gc.get_apply().writeln('{} = {} | {};'.format(t['handle'],a['handle'],b['handle']))        
        return gc

    def execute(self,test_env):
        test_env[self.target] = test_env[self.operand_a] or test_env[self.operand_b]


class StrictComparator(StrictTwoOperandCommand):

    def check(self):
        super().check()
        assert self.env.get_varinfo(self.target)['type']==bool_t
        vars_have_the_same_type(self.operand_a,self.operand_b,self.env)
#        assert self.env.get_varinfo(self.operand_a)['type'] in self.get_allowed_types()
#        assert self.env.get_varinfo(self.operand_b)['type'] in self.get_allowed_types()
        is_writeable(self.target,self.env)

#    def get_allowed_types(self):
#        return [ uint8_t, uint16_t, uint32_t, uint64_t ]


class GreaterThan(StrictComparator):
    
    def get_generated_code(self):
        gc = GeneratedCode()
        t  = self.env.get_varinfo(self.target)
        a  = self.env.get_varinfo(self.operand_a)
        b  = self.env.get_varinfo(self.operand_b)
        gc.get_apply().writeln('{} = (BOOL_T)(bit<1>)({} > {});'.format(t['handle'],a['handle'],b['handle']))        
        return gc

    def execute(self,test_env):
        test_env[self.target] = test_env[self.operand_a] > test_env[self.operand_b]

class LessThan(StrictComparator):
    
    def get_generated_code(self):
        gc = GeneratedCode()
        t  = self.env.get_varinfo(self.target)
        a  = self.env.get_varinfo(self.operand_a)
        b  = self.env.get_varinfo(self.operand_b)
        gc.get_apply().writeln('{} = (BOOL_T)(bit<1>)({} < {});'.format(t['handle'],a['handle'],b['handle']))        
        return gc

    def execute(self,test_env):
        test_env[self.target] = test_env[self.operand_a] < test_env[self.operand_b]


class Equals(StrictComparator):
    
    def get_generated_code(self):
        gc = GeneratedCode()
        t  = self.env.get_varinfo(self.target)
        a  = self.env.get_varinfo(self.operand_a)
        b  = self.env.get_varinfo(self.operand_b)
        gc.get_apply().writeln('{} = (BOOL_T)(bit<1>)({} == {});'.format(t['handle'],a['handle'],b['handle']))        
        return gc

    def execute(self,test_env):
        test_env[self.target] = test_env[self.operand_a] == test_env[self.operand_b]

class MaskedEqualsConst(Command):

    def __init__(self,target,vname,mask:int,const:int,env=None):
        self.target = target
        self.vname = vname
        self.mask = mask
        self.const = const
        self.env = env
    
        if self.env!=None:
            self.check()
            
    def check(self):
        var_exists(self.vname,self.env)
        is_writeable(self.target,self.env)
        assert self.env.get_varinfo(self.target)['type']==bool_t
    
    def get_generated_code(self):
        gc = GeneratedCode()
        t  = self.env.get_varinfo(self.target)
        a  = self.env.get_varinfo(self.vname)
        gc.get_apply().writeln('{} = (BOOL_T)(bit<1>)({} & {} == {});'.format(t['handle'],a['handle'],self.mask,self.const))        
        return gc
    
    def execute(self,test_env):
        test_env[self.target] = test_env[self.vname] & self.mask == self.const

class MaskedNotEqualsConst(Command):

    def __init__(self,target,vname,mask:int,const:int,env=None):
        self.target = target
        self.vname = vname
        self.mask = mask
        self.const = const
        self.env = env
    
        if self.env!=None:
            self.check()
            
    def check(self):
        var_exists(self.vname,self.env)
        is_writeable(self.target,self.env)
        assert self.env.get_varinfo(self.target)['type']==bool_t
    
    def get_generated_code(self):
        gc = GeneratedCode()
        t  = self.env.get_varinfo(self.target)
        a  = self.env.get_varinfo(self.vname)
        gc.get_apply().writeln('{} = (BOOL_T)(bit<1>)({} & {} != {});'.format(t['handle'],a['handle'],self.mask, self.const))        
        return gc
    
    def execute(self,test_env):
        test_env[self.target] = test_env[self.vname] & self.mask != self.const

class EqualsConst(Command):

    def __init__(self,target,vname,const:int,env=None):
        self.target = target
        self.vname = vname
        self.const = const
        self.env = env
    
        if self.env!=None:
            self.check()
            
    def check(self):
        var_exists(self.vname,self.env)
        is_writeable(self.target,self.env)
        assert self.env.get_varinfo(self.target)['type']==bool_t
    
    def get_generated_code(self):
        gc = GeneratedCode()
        t  = self.env.get_varinfo(self.target)
        a  = self.env.get_varinfo(self.vname)
        gc.get_apply().writeln('{} = (BOOL_T)(bit<1>)({} == {});'.format(t['handle'],a['handle'],self.const))        
        return gc
    
    def execute(self,test_env):
        test_env[self.target] = test_env[self.vname] == self.const



class LogicalNot(Command):
    
    def __init__(self,vname,env=None):
        self.vname = vname
        self.env = env
    
        if self.env!=None:
            self.check()
            
    def check(self):
        var_exists(self.vname,self.env)
        assert self.env.get_varinfo(self.vname)['type']==bool_t
        is_writeable(self.vname,self.env)

    def get_generated_code(self):
        gc = GeneratedCode()
        vi  = self.env.get_varinfo(self.vname)
        gc.get_apply().writeln('{} = {} ^ 1;'.format(vi['handle'],vi['handle']))
        return gc
    
    def execute(self,test_env):
        test_env[self.vname] = not test_env[self.vname]



class If(Command):

    def __init__(self,vname:str,env=None,then_block=None,else_block=None):
        self.env = env
        self.vname = vname
        self.then_block = then_block
        self.else_block = else_block

        if self.env!=None:
            self.check()

    def check(self):
        var_exists(self.vname,self.env)
        assert self.env.get_varinfo(self.vname)['type']==bool_t

    def get_generated_code(self):
        gc = GeneratedCode()
        vi  = self.env.get_varinfo(self.vname)
        gc.get_apply().writeln('if ({}==1){{'.format(vi['handle']))
        gc.get_apply().increase_indent()

        if self.then_block!=None:
            gc.concat( self.then_block.get_generated_code() )
        gc.get_apply().decrease_indent()
        gc.get_apply().writeln('}')

        if self.else_block!=None:
            gc.get_apply().writeln('else{')
            gc.get_apply().increase_indent()
            gc.concat( self.else_block.get_generated_code() )
            gc.get_apply().decrease_indent()
            gc.get_apply().writeln('}')
        
        return gc

    def should_return(self):
        return self.then_block == None

    def get_return_object(self,parent):
        return self.create_then_block(parent)

    def create_then_block(self,parent_block):
        self.then_block = ThenBlock(self.env,parent_block,self)
        return self.then_block

    def create_else_block(self,parent_block):
        self.else_block = ElseBlock(self.env,parent_block)
        return self.else_block

    def execute(self,test_env):
        if test_env[self.vname]:
            self.then_block.test(test_env)
        elif self.else_block!=None:
            self.else_block.test(test_env)


class ElseBlock(Block):
    
    def __init__(self, env, parent_block):
        super().__init__(env)
        self.parent_block = parent_block

    def EndIf(self):
        return self.parent_block


class ThenBlock(Block):
    
    def __init__(self, env, parent_block, parent_if):
        super().__init__(env)
        self.parent_block = parent_block
        self.parent_if = parent_if

    def Else(self) -> ElseBlock:
        return self.parent_if.create_else_block(self.parent_block)

    def EndIf(self) -> Block:
        return self.parent_block


class SendBack(Command):
    def __init__(self,env=None):
        self.env = env

    def check(self):
        pass
                
    def get_generated_code(self):
        gc = GeneratedCode()
        gc.get_apply().writeln('meta.postprocessing = SENDBACK;')
        return gc

    def execute(self,test_env):
        test_env['meta.postprocessing']='SENDBACK'


class Comment(Command):

    def __init__(self,message:str,env=None):
        self.message = message
        self.env = env

    def check(self):
        pass

    def get_generated_code(self):
        gc = GeneratedCode()
        gc.get_apply().writeln('// {} '.format(self.message))
        return gc

    def execute(self,test_env):
        pass



class Logger(Command):

    def __init__(self,fun,enabled=True,env=None):
        self.enabled = enabled
        self.fun = fun
        self.env = env

    def check(self):
        pass

    def get_generated_code(self):
        gc = GeneratedCode()
        return gc

    def execute(self,test_env):
        if self.enabled:
            self.fun(test_env)



class Switch(Command):

    def __init__(self,vname:str,env=None,cases=None):
        self.env = env
        self.vname = vname

        if cases!=None:
            raise NotImplemented('passing cses using parameters is not yet supported')

        if self.env!=None:
            self.check()

    def check(self):
        var_exists(self.vname,self.env)

    def should_return(self):
        return True

    def get_return_object(self,parent):
        self.parent = parent
        return self

    def Case(self,cvname:str):
        var_exists(cvname,self.env)
        var_exists(self.vname,self.env)
        vars_have_the_same_type(self.vname,cvname,self.env)

        self.first_guess = cvname
        self.first_block = CaseBlock(self.env,self.parent,self.vname)
        return self.first_block

    def get_generated_code(self):
        gc = GeneratedCode()
        
        gc.get_apply().writeln('if ({}=={}){{'.format( self.env.get_varinfo(self.vname)['handle'], self.env.get_varinfo(self.first_guess)['handle'] ))
        actual_block = self.first_block
        
        gc.get_apply().increase_indent()
        tmp = actual_block.get_generated_code()
        gc.concat(tmp)
        gc.get_apply().decrease_indent()
        
        while actual_block.get_next_block()!=None:
            next_guess = actual_block.get_next_guess()
            actual_block = actual_block.get_next_block()
            
            gc.get_apply().writeln('}')
            if next_guess != None:
                gc.get_apply().writeln('else if ({}=={}){{'.format( self.env.get_varinfo(self.vname)['handle'], self.env.get_varinfo(next_guess)['handle'] ))
            else:
                gc.get_apply().writeln('else{')

            gc.get_apply().increase_indent()
            tmp = actual_block.get_generated_code()
            gc.concat(tmp)
            gc.get_apply().decrease_indent()

        gc.get_apply().writeln('}')

        return gc

    def execute(self,test_env):
        value = test_env[self.vname]
        actual_block = self.first_block
        actual_guess = self.first_guess

        while actual_block!=None and ( actual_guess!=None and value!=test_env[actual_guess] ):
            actual_guess = actual_block.get_next_guess()
            actual_block = actual_block.get_next_block()

        if actual_block!=None:
            actual_block.test(test_env)



class CaseBlock(Block):
    def __init__(self, env, parent_block, match_var):
        super().__init__(env)
        self.parent_block = parent_block
        self.next_guess = None
        self.next_block = None
        self.match_var = match_var

    def Case(self,cvname:str):
        var_exists(cvname,self.env)
        var_exists(self.match_var,self.env)
        vars_have_the_same_type(self.match_var,cvname,self.env)

        self.next_guess = cvname
        self.next_block = CaseBlock(self.env,self.parent_block,self.match_var)
        return self.next_block

    def Default(self):
        self.next_block = DefaultBlock(self.env,self.parent_block)
        return self.next_block

    def EndSwitch(self):
        return self.parent_block

    def get_next_guess(self):
        return self.next_guess

    def get_next_block(self):
        return self.next_block


class DefaultBlock(Block):
    def __init__(self, env, parent_block):
        super().__init__(env)
        self.parent_block = parent_block
        self.next_guess = None
        self.next_block = None

    def EndSwitch(self):
        return self.parent_block

    def get_next_guess(self):
        return self.next_guess

    def get_next_block(self):
        return self.next_block
    

class Atomic(Command):
    def __init__(self,env=None,atomic_block=None):
        self.env = env
        self.atomic_block = atomic_block

        if self.env!=None:
            self.check()

    def check(self):
        pass
    
    def get_generated_code(self):
        gc = GeneratedCode()    

        gc.get_apply().writeln('@atomic{')
        gc.get_apply().writeln('ATOMIC_BEGIN')
        gc.get_apply().increase_indent()

        tmp = self.atomic_block.get_generated_code()
        gc.concat(tmp)

        gc.get_apply().decrease_indent()
        gc.get_apply().writeln('ATOMIC_END')
        gc.get_apply().writeln('}')    

        return gc

    def should_return(self):
        return self.atomic_block==None

    def get_return_object(self,parent):
        self.atomic_block = AtomicBlock(self.env,parent)
        return self.atomic_block

    def execute(self,test_env):
        self.atomic_block.test(test_env)


class AtomicBlock(Block):

    def __init__(self, env, parent_block):
        super().__init__(env)
        self.parent_block = parent_block

    def EndAtomic(self):
        return self.parent_block



class Drop(Command):
    def __init__(self,env=None):
        self.env = env

    def check(self):
        pass
                
    def get_generated_code(self):
        gc = GeneratedCode()
        gc.get_apply().writeln('meta.postprocessing = DROP;')
        return gc

    def execute(self,test_env):
        test_env['meta.postprocessing']='DROP'



class SetStandardField(Command):
    
    def __init__(self,field,value,env=None):
        self.field = field
        self.value = value
        self.env = env
    
        if self.env!=None:
            self.check()
            
    def check(self):
        pass

    def get_generated_code(self):
        gc = GeneratedCode()
        gc.get_apply().writeln('{} = {};'.format(self.field.get_handle(),self.field.get_type().to_p4_literal(self.value)))
        return gc
    
    def execute(self,test_env):
        # TODO
        # test_env[self.vname] = vi['type'].cast_value(self.value)
        pass


class CastVar(Command):
    
    def __init__(self,target,source,env=None):
        self.target = target
        self.source = source
        self.env = env

        if self.env!=None:
            self.check()

    def check(self):
        var_exists(self.source,self.env)
        var_exists(self.target,self.env)
        is_writeable(self.target,self.env)

    def get_generated_code(self):
        gc = GeneratedCode()
        s  = self.env.get_varinfo(self.source)
        t  = self.env.get_varinfo(self.target)
        gc.get_apply().writeln('{} = ({}) {};'.format(t['handle'],t['type'].get_p4_type(),s['handle']))
        return gc
    
    def execute(self,test_env):
        ti = self.env.get_varinfo(self.target)
        test_env[self.target] = ti['type'].cast_value(test_env[self.source])

class Table:
    def __init__(self, name, actions, keys, size, const_entries, default_action = ""):
        self.name = name
        self.keys = keys
        self.actions = actions
        self.size = size
        self.const_entries = const_entries
        self.default_action = default_action

    # TODO: create action class
    # TODO: check types and signatures
    def get_generated_code(self):
        gc = GeneratedCode()
        declaration = gc.get_decl()
        declaration.writeln("table {} {{".format(self.name))
        declaration.increase_indent()
        declaration.writeln("key = {")
        declaration.increase_indent()
        for key in self.keys:
            declaration.writeln("{}: {};".format(key["name"], key["match_type"]))
        declaration.decrease_indent()
        declaration.writeln("}")
        declaration.writeln("actions = {")
        declaration.increase_indent()
        for action in self.actions:
            declaration.writeln("{};".format(action))
        declaration.decrease_indent()
        declaration.writeln("}")
        declaration.writeln("size = {};".format(self.size))
        if self.default_action:
            declaration.writeln("const default_action = {};".format(self.default_action))
        if self.const_entries:
            declaration.writeln("const entries = {")
            declaration.increase_indent()
            for entry in self.const_entries:
                declaration.writeln(
                    "{} : {}({});".format(
                        entry["value"], entry["action"], ",".join(entry["parameters"])
                    )
                )
            declaration.decrease_indent()
            declaration.writeln("}")
        declaration.decrease_indent()
        declaration.writeln("}")
        return gc

class ReadFromControlPlaneSet(Command):
    def __init__(self, keys, targets, env=None):
        self.targets = targets
        self.keys = keys
        self.env = env

    def get_generated_code(self):
        gc = GeneratedCode()
        target_infos = []
        for target in self.targets:
            target_infos.append(self.env.get_varinfo(target))
        match = []
        for key in self.keys:
            match.append([self.env.get_varinfo(key["name"]),key["match_type"]])
        declaration = gc.get_decl()
        table_name = "control_plane_set_table_" + UID.get()
        apply = gc.get_apply()
        setter_action = "setter_action_" + UID.get()
        parameters = [p["type"].get_p4_type() + "  param" + UID.get() for p in target_infos]
        declaration.writeln("action {}({}) {{".format(setter_action, ",".join(parameters)))
        declaration.increase_indent()
        for i in range(len(parameters)):
            declaration.writeln(
                "{} = {};".format(target_infos[i]["handle"], parameters[i].split(" ")[2])
            )
        declaration.decrease_indent()
        declaration.writeln("}")
        actions = [setter_action]
        try:
            key = [
                {"name": part_key[0]["handle"], "match_type": part_key[1]} for part_key in match
            ]
        except TypeError:
            key = [
                {"name": part_key[0].get_handle(), "match_type": part_key[1]} for part_key in match
            ]
        size = 1
        const_entries = []
        eval_table = Table(
            table_name, actions, key, size, const_entries
        )
        gc.concat(eval_table.get_generated_code())
        apply.writeln("{}.apply();".format(table_name))
        return gc

    def check(self):
        pass

    def execute(self, test_env):
        pass

