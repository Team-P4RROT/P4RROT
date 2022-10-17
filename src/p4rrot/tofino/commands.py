
import copy 
import random
from typing import Dict, List, Tuple

from p4rrot.known_types import KnownType
from p4rrot.standard_fields import *
from p4rrot.generator_tools import *
from p4rrot.core.commands import *
from p4rrot.tofino.helper import *
from p4rrot.checks import *


class TofinoAssignRandomValue(Command):
    
    def __init__(self,vname:str,env=None) -> None:
        self.vname = vname
        self.env = env

        if self.env!=None:
            self.check()

    def check(self):
        var_exists(self.vname,self.env)
        assert self.env.get_varinfo(self.vname)['type'] in [ uint8_t, uint16_t ,uint32_t, uint64_t ], 'Not supported random generation'
        is_writeable(self.vname,self.env)

    def get_generated_code(self):
        gc = GeneratedCode()
        vi = self.env.get_varinfo(self.vname)
        generator_name = 'rnd_'+UID.get()
        gc.get_decl().writeln('Random<{}>() {};'.format(vi['type'].get_p4_type(),generator_name))
        gc.get_apply().writeln('{} = {}.get();'.format( vi['handle'],generator_name))
        return gc

    def execute(self,test_env):
        target_type = self.env.get_varinfo(self.vname)['type']
        test_env[self.vname] = random.randint(0,2**(target_type.get_size()*8-1))


class UsingBlock(Block):
    def __init__(self, env, parent_block):
        super().__init__(env)
        self.parent_block = parent_block

    def EndUsing(self):
        return self.parent_block


class Using(Command):
    def __init__(
        self,
        shared_array_name: str,
        index_var: str,
        return_var=None,
        using_block=None,
        env=None,
    ):
        self.shared_array_name = shared_array_name
        self.index_var = index_var
        self.using_block = using_block
        self.return_var = return_var
        self.env = None

    def get_generated_code(self):
        gc = GeneratedCode()
        
        index_info = self.env.get_varinfo(self.index_var)
        reg_info = self.env.get_varinfo(self.shared_array_name)
        reg_value_type = reg_info['type'][1].get_p4_type()
        if self.return_var!=None:        
            return_info = self.env.get_varinfo(self.return_var)
            return_type = return_info['type'].get_p4_type()
        else:
            return_type = reg_value_type

        action_name = 'regac_'+UID.get()

        gc.get_decl().writeln(f"RegisterAction<{reg_value_type},_,{return_type}>({reg_info['handle']}) {action_name} = {{")
        gc.get_decl().increase_indent()
        
        gc.get_decl().writeln(f"void apply(inout {reg_value_type} {self.shared_array_name},  out {return_type} {self.return_var}){{")
        gc.get_decl().increase_indent()

        if self.using_block:
            tmp = self.using_block.get_generated_code()
            apply = tmp.get_apply()
            gc.get_decl().write(apply.get_code(),indent_new_lines=True)
            tmp.get_apply().code = '' # TODO: it should use a function without relying on the representation

        gc.get_decl().decrease_indent()
        gc.get_decl().writeln("}")
        gc.get_decl().decrease_indent()
        gc.get_decl().writeln("};")

        if self.using_block:
            gc.concat(tmp)

        if self.return_var!=None:
            gc.get_apply().writeln(f"{return_info['handle']} = {action_name}.execute({index_info['handle']});")
        else:
            gc.get_apply().writeln(f"{action_name}.execute({index_info['handle']});")

        return gc
    
    def check(self):
        pass

    def should_return(self):
        return self.using_block == None

    def get_return_object(self, parent):
        value_type = self.env.get_varinfo(self.shared_array_name)['type'][1]

        new_env = copy.deepcopy(self.env)
        new_env.info[self.shared_array_name]["handle"]=self.shared_array_name # TODO: set_varinfo is needed
        new_env.info[self.shared_array_name]["type"]=value_type # TODO: set_varinfo is needed
        new_env.info[self.shared_array_name]["writeable"]=True # TODO: set_varinfo is needed
        if self.return_var!=None:
            new_env.info[self.return_var]["handle"]=self.return_var # TODO: set_varinfo is needed
        self.using_block = UsingBlock(new_env, parent)
        return self.using_block


class IncrementSharedArray(Command):
    def __init__(
        self,
        shared_array,
        number_type,
        index_type,
        index_to_increase,
        step=1,
        read_new_to=None,
        env=None,
    ):
        self.shared_array = shared_array
        self.number_type = number_type
        self.index_type = index_type
        self.index_to_increase = index_to_increase
        self.step = step
        self.read_new_to = read_new_to
        self.env = env

        if self.env != None:
            self.check()

    def check(self):
        if self.read_new_to:
            var_exists(self.read_new_to, self.env)
            var_is_of_type(self.read_new_to, self.number_type, self.env)
            is_writeable(self.read_new_to, self.env)

    def get_generated_code(self):
        gc = GeneratedCode()
        declaration = gc.get_decl()
        if self.read_new_to is not None:
            target = self.env.get_varinfo(self.read_new_to)
        action_name = "increment_shared_array_action_" + UID.get()
        apply_lines = ["to_store = to_store + {};".format(self.step)]
        parameters = [{"mode": "inout", "type": self.number_type, "name": "to_store"}]
        if self.read_new_to:
            apply_lines.append("to_return = to_store;")
            parameters.append(
                {"mode": "out", "type": self.number_type, "name": "to_return"}
            )
        increment_shared_array_action = SharedArrayAction(
            action_name,
            self.shared_array,
            self.number_type,
            self.number_type,
            self.index_type,
            parameters,
            apply_lines,
        )
        gc.concat(increment_shared_array_action.get_generated_code())
        if self.read_new_to:
            gc.get_apply().writeln(
                "{} = {}.execute({});".format(
                    target["handle"], action_name, self.index_to_increase
                )
            )
        else:
            gc.get_apply().writeln(
                "{}.execute({});".format(action_name, self.index_to_increase)
            )
        return gc


class DecrementSharedArray(Command):
    def __init__(
        self,
        shared_array,
        number_type,
        index_type,
        index_to_decrease,
        step=1,
        read_new_to=None,
        env=None,
    ):
        self.shared_array = shared_array
        self.number_type = number_type
        self.index_type = index_type
        self.index_to_decrease = index_to_decrease
        self.step = step
        self.read_new_to = read_new_to
        self.env = env

        if self.env != None:
            self.check()

    def check(self):
        if self.read_new_to:
            var_exists(self.read_new_to, self.env)
            var_is_of_type(self.read_new_to, self.number_type, self.env)
            is_writeable(self.read_new_to, self.env)

    def get_generated_code(self):
        gc = GeneratedCode()
        declaration = gc.get_decl()
        if self.read_new_to is not None:
            target = self.env.get_varinfo(self.read_new_to)
        action_name = "decrement_shared_array_action_" + UID.get()
        apply_lines = ["to_store = to_store - {};".format(self.step)]
        parameters = [{"mode": "inout", "type": self.number_type, "name": "to_store"}]
        if self.read_new_to:
            apply_lines.append("to_return = to_store;")
            parameters.append(
                {"mode": "out", "type": self.number_type, "name": "to_return"}
            )
        decrement_shared_array_action = SharedArrayAction(
            action_name,
            self.shared_array,
            self.number_type,
            self.number_type,
            self.index_type,
            parameters,
            apply_lines,
        )
        gc.concat(decrement_shared_array_action.get_generated_code())
        if self.read_new_to:
            gc.get_apply().writeln(
                "{} = {}.execute({});".format(
                    target["handle"], action_name, self.index_to_decrease
                )
            )
        else:
            gc.get_apply().writeln(
                "{}.execute({});".format(action_name, self.index_to_decrease)
            )
        return gc


class WriteSharedArray(Command):
    def __init__(
        self,
        shared_array,
        value_type,
        index_type,
        index_to_write,
        value_to_write,
        read_old_to=None,
        env=None,
    ):
        self.shared_array = shared_array
        self.value_type = value_type
        self.index_type = index_type
        self.index_to_write = index_to_write
        self.value_to_write = value_to_write
        self.read_old_to = read_old_to
        self.env = env

        if self.env != None:
            self.check()

    def check(self):
        if self.read_old_to:
            var_exists(self.read_old_to, self.env)
            var_is_of_type(self.read_old_to, self.value_type, self.env)
            is_writeable(self.read_old_to, self.env)

    def get_generated_code(self):
        gc = GeneratedCode()
        declaration = gc.get_decl()
        if self.read_old_to is not None:
            target = self.env.get_varinfo(self.read_old_to)
        action_name = "write_shared_array_action_" + UID.get()
        apply_lines = []
        parameters = [{"mode": "inout", "type": self.value_type, "name": "to_store"}]
        if self.read_old_to:
            apply_lines.append("to_return = to_store;")
            parameters.append(
                {"mode": "out", "type": self.value_type, "name": "to_return"}
            )
        apply_lines.append("to_store = {};".format(self.value_to_write))
        write_shared_array_action = SharedArrayAction(
            action_name,
            self.shared_array,
            self.value_type,
            self.value_type,
            self.index_type,
            parameters,
            apply_lines,
        )
        gc.concat(write_shared_array_action.get_generated_code())
        if self.read_old_to:
            gc.get_apply().writeln(
                "{} = {}.execute({});".format(
                    target["handle"], action_name, self.index_to_write
                )
            )
        else:
            gc.get_apply().writeln(
                "{}.execute({});".format(action_name, self.index_to_write)
            )
        return gc

class XORSharedArray(Command):
    def __init__(
        self,
        shared_array,
        map_var,
        index_to_xor,
        read_new_to=None,
        env=None,
    ):
        self.shared_array = shared_array
        self.map_var = map_var
        self.index_to_xor = index_to_xor
        self.read_new_to = read_new_to
        self.env = env

        if self.env != None:
            self.check()

    def check(self):
        var_exists(self.shared_array, self.env)
        if self.read_new_to:
            var_exists(self.read_new_to, self.env)
            var_is_of_type(self.read_new_to, self.env.get_varinfo(self.shared_array)["type"][2], self.env)
            is_writeable(self.read_new_to, self.env)

    def get_generated_code(self):
        gc = GeneratedCode()
        if self.read_new_to is not None:
            target = self.env.get_varinfo(self.read_new_to)
        array = self.env.get_varinfo(self.shared_array)
        index_type = array["type"][1]
        value_type = array["type"][2]
        map = self.env.get_varinfo(self.map_var)
        action_name = "xor_shared_array_action_" + UID.get()
        apply_lines = ["to_store = to_store ^ {};".format(map["handle"])]
        parameters = [{"mode": "inout", "type": value_type, "name": "to_store"}]
        if self.read_new_to:
            apply_lines.append("to_return = to_store;")
            parameters.append(
                {"mode": "out", "type": value_type, "name": "to_return"}
            )
        xor_shared_array_action = SharedArrayAction(
            action_name,
            self.shared_array,
            value_type,
            value_type,
            index_type,
            parameters,
            apply_lines,
        )
        gc.concat(xor_shared_array_action.get_generated_code())
        if self.read_new_to:
            gc.get_apply().writeln(
                "{} = {}.execute({});".format(
                    target["handle"], action_name, self.index_to_xor
                )
            )
        else:
            gc.get_apply().writeln(
                "{}.execute({});".format(action_name, self.index_to_xor)
            )
        return gc


class ReadSharedArray(Command):
    def __init__(
        self, shared_array, value_type, index_type, index_to_read, read_to, env=None
    ):
        self.shared_array = shared_array
        self.value_type = value_type
        self.index_type = index_type
        self.index_to_read = index_to_read
        self.read_to = read_to
        self.env = env

        if self.env != None:
            self.check()

    def check(self):
        var_exists(self.read_to, self.env)
        var_is_of_type(self.read_to, self.value_type, self.env)
        is_writeable(self.read_to, self.env)

    def get_generated_code(self):
        gc = GeneratedCode()
        declaration = gc.get_decl()
        target = self.env.get_varinfo(self.read_to)
        action_name = "read_shared_array_action_" + UID.get()
        apply_lines = ["to_return = stored_value;"]
        parameters = [
            {"mode": "inout", "type": self.value_type, "name": "stored_value"},
            {"mode": "out", "type": self.value_type, "name": "to_return"},
        ]
        read_shared_array_action = SharedArrayAction(
            action_name,
            self.shared_array,
            self.value_type,
            self.value_type,
            self.index_type,
            parameters,
            apply_lines,
        )
        gc.concat(read_shared_array_action.get_generated_code())
        gc.get_apply().writeln(
            "{} = {}.execute({});".format(
                target["handle"], action_name, self.index_to_read
            )
        )
        return gc


class GreaterThanTable(StrictComparator):
    def get_generated_code(self):
        gc = GeneratedCode()
        t = self.env.get_varinfo(self.target)
        a = self.env.get_varinfo(self.operand_a)
        b = self.env.get_varinfo(self.operand_b)
        declaration = gc.get_decl()
        table_name = "eval_table_" + UID.get()
        apply = gc.get_apply()
        difference_variable = "difference_variable_" + UID.get()
        setter_action = "setter_action_" + UID.get()
        declaration.writeln(
            "{} {};".format(a["type"].get_p4_type(), difference_variable)
        )
        for bool_val in ["true", "false"]:
            declaration.writeln("action {}_{}() {{".format(setter_action, bool_val))
            declaration.increase_indent()
            declaration.writeln(
                "{} = {};".format(t["handle"], 1 if bool_val == "true" else 0)
            )
            declaration.decrease_indent()
            declaration.writeln("}")
        type_size_in_bits = a["type"].get_size() * 8
        zero_entry = (
            "0b" + "0" * type_size_in_bits + "&&&" + "0b" + "1" * type_size_in_bits
        )
        sign_entry = (
            "0b"
            + "0" * type_size_in_bits
            + "&&&"
            + "0b1"
            + "0" * (type_size_in_bits - 1)
        )
        actions = [setter_action + "_true", setter_action + "_false"]
        key = [{"name": difference_variable, "match_type": "ternary"}]
        size = 2
        const_entries = [
            {"value": zero_entry, "action": setter_action + "_false", "parameters": []},
            {"value": sign_entry, "action": setter_action + "_false", "parameters": []},
        ]
        default_action = setter_action + "_true"
        eval_table = Table(
            table_name, actions, key, size, const_entries, default_action
        )
        gc.concat(eval_table.get_generated_code())

        apply.writeln(
            "{} = {} - {};".format(difference_variable, a["handle"], b["handle"])
        )
        apply.writeln("{}.apply();".format(table_name))
        return gc

    def execute(self, test_env):
        test_env[self.target] = test_env[self.operand_a] > test_env[self.operand_b]


class SmallerThanTable(StrictComparator):
    def get_generated_code(self):
        gc = GeneratedCode()
        t = self.env.get_varinfo(self.target)
        a = self.env.get_varinfo(self.operand_a)
        b = self.env.get_varinfo(self.operand_b)
        declaration = gc.get_decl()
        table_name = "eval_table_" + UID.get()
        apply = gc.get_apply()
        difference_variable = "difference_variable_" + UID.get()
        setter_action = "setter_action_" + UID.get()
        declaration.writeln(
            "{} {};".format(a["type"].get_p4_type(), difference_variable)
        )
        for bool_val in ["true", "false"]:
            declaration.writeln("action {}_{}() {{".format(setter_action, bool_val))
            declaration.increase_indent()
            declaration.writeln(
                "{} = {};".format(t["handle"], 1 if bool_val == "true" else 0)
            )
            declaration.decrease_indent()
            declaration.writeln("}")
        type_size_in_bits = a["type"].get_size() * 8
        zero_entry = (
            "0b" + "0" * type_size_in_bits + "&&&" + "0b" + "1" * type_size_in_bits
        )
        sign_entry = (
            "0b1"
            + "0" * (type_size_in_bits - 1)
            + "&&&"
            + "0b1"
            + "0" * (type_size_in_bits - 1)
        )
        actions = [setter_action + "_true", setter_action + "_false"]
        key = [{"name": difference_variable, "match_type": "ternary"}]
        size = 2
        const_entries = [
            {"value": zero_entry, "action": setter_action + "_false", "parameters": []},
            {"value": sign_entry, "action": setter_action + "_true", "parameters": []},
        ]
        default_action = setter_action + "_false"
        eval_table = Table(
            table_name, actions, key, size, const_entries, default_action
        )
        gc.concat(eval_table.get_generated_code())

        apply.writeln(
            "{} = {} - {};".format(difference_variable, a["handle"], b["handle"])
        )
        apply.writeln("{}.apply();".format(table_name))
        return gc

    def execute(self, test_env):
        test_env[self.target] = test_env[self.operand_a] < test_env[self.operand_b]


class EqualTable(StrictComparator):
    def get_generated_code(self):
        gc = GeneratedCode()
        t = self.env.get_varinfo(self.target)
        a = self.env.get_varinfo(self.operand_a)
        b = self.env.get_varinfo(self.operand_b)
        declaration = gc.get_decl()
        table_name = "eval_table_" + UID.get()
        apply = gc.get_apply()
        difference_variable = "difference_variable_" + UID.get()
        setter_action = "setter_action_" + UID.get()
        declaration.writeln(
            "{} {};".format(a["type"].get_p4_type(), difference_variable)
        )
        for bool_val in ["true", "false"]:
            declaration.writeln("action {}_{}() {{".format(setter_action, bool_val))
            declaration.increase_indent()
            declaration.writeln(
                "{} = {};".format(t["handle"], 1 if bool_val == "true" else 0)
            )
            declaration.decrease_indent()
            declaration.writeln("}")
        actions = [setter_action + "_true", setter_action + "_false"]
        key = [{"name": difference_variable, "match_type": "exact"}]
        size = 1
        const_entries = [
            {"value": 0, "action": setter_action + "_true", "parameters": []}
        ]
        default_action = setter_action + "_false"
        eval_table = Table(
            table_name, actions, key, size, const_entries, default_action
        )
        gc.concat(eval_table.get_generated_code())

        apply.writeln(
            "{} = {} - {};".format(difference_variable, a["handle"], b["handle"])
        )
        apply.writeln("{}.apply();".format(table_name))
        return gc

    def execute(self, test_env):
        test_env[self.target] = test_env[self.operand_a] == test_env[self.operand_b]


class NotEqualTable(StrictComparator):
    def get_generated_code(self):
        gc = GeneratedCode()
        t = self.env.get_varinfo(self.target)
        a = self.env.get_varinfo(self.operand_a)
        b = self.env.get_varinfo(self.operand_b)
        declaration = gc.get_decl()
        table_name = "eval_table_" + UID.get()
        apply = gc.get_apply()
        difference_variable = "difference_variable_" + UID.get()
        setter_action = "setter_action_" + UID.get()
        declaration.writeln(
            "{} {};".format(a["type"].get_p4_type(), difference_variable)
        )
        for bool_val in ["true", "false"]:
            declaration.writeln("action {}_{}() {{".format(setter_action, bool_val))
            declaration.increase_indent()
            declaration.writeln(
                "{} = {};".format(t["handle"], 1 if bool_val == "true" else 0)
            )
            declaration.decrease_indent()
            declaration.writeln("}")
        actions = [setter_action + "_true", setter_action + "_false"]
        key = [{"name": difference_variable, "match_type": "exact"}]
        size = 1
        const_entries = [
            {"value": 0, "action": setter_action + "_false", "parameters": []}
        ]
        default_action = setter_action + "_true"
        eval_table = Table(
            table_name, actions, key, size, const_entries, default_action
        )
        gc.concat(eval_table.get_generated_code())

        apply.writeln(
            "{} = {} - {};".format(difference_variable, a["handle"], b["handle"])
        )
        apply.writeln("{}.apply();".format(table_name))
        return gc

    def execute(self, test_env):
        test_env[self.target] = test_env[self.operand_a] != test_env[self.operand_b]


class AssignWithHash(StrictAssignVar):
    def get_generated_code(self):
        gc = GeneratedCode()
        s = self.env.get_varinfo(self.source)
        t = self.env.get_varinfo(self.target)
        gc.get_apply().writeln(
            "@in_hash{{ {} = {}; }}".format(t["handle"], s["handle"])
        )
        return gc



class Digest(Command):
    def __init__(self, values, keys, env=None):
        self.values = values
        self.keys = keys
        self.env = env
        self.id = UID.get()[3:]

    def check(self):
        pass

    def get_generated_code(self):
        self.values = [(self.env.get_varinfo(value).get_handle(), self.env.get_varinfo(value).get_type()) for value in self.values]
        gc = GeneratedCode()
        names = [
            (name.split(".")[-1] + "_" + str(UID.get()), given_type)
            for name, given_type, in self.values
        ]
        self.digest_name, digest_code = gen_struct(names, "generated_digest")
        gc.get_or_create("ingress_deparser_declaration").writeln(
            "Digest<{}>() {};".format(self.digest_name, self.digest_name)
        )
        gc.get_headers().write(digest_code)
        gc.get_or_create("ingress_deparser_apply").writeln(
            "if (ig_dprsr_md.digest_type=={}){{".format(self.id)
        )
        gc.get_or_create("ingress_deparser_apply").increase_indent()
        pack_list_types = ",".join([value[0] for value in self.values])
        gc.get_or_create("ingress_deparser_apply").writeln(
            "{}.pack({{{}}});".format(self.digest_name, pack_list_types)
        )
        gc.get_or_create("ingress_deparser_apply").decrease_indent()
        gc.get_or_create("ingress_deparser_apply").writeln("}")
        match = []
        for key in self.keys:
            match.append(self.env.get_varinfo(key))
        declaration = gc.get_decl()
        table_name = "set_digest_or_drop_table_" + UID.get()
        apply = gc.get_apply()
        setter_action = "setter_action_" + UID.get()
        declaration.writeln("action {}() {{".format(setter_action))
        declaration.increase_indent()
        declaration.writeln("ig_dprsr_md.digest_type = {};".format(self.id))
        declaration.decrease_indent()
        declaration.writeln("}")
        declaration.writeln("action drop_packet() {")
        declaration.increase_indent()
        declaration.writeln("ig_dprsr_md.drop_ctl = 0x1;")
        declaration.decrease_indent()
        declaration.writeln("}")
        actions = [setter_action, "drop_packet"]
        try:
            key = [
                {"name": part_key["handle"], "match_type": "exact"} for part_key in match
            ]
        except TypeError:
            key = [
                {"name": part_key.get_handle(), "match_type": "exact"} for part_key in match
            ]
        size = 1
        const_entries = []
        default_action = "drop_packet"
        eval_table = Table(
            table_name, actions, key, size, const_entries, default_action
        )
        gc.concat(eval_table.get_generated_code())
        apply.writeln("{}.apply();".format(table_name))
        return gc


class CheckControlPlaneSet(Command):
    def __init__(self, keys, target, table_name = None, env=None):
        self.target = target
        self.keys = keys
        self.table_name = table_name
        self.env = env

    def get_generated_code(self):
        gc = GeneratedCode()
        t = self.env.get_varinfo(self.target)
        match = []
        for key in self.keys:
            match.append(self.env.get_varinfo(key))
        declaration = gc.get_decl()
        table_name = ("exact_match_table_" + UID.get()) if self.table_name is None else self.table_name
        apply = gc.get_apply()
        setter_action = "setter_action_" + UID.get()
        for bool_val in ["true", "false"]:
            declaration.writeln("action {}_{}() {{".format(setter_action, bool_val))
            declaration.increase_indent()
            declaration.writeln(
                "{} = {};".format(t["handle"], 1 if bool_val == "true" else 0)
            )
            declaration.decrease_indent()
            declaration.writeln("}")
        actions = [setter_action + "_true", setter_action + "_false"]
        try:
            key = [
                {"name": part_key["handle"], "match_type": "exact"} for part_key in match
            ]
        except TypeError:
            key = [
                {"name": part_key.get_handle(), "match_type": "exact"} for part_key in match
            ]
        size = 1
        const_entries = []
        default_action = setter_action + "_false"
        eval_table = Table(
            table_name, actions, key, size, const_entries, default_action
        )
        gc.concat(eval_table.get_generated_code())
        apply.writeln("{}.apply();".format(table_name))
        return gc

    def check(self):
        pass

    def execute(self, test_env):
        pass

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
            match.append(self.env.get_varinfo(key))
        declaration = gc.get_decl()
        table_name = "exact_match_table_" + UID.get()
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
                {"name": part_key["handle"], "match_type": "exact"} for part_key in match
            ]
        except TypeError:
            key = [
                {"name": part_key.get_handle(), "match_type": "exact"} for part_key in match
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

class DropPacket(Command):
    def __init__(self, env=None):
        self.env = env

    def get_generated_code(self):
        gc = GeneratedCode()
        apply = gc.get_apply()
        apply.writeln("ig_dprsr_md.drop_ctl = 0x1;")
        return gc

    def check(self):
        pass

    def execute(self, test_env):
        pass


class UpdateLPF(Command):
    def __init__(self,target,source,index,value,env=None):
        self.target = target
        self.source = source
        self.index = index
        self.value = value
        self.env = env
    
        if self.env!=None:
            self.check()
            
    def check(self):
        var_exists(self.target,self.env)
        is_writeable(self.target,self.env)
        var_exists(self.source,self.env)
        var_exists(self.index,self.env)
        var_exists(self.value,self.env)
    
    def get_generated_code(self):
        gc = GeneratedCode()
        si  = self.env.get_varinfo(self.source)
        ti  = self.env.get_varinfo(self.target)
        vi  = self.env.get_varinfo(self.value)
        ii  = self.env.get_varinfo(self.index)
        gc.get_apply().writeln(f"{ti['handle']} = {si['handle']}.execute({vi['handle']},{ii['handle']});")
        return gc
    
    def execute(self,test_env):
        raise Exception("Not implemented")

        