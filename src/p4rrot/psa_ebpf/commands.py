from p4rrot.known_types import KnownType
from typing import Dict, List, Tuple
from p4rrot.standard_fields import *
from p4rrot.generator_tools import *
from p4rrot.checks import *
from p4rrot.core.commands import *
import random

class AssignRandomValue(Command):

    def __init__(self, vname, min_value, max_value, env=None):
        self.env = env
        self.vname=vname
        self.min_value = min_value
        self.max_value = max_value

        
        if self.env != None:
            self.check()


    def check(self):
        var_exists(self.vname, self.env)
        assert self.env.get_varinfo(self.vname)['type'] in [ uint8_t, uint16_t ,uint32_t, uint64_t ], 'Not supported random generation'
        target_type = self.env.get_varinfo(self.vname)['type']
        is_writeable(self.vname,self.env)


    def get_generated_code(self):
        gc = GeneratedCode()
        rng_name = "rng_"+UID.get()
        target_type = self.env.get_varinfo(self.vname)['type']
        rng_type = target_type.get_p4_type()
        vi  = self.env.get_varinfo(self.vname)
        gc.get_decl().writeln('Random< {} >(({}){},({}){}) {};'.format(
            rng_type,
            rng_type,
            self.min_value,
            rng_type,
            self.max_value,
            rng_name
        ))
        gc.get_apply().writeln('{} = {}.read();'.format(vi['handle'], rng_name))
        return gc


    def execute(self, test_env):
        target_type = self.env.get_varinfo(self.vname)['type']
        test_env[self.vname] = random.randint(target_type.cast_value(min_value),target_type.cast_value(max_value))


class AssignHash(Command):
    def __init__(self, t_name, s_name, hash_name, env=None):
        self.env = env
        self.t_name = t_name
        self.s_name = s_name
        self.hash_name = hash_name

        if self.env != None:
            self.check()

    def check(self):
        var_exists(self.t_name, self.env)
        var_exists(self.s_name, self.env)
        var_exists(self.hash_name, self.env)
        is_writeable(self.t_name, self.env)

    def get_generated_code(self):
        gc = GeneratedCode()
        target = self.env.get_varinfo(self.t_name)
        source = self.env.get_varinfo(self.s_name)
        gc.get_apply().writeln('{} = {}.get_hash({});'.format(target['handle'], self.hash_name, source['handle']))
        return gc


class GetTimestamp(Command):
    def __init__(self, vname, env=None):
        self.env = env
        self.vname = vname

        if self.env != None:
            self.check()

    
    def check(self):
        var_exists(self.vname, self.env)
        assert self.env.get_varinfo(self.vname)['type'] == uint64_t
        is_writeable(self.vname, self.env)


    def get_generated_code(self):
        gc = GeneratedCode()
        vi = self.env.get_varinfo(self.vname)
        gc.get_apply().writeln('{} = (bit<64>) istd.ingress_timestamp;'.format(vi['handle']))
        return gc

    
    def execute(self, test_env):
        pass


class Clone(Command):
    def __init__(self, keys, table_name=None, action_name=None, env=None):
        self.keys = keys
        self.env = env
        if table_name is None:
            self.table_name = "clone_table" + UID.get()
        else:
            self.table_name=table_name

        if action_name is None:
            self.action_name = "setter_action_" + UID.get()
        else:
            self.action_name = action_name

    
    def check(self):
        pass

    def get_generated_code(self):
        gc = GeneratedCode()
        decl = gc.get_decl()
        decl.writeln(f"action {self.action_name}(CloneSessionId_t clone_session) {{")
        decl.increase_indent()
        decl.writeln("ostd.clone_session_id = clone_session;")
        decl.writeln("ostd.clone = true;")
        decl.decrease_indent()
        decl.writeln("}")


        apply = gc.get_apply()
        match = []
        for key in self.keys:
            match.append(self.env.get_varinfo(key))
        actions = [self.action_name, "NoAction"]

        try:
            key = [
                {"name": part_key["handle"], "match_type": "exact"} for part_key in match
            ]
        except TypeError:
            key = [
                {"name": part_key.get_handle(), "match_type": "exact"} for part_key in match
            ]
        size = 256
        const_entries = []
        default_action = "NoAction"
        eval_table = Table(
            self.table_name, actions, key, size, const_entries, default_action
        )
        gc.concat(eval_table.get_generated_code())
        apply.writeln("{}.apply();".format(self.table_name))

        return gc
