from p4rrot.known_types import KnownType
from typing import Dict, List, Tuple
from p4rrot.standard_fields import *
from p4rrot.generator_tools import *
from p4rrot.checks import *
import random

class AssignRandomValue(Command):

    def __init__(self, vname, rngname, env=None):
        self.env = env
        self.vname=vname
        self.rngname=rngname

        
        if self.env != None:
            self.check()


    def check(self):
        var_exists(self.vname, self.env)
        var_exists(self.rngname, self.env)
        is_writeable(self.vname,self.env)
        vars_have_the_same_type(self.vname, self.rngname, self.env)


    def get_generated_code(self):
        gc = GeneratedCode()
        vi  = self.env.get_varinfo(self.vname)
        gc.get_apply().writeln('{} = {}.read();'.format(vi['handle'], self.rngname))
        return gc


    def execute(self, test_env):
        min_value = self.env.get_varinfo(self.rngname)['min_value']
        max_value = self.env.get_varinfo(self.rngname)['max_value']
        test_env[self.vname] = random.randint(target_type.cast_value(min_value),target_type.cast_value(max_value))

