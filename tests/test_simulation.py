import sys
sys.path.append('./src/')

import pytest

from p4rrot.known_types import KnownType
from typing import Dict, List, Tuple
from p4rrot.standard_fields import *
from p4rrot.generator_tools import *
from p4rrot.core.commands import *
from p4rrot.core.stateful import *
from p4rrot.v1model.commands import *
from p4rrot.v1model.stateful import *


def test_assign_const():
    fp = FlowProcessor(
        istruct=[('a',uint32_t),('b',uint64_t),('c',uint64_t)],
        ostruct=[('s',uint16_t),('x',bool_t),('y',bool_t)],
        mstruct=[('t',uint8_t)],    
        method='RESPOND'
    )

    fp.add(AssignConst('a',5))
    fp.add(AssignConst('b',50000))
    fp.add(AssignConst('c',9))
    fp.add(AssignConst('s',17))
    fp.add(AssignConst('x',True))
    fp.add(AssignConst('y',False))
    fp.add(AssignConst('t',110))
    fp.add(AssignConst('a',7))

    env = {'a':0,'b':0,'c':0}
    fp.test(env)

    assert env['a']==7
    assert env['b']==50000
    assert env['c']==9
    assert env['s']==17
    assert env['x']==True
    assert env['y']==False
    assert env['t']==110


def test_increment():
    fp = FlowProcessor(
        istruct=[('a',uint8_t),('b',uint8_t),('c',uint8_t)],
    )

    fp.add(Increment('a',5))
    fp.add(Increment('b',7))
    fp.add(Increment('c',1))

    env = {'a':9,'b':17,'c':255}
    fp.test(env)

    assert env['a']==14
    assert env['b']==24
    assert env['c']==0


def test_decrement():
    fp = FlowProcessor(
        istruct=[('a',uint8_t),('b',uint8_t),('c',uint8_t)],
    )

    fp.add(Decrement('a',5))
    fp.add(Decrement('b',7))
    fp.add(Decrement('c',1))

    env = {'a':10,'b':17,'c':0}
    fp.test(env)

    assert env['a']==5
    assert env['b']==10
    assert env['c']==255


def test_assign_var():
    fp = FlowProcessor(
        istruct=[('a',uint16_t),('b',uint32_t),('c',bool_t)],
        ostruct=[('a2',uint16_t),('b2',uint32_t),('c2',bool_t)],
        method='RESPOND'
    )

    fp.add(StrictAssignVar('a2','a'))
    fp.add(StrictAssignVar('b2','b'))
    fp.add(StrictAssignVar('c2','c'))

    env = {'a':0,'b':7658,'c':True}
    fp.test(env)

    assert env['a2']==0
    assert env['b2']==7658
    assert env['c2']==True


def test_addition():
    fp = FlowProcessor(
        istruct=[('a',uint32_t),('b',uint32_t),('c',uint32_t)],
        method='RESPOND'
    )

    fp.add(StrictAddition('c','a','b'))

    env = {'a':7,'b':103,'c':5}
    fp.test(env)

    assert env['a']==7
    assert env['b']==103
    assert env['c']==110


def test_subtract():
    fp = FlowProcessor(
        istruct=[('a',uint8_t),('b',uint8_t),('c',uint8_t)],
        method='RESPOND'
    )

    fp.add(StrictSubtraction('c','a','b'))

    env = {'a':0,'b':1,'c':5}
    fp.test(env)

    assert env['a']==0
    assert env['b']==1
    assert env['c']==255


def test_and():
    fp = FlowProcessor(
        istruct=[('a',bool_t),('b',bool_t)],
        ostruct=[('c',bool_t)],
        method='RESPOND'
    )

    fp.add(LogicalAnd('c','a','b'))

    for a,b,c in [(True,True,True),(False,True,False),(True,False,False),(False,False,False)]:
        env = {'a':a,'b':b}
        fp.test(env)
        assert env['c']==c    
    

def test_or():
    fp = FlowProcessor(
        istruct=[('a',bool_t),('b',bool_t)],
        ostruct=[('c',bool_t)],
        method='RESPOND'
    )

    fp.add(LogicalOr('c','a','b'))

    for a,b,c in [(True,True,True),(False,True,True),(True,False,True),(False,False,False)]:
        env = {'a':a,'b':b}
        fp.test(env)
        assert env['c']==c    
    
def test_not():
    fp = FlowProcessor(
        istruct=[('a',bool_t)],
        method='RESPOND'
    )

    fp.add(LogicalNot('a'))

    for a,na in [(False,True),(True,False)]:
        env = {'a':a}
        fp.test(env)
        assert env['a']==na    


def test_greater_than():
    fp = FlowProcessor(
        istruct=[('a',uint8_t),('b',uint8_t)],
        ostruct=[('c',bool_t)],
        method='RESPOND'
    )

    fp.add(GreaterThan('c','a','b'))

    for a,b,c in [(5,7,False),(7,5,True),(9,9,False),(0,0,False)]:
        env = {'a':a,'b':b}
        fp.test(env)
        assert env['c']==c    


def test_less_than():
    fp = FlowProcessor(
        istruct=[('a',uint8_t),('b',uint8_t)],
        ostruct=[('c',bool_t)],
        method='RESPOND'
    )

    fp.add(LessThan('c','a','b'))

    for a,b,c in [(5,7,True),(7,5,False),(9,9,False),(0,0,False)]:
        env = {'a':a,'b':b}
        fp.test(env)
        assert env['c']==c    


def test_equals():
    fp = FlowProcessor(
        istruct=[('a',uint8_t),('b',uint8_t)],
        ostruct=[('c',bool_t)],
        method='RESPOND'
    )

    fp.add(Equals('c','a','b'))

    for a,b,c in [(5,7,False),(7,5,False),(9,9,True),(0,0,True)]:
        env = {'a':a,'b':b}
        fp.test(env)
        assert env['c']==c    


def test_if():
    fp = FlowProcessor(
            istruct=[('x',bool_t),('y',bool_t),('z',bool_t)],
            ostruct=[('a',uint32_t),('b',uint32_t),('c',uint32_t)],
            method='RESPOND'
        )

    fp\
    .add(If('x'))\
                .add(AssignConst('a',5))\
        .Else()\
                .add(AssignConst('a',7))\
        .EndIf()\
    .add(AssignConst('b',9))\
    .add(If('y'))\
                .add(AssignConst('c',1))\
                .add(If('z'))\
                    .add(AssignConst('c',2))\
                .EndIf()\
        .Else()\
            .add(AssignConst('c',3))\
        .EndIf()


    for x,y,z,a,b,c in [(True,True,True,5,9,2),(True,True,False,5,9,1),
                        (True,False,True,5,9,3),(False,True,True,7,9,2),
                        (True,False,False,5,9,3),(False,True,False,7,9,1),
                        (False,False,True,7,9,3),(False,False,False,7,9,3)]:
        env = {'x':x,'y':y,'z':z}
        fp.test(env)
        assert env['a']==a    
        assert env['b']==b    
        assert env['c']==c    


def test_sendback():
    fp = FlowProcessor(
            istruct=[('x',bool_t)],
            method='RESPOND'
        )

    fp\
    .add(If('x'))\
                .add(SendBack())\
        .EndIf()\
    
    env = {'x':True}
    fp.test(env)
    assert env['meta.postprocessing']=='SENDBACK'    
    
    env = {'x':False}
    fp.test(env)
    assert 'meta.postprocessing' not in env


def test_shared_variable():
    fp = FlowProcessor(
            istruct=[('x',bool_t),('a',uint32_t)],
            state=[ SharedVariable('s',uint32_t) ],
            method='MODIFY'
        )

    fp\
    .add(If('x'))\
                .add(WriteToShared('s','a'))\
        .Else()\
                .add(ReadFromShared('a','s'))\
        .EndIf()\
    
    s = [None]
    env = {'x':True,'a':756,'s':s}
    fp.test(env)
    assert env['s'][0]==756

    env = {'x':False,'a':0,'s':s}
    fp.test(env)
    assert env['a']==756


def test_shared_array():
    shared_array = SharedArray('s',uint32_t,5)
    fp = FlowProcessor(
            istruct=[('x',bool_t),('i',uint32_t),('v',uint32_t)],
            state=[ shared_array ],
            method='MODIFY'
        )

    fp\
    .add(If('x'))\
                .add(WriteToSharedAt('s','i','v'))\
        .Else()\
                .add(ReadFromSharedAt('v','s','i'))\
        .EndIf()\
    
    s = shared_array.get_repr()
    env = {'x':True,'i':4,'v':756,'s':s}
    fp.test(env)
    assert env['s'][4]==756

    env = {'x':False,'i':4,'v':0,'s':s}
    fp.test(env)
    assert env['v']==756


def test_logger():
    fp = FlowProcessor(
        istruct=[('a',uint8_t),('b',uint8_t)],
        ostruct=[('c',bool_t)],
        method='RESPOND'
    )

    def check(env):
        # print(...)
        assert env['c']==True   

    fp.add(LessThan('c','a','b'))
    fp.add(If('c'))\
        .add(Logger(check))\
    .EndIf()

    for a,b,c in [(5,7,True),(7,5,False),(9,9,False),(0,0,False),(99,100,True),(0,255,True)]:
        env = {'a':a,'b':b}
        fp.test(env)
        assert env['c']==c    


def test_const():
    c = Const('c',uint32_t,5)

    fp = FlowProcessor(
        istruct=[('a',uint32_t)],
        state=[c],    
        method='RESPOND'
    )

    fp.add(StrictAssignVar('a','c'))

    env = {'a':0, 'c':c.get_repr()}
    fp.test(env)

    assert env['a']==5


def test_switch_case():
    UID.reset()
    op_plus = Const('op_plus',uint8_t,ord('+'))
    op_minus = Const('op_minus',uint8_t,ord('-'))
    fp = FlowProcessor(
            istruct=[('a',uint32_t),('b',uint32_t),('op',uint8_t)],
            ostruct=[('r',uint32_t)],
            state=[op_plus,op_minus]
        )

    fp\
    .add(Switch('op'))\
            .Case('op_plus')\
                .add(StrictAddition('r','a','b'))\
            .Case('op_minus')\
                .add(StrictSubtraction('r','a','b'))\
            .Default()\
                .add(AssignConst('r',0xdeaddead))\
            .EndSwitch()\
    .add(SendBack())

    for a,b,op,r in [(5,7,ord('+'),12),(789,79,ord('-'),710),(1234,5678,ord('?'),0xdeaddead)]:
        env = {'a':a, 'b':b, 'op':op, 'op_plus':op_plus.get_repr(), 'op_minus':op_minus.get_repr() }
        fp.test(env)
        print(env)
        assert env['r']==r


@pytest.mark.parametrize('x,y',[(5,7),(9,5),(11,11),(77,9),(0,9)])
def test_switch_table(x,y):
    UID.reset()

    fp = FlowProcessor(
            istruct = [('x',uint8_t),('y',uint8_t)],
            locals  = [('l',bool_t)],
        )

    (
    fp
    .add(SwitchTable(['x']))
        .Case([5])
            .add(AssignConst('y',7))
        .Case([9])
            .add(AssignConst('y',5))
        .Case([11])
            .add(AssignConst('y',11))
        .Default()
            .add(AssignConst('y',9))
    .EndSwitch()
    )  

    assert fp.test({'x':x,'y':0}) == {'x':x,'y':y} 