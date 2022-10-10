
import sys
sys.path.append('./src/')

from p4rrot.core.commands import *
from p4rrot.v1model.commands import *

def test_assign_const():
    assert 'hdr.inp.a = 5;\n' == AssignConst('a',5,Environment([('a',uint32_t),('b',uint32_t)],[],[],[],None,'inp','out','met',None)).get_generated_code().get_apply().get_code()

def test_expr_to_p4():
    class FakeEnv(Environment):
        def __init__(self):
            pass

        def get_varinfo(self,v):
            return {'handle':'replaced_'+v}
    assert expr_to_p4('a = a.a + a + b + c',FakeEnv()) == 'replaced_a = a.a + replaced_a + replaced_b + c'