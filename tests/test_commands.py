
import sys
sys.path.append('./src/')

from p4rrot.core.commands import *

def test_assign_const():
    assert 'hdr.inp.a = 5;\n' == AssignConst('a',5,Environment([('a',uint32_t),('b',uint32_t)],[],[],[],'inp','out','met',None)).get_generated_code().get_apply().get_code()