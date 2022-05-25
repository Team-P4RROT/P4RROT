from p4rrot.generator_tools import *

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

#This class is meant to be used only for the implementation of commands not in actual p4rrot user code
class SharedArrayAction:
    def __init__(
        self,
        name,
        shared_array_name,
        input_type,
        output_type,
        index_type,
        parameters,
        apply_lines = []
    ):
        self.name = name
        self.shared_array_name = shared_array_name
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
                self.shared_array_name,
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