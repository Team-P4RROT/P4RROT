from p4rrot.known_types import KnownType
from typing import Dict, List, Tuple
from p4rrot.standard_fields import *
from p4rrot.generator_tools import *
from p4rrot.checks import *

class UsingBlock(Block):
    def __init__(self, env, parent_block):
        super().__init__(env)
        self.parent_block = parent_block

    def EndUsing(self):
        return self.parent_block

class Using(Command):
    def __init__(
        self,
        name,
        register_name,
        input_type,
        output_type,
        index_type,
        parameters,
        using_block = None
    ):
        self.name = name
        self.register_name = register_name
        self.input_type = input_type
        self.output_type = output_type
        self.index_type = index_type
        self.using_block = using_block
        self.parameters = parameters
        self.env = None

    def get_generated_code(self):
        gc = GeneratedCode()
        declaration = gc.get_decl()
        declaration.writeln(
            "RegisterAction<{},{},{}>({}) {} = {{".format(
                self.input_type,
                self.index_type,
                self.output_type,
                self.register_name,
                self.name,
            )
        )
        declaration.write("void apply(")
        not_first_parameter = False
        for parameter in self.parameters:
            if not_first_parameter:
                declaration.write(", ")
            declaration.write("{} {} {}".format(parameter["mode"], parameter["type"], parameter["name"]))
            not_first_parameter = True
        declaration.writeln("){")
        declaration.increase_indent()
        declaration.increase_indent()
        tmp = self.using_block.get_generated_code()
        gc.concat(tmp)
        declaration.decrease_indent()
        declaration.writeln("}")
        declaration.decrease_indent()
        declaration.writeln("};")
        return gc

    def should_return(self):
        return self.using_block == None

    def get_return_object(self, parent):
        self.using_block = UsingBlock(self.env, parent)
        return self.using_block

class RegisterAction:
    def __init__(
        self,
        name,
        register_name,
        input_type,
        output_type,
        index_type,
        parameters,
        apply_lines = [],
        using_block = None
    ):
        self.name = name
        self.register_name = register_name
        self.input_type = input_type
        self.output_type = output_type
        self.index_type = index_type
        self.apply_lines = apply_lines
        self.parameters = parameters
        self.env = None

    def get_generated_code(self):
        gc = GeneratedCode()
        declaration = gc.get_decl()
        declaration.writeln(
            "RegisterAction<{},{},{}>({}) {} = {{".format(
                self.input_type.get_p4_type(),
                self.index_type.get_p4_type(),
                self.output_type.get_p4_type(),
                self.register_name,
                self.name,
            )
        )
        declaration.write("void apply(")
        not_first_parameter = False
        for parameter in self.parameters:
            if not_first_parameter:
                declaration.write(", ")
            declaration.write("{} {} {}".format(parameter["mode"], parameter["type"].get_p4_type(), parameter["name"]))
            not_first_parameter = True
        declaration.writeln("){")
        declaration.increase_indent()
        declaration.increase_indent()
        for line in self.apply_lines:
            declaration.writeln(line)
        declaration.decrease_indent()
        declaration.writeln("}")
        declaration.decrease_indent()
        declaration.writeln("};")
        return gc

    def should_return(self):
        return self.using_block == None

    def get_return_object(self, parent):
        self.using_block = UsingBlock(self.env, parent)
        return self.using_block

class IncrementRegister(Command):

    def __init__(self, register, number_type, index_type, index_to_increase, step = 1, read_new_to = None, env=None):
        self.register = register
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
            is_writeable(self.read_new_to, self.env)

    def get_generated_code(self):
        gc = GeneratedCode()
        declaration = gc.get_decl()
        if self.read_new_to is not None:
            target = self.env.get_varinfo(self.read_new_to)
        action_name = "increment_register_action_" + UID.get()
        apply_lines = ["to_store = to_store + {};".format(self.step)]
        parameters = [{"mode" : "inout", "type" : self.number_type, "name" : "to_store"}]
        if self.read_new_to:
            apply_lines.append("to_return = to_store;")
            parameters.append({"mode" : "out", "type" : self.number_type, "name" : "to_return"})
        increment_register_action = RegisterAction(action_name, self.register, self.number_type, self.number_type, self.index_type, parameters, apply_lines)
        gc.concat(increment_register_action.get_generated_code())
        if self.read_new_to:
            gc.get_apply().writeln(
                "{} = {}.execute({});".format(target["handle"],action_name, self.index_to_increase)
            )
        else:
            gc.get_apply().writeln(
                "{}.execute({});".format(action_name, self.index_to_increase)
            )
        return gc

class DecrementRegister(Command):

    def __init__(self, register, number_type, index_type, index_to_decrease, step = 1, read_new_to = None, env=None):
        self.register = register
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
            is_writeable(self.read_new_to, self.env)

    def get_generated_code(self):
        gc = GeneratedCode()
        declaration = gc.get_decl()
        if self.read_new_to is not None:
            target = self.env.get_varinfo(self.read_new_to)
        action_name = "decrement_register_action_" + UID.get()
        apply_lines = ["to_store = to_store - {};".format(self.step)]
        parameters = [{"mode" : "inout", "type" : self.number_type, "name" : "to_store"}]
        if self.read_new_to:
            apply_lines.append("to_return = to_store;")
            parameters.append({"mode" : "out", "type" : self.number_type, "name" : "to_return"})
        decrement_register_action = RegisterAction(action_name, self.register, self.number_type, self.number_type, self.index_type, parameters, apply_lines)
        gc.concat(decrement_register_action.get_generated_code())
        if self.read_new_to:
            gc.get_apply().writeln(
                "{} = {}.execute({});".format(target["handle"],action_name, self.index_to_decrease)
            )
        else:
            gc.get_apply().writeln(
                "{}.execute({});".format(action_name, self.index_to_decrease)
            )
        return gc

class WriteRegister(Command):

    def __init__(self, register, value_type, index_type, index_to_write, value_to_write, read_new_to = None, env=None):
        self.register = register
        self.value_type = value_type
        self.index_type = index_type
        self.index_to_write = index_to_write
        self.value_to_write = value_to_write
        self.read_new_to = read_new_to
        self.env = env

        if self.env != None:
            self.check()

    def check(self):
        if self.read_new_to:
            var_exists(self.read_new_to, self.env)
            is_writeable(self.read_new_to, self.env)

    def get_generated_code(self):
        gc = GeneratedCode()
        declaration = gc.get_decl()
        if self.read_new_to is not None:
            target = self.env.get_varinfo(self.read_new_to)
        action_name = "write_register_action_" + UID.get()
        apply_lines = ["to_store = {};".format(self.value_to_write)]
        parameters = [{"mode" : "inout", "type" : self.number_type, "name" : "to_store"}]
        if self.read_new_to:
            apply_lines.append("to_return = to_store;")
            parameters.append({"mode" : "out", "type" : self.number_type, "name" : "to_return"})
        write_register_action = RegisterAction(action_name, self.register, self.value_type, self.value_type, self.index_type, parameters, apply_lines)
        gc.concat(write_register_action.get_generated_code())
        if self.read_new_to:
            gc.get_apply().writeln(
                "{} = {}.execute({});".format(target["handle"],action_name, self.index_to_write)
            )
        else:
            gc.get_apply().writeln(
                "{}.execute({});".format(target["handle"],action_name, self.index_to_write)
            )
        return gc

class ReadRegister(Command):

    def __init__(self, register, value_type, index_type, index_to_read, value_to_read, read_to, env=None):
        self.register = register
        self.value_type = value_type
        self.index_type = index_type
        self.index_to_read = index_to_read
        self.value_to_read = value_to_read
        self.read_to = read_to
        self.env = env

        if self.env != None:
            self.check()

    def check(self):
        var_exists(self.read_to, self.env)
        is_writeable(self.read_to, self.env)

    def get_generated_code(self):
        gc = GeneratedCode()
        declaration = gc.get_decl()
        target = self.env.get_varinfo(self.read_to)
        action_name = "read_register_action_" + UID.get()
        apply_lines = ["to_return = stored_value;"]
        parameters = [{"mode" : "inout", "type" : self.value_type, "name" : "stored_value"}, {"mode" : "out", "type" : self.number_type, "name" : "to_return"}]
        read_register_action = RegisterAction(action_name, self.register, self.value_type, self.value_type, self.index_type, parameters, apply_lines)
        gc.concat(read_register_action.get_generated_code())
        gc.get_apply().writeln(
            "{} = {}.execute({});".format(target["handle"],action_name, self.index_to_read)
        )
        return gc