from p4rrot.generator_tools import *

class Table:
    def __init__(self, name, actions, keys, size, const_entries, default_action, use_subtraction = False):
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
        declaration.writeln("actions = {")
        for action in self.actions:
            declaration.writeln("{};".format(action))
        declaration.writeln("}")
        declaration.writeln("key = {")
        declaration.increase_indent()
        for key in self.keys:
            declaration.writeln("{}: {};".format(key["name"], key["match_type"]))
        declaration.decrease_indent()
        declaration.writeln("}")
        declaration.writeln("size = {};".format(self.size))
        declaration.writeln("const default_action = {};".format(self.default_action))
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