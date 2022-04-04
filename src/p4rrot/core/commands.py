
from p4rrot.known_types import KnownType
from typing import Dict, List, Tuple
from p4rrot.standard_fields import *
from p4rrot.generator_tools import *
from p4rrot.checks import *
    

class AssignConst(Command):
    '''
    Assign the value of a literal to a variable.
    '''

    def __init__(self,vname,value,env=None):
        """Assign the value to a variable called *vname*.

        :param vname: name of the variable
        :type vname: str
        :param value: (literal) value to be assigned
        :type value: int
        :param env: containing the accessible variables, defaults to None
        :type env: Environment, optional
        """     
        
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
    "Increment a variable with a scalar value."
    
    def __init__(self,vname,value:int,env=None):
        """Increment a variable with a scalar value.

        :param vname: name of the variable
        :type vname: str
        :param value: scalar value to be added
        :type value: int
        :param env: containing the accessible variables, defaults to None
        :type env: Environment, optional
        """        
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
    "Decrement a variable with a scalar value."

    def __init__(self,vname,value:int,env=None):
        """Decrement a variable with a scalar value.

        :param vname: name of the variable
        :type vname: str
        :param value: scalar value to be substracted
        :type value: int
        :param env: containing the accessible variables, defaults to None
        :type env: Environment, optional
        """        
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
    'Assign the value of one variable to an other with the same type.'

    def __init__(self,target:str,source:str,env=None):
        """Assign the value of the *source* variable to the variable called *target*. The two has to be the same type.

        :param target: name of the target variable
        :type target: str
        :param source: name of the source variable
        :type source: str
        :param env: containing the accessible variables, defaults to None
        :type env: Environment, optional
        """        
   
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
        """The type of the operands and the target variable must have the same type.

        :param target: the name of the variable where the result is stored
        :type target: str
        :param operand_a: variable name of the first operand
        :type operand_a: str
        :param operand_b: variable name of the second operand
        :type operand_b: str
        :param env:  containing the accessible variables, defaults to None
        :type env: Environment, optional
        """        
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
    "Calculate the sume of two variables."

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


class StrictSubtraction(StrictNumericTwoOperandCommand):
    "Substracts one variable from another."


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
        assert self.env.get_varinfo(self.operand_a)['type'] in self.get_allowed_types()
        assert self.env.get_varinfo(self.operand_b)['type'] in self.get_allowed_types()
        is_writeable(self.target,self.env)

    def get_allowed_types(self):
        return [ uint8_t, uint16_t, uint32_t, uint64_t ]


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
    "Starts an *If-Else* statement."

    def __init__(self,vname:str,env=None,then_block=None,else_block=None):
        """Creating an *If-Else* statement. The *then* and *else* branches can be defined later or here as an optional parameter.

        :param vname: name of the *bool_t* variable representing the condition.
        :type vname: str
        :param env: containing the accessible variables, defaults to None
        :type env: Environment, optional
        :param then_block: commands to be executed if the condition is true, defaults to None
        :type then_block: Block, optional
        :param else_block: commands to be executed if the condition is false, defaults to None
        :type else_block: Block, optional
        """        
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
    "Representing the *else* branch of  an *If* statement."

    def __init__(self, env, parent_block):
        super().__init__(env)
        self.parent_block = parent_block

    def EndIf(self):
        """Ending the *If* statement.

        :return: The *Block*, where the *If* was instantieted. 
        :rtype: Block
        """ 
        return self.parent_block


class ThenBlock(Block):
    "Representing the then *branch* of  an *If* statement."

    def __init__(self, env, parent_block, parent_if):
        super().__init__(env)
        self.parent_block = parent_block
        self.parent_if = parent_if

    def Else(self) -> ElseBlock:
        """Ending the *then* block, and starting the *else* part.

        :return: the else block to be populated
        :rtype: ElseBlock
        """        
        return self.parent_if.create_else_block(self.parent_block)

    def EndIf(self) -> Block:
        """Ending the *If* statement.

        :return: The *Block*, where the *If* was instantieted. 
        :rtype: Block
        """        
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
    'Assign the value of one variable to an other with a type-casting.'

    def __init__(self,target:str,source:str,env=None):
        """Assign the value of the *source* variable to the *target* variable where *target* is cast to the type of *source*.

        :param target: name of the target variable
        :type target: str
        :param source: name of the source variable
        :type source: str
        :param env: containing the accessible variables, defaults to None
        :type env: Environment, optional
        """        
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

