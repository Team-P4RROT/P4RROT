#
# Useful classess and functions for code generation
#

import os
from p4rrot.known_types import KnownType
from typing import Dict, List, Tuple
from p4rrot.standard_fields import *


class UID:
    """
    Static class implementing a singleton pattern to generate unique ID-s.
    """

    next_id = 0

    def get():
        UID.next_id += 1
        return 'uid'+str(UID.next_id)

    def reset():
        UID.next_id = 0


class CodeWriter:
    """
    Simple text generator with indentation and new line management.
    """

    def __init__(self):
        self.code = ''
        self.indent = 0

    def write(self, text: str, indent: bool = False, indent_new_lines=False):
        padding = ''
        if indent_new_lines:
            padding = '\t'*self.indent
            if len(self.code)>0 and self.code[-1] == '\n':
                self.code += padding

        if len(text)>0 and text[-1]=='\n':
            text_to_insert = text[:-1].replace('\n', '\n'+padding)+'\n'
        else:
            text_to_insert = text.replace('\n', '\n'+padding)

        if not indent:
            self.code += text_to_insert
        else:
            self.code += '\t'*max(0, self.indent) + text_to_insert

    def new_line(self):
        self.code += '\n'

    def writeln(self, text: str):
        self.code += '\t'*max(0, self.indent)+text+'\n'

    def increase_indent(self):
        self.indent += 1

    def decrease_indent(self):
        self.indent -= 1

    def get_code(self):
        return self.code


class GeneratedCode:
    """
    The generated P4 code for a functionality may affect 5 parts of the sourcecode represented by this class.
    - Header and struct declarations
    - The list of used headers
    - Parser states
    - Declarations inside the control block (tables, registers, ...)
    - Statments within the apply block
    """

    def __init__(self):
        self.headers = CodeWriter()
        self.hdrlist = CodeWriter()
        self.parser = CodeWriter()
        self.decl = CodeWriter()
        self.apply = CodeWriter()
        self.arbitrary_writers = {}

    def get_headers(self):
        return self.headers

    def get_hdrlist(self):
        return self.hdrlist

    def get_parser(self):
        return self.parser

    def get_decl(self):
        return self.decl

    def get_apply(self):
        return self.apply
    
    def get_or_create(self, gc_name):
        if not gc_name in self.arbitrary_writers:
            self.arbitrary_writers[gc_name] = CodeWriter()
        return self.arbitrary_writers[gc_name]

    def dump(self,output_dir:str):
        f = open(os.path.join(output_dir,'a_headers.p4'),'w')
        f.write(self.get_headers().get_code())

        f = open(os.path.join(output_dir,'a_hdrlist.p4'),'w')
        f.write(self.get_hdrlist().get_code())

        f = open(os.path.join(output_dir,'a_declarations.p4'),'w')
        f.write(self.get_decl().get_code())

        f = open(os.path.join(output_dir,'a_chains.p4'),'w')
        f.write(self.get_parser().get_code())

        f = open(os.path.join(output_dir,'a_apply.p4'),'w')
        f.write(self.get_apply().get_code())

        
        for gc_name in self.arbitrary_writers:
            file_name = 'a_' + gc_name + '.p4'
            f = open(os.path.join(output_dir,file_name), "w")
            f.write(self.arbitrary_writers[gc_name].get_code())

    def	concat(self,other,add_padding=True):
        self.headers.write(other.headers.get_code(),indent_new_lines=add_padding)
        self.hdrlist.write(other.hdrlist.get_code(),indent_new_lines=add_padding)
        self.parser.write(other.parser.get_code(),indent_new_lines=add_padding)
        self.decl.write(other.decl.get_code(),indent_new_lines=add_padding)
        self.apply.write(other.apply.get_code(),indent_new_lines=add_padding)
        
        for arbitrary_writer in other.arbitrary_writers:
            self.get_or_create(arbitrary_writer).write(other.arbitrary_writers[arbitrary_writer].get_code(),indent_new_lines=add_padding)



def gen_struct(description: List[Tuple[str, KnownType]], name: str = None):
    """
    Generate struct definitions. The description paramerter is a list of touples
    """

    cw = CodeWriter()

    # decide name
    uid = UID.get()
    if name == None:
        name = "genstruct"
    name = name+"_"+uid

    # generate definition
    cw.writeln("struct "+name+"{")
    for n, t in description:
        cw.writeln("\t{} {};".format(t.get_p4_type(), n))
    cw.writeln("}")
    return name, cw.get_code()

def gen_simple_parser_state(next_state: str, target_state: str, lookahead_struct=None, state_name: str = ""):

    gc = GeneratedCode()

    # state name
    if state_name == "":
        state_name = 'check_'+UID.get()
    gc.get_parser().writeln('state {}{{'.format(state_name))
    gc.get_parser().increase_indent()

    # lookahead if required
    if lookahead_struct != None:
        struct_name, header_code = gen_struct(lookahead_struct)
        gc.get_headers().write(header_code)
        gc.get_parser().writeln("{} tmp = pkt.lookahead<{}>();\n".format(struct_name, struct_name))

    # select
    def get_handle(f):
        if isinstance(f, StandardField):
            return f.get_handle()
        elif lookahead_struct != None:
            d = {k: 'tmp.'+f for k, _ in lookahead_struct}
            if f in d:
                return d[f]
        raise Exception('unknown field '+str(f))
    #gc.get_parser().increase_indent()
    gc.get_parser().writeln("transition "+ target_state+";")

    gc.get_parser().decrease_indent()
    gc.get_parser().writeln('}')

    return state_name, gc


def gen_decision_parser_state(conditions: str, next_state: str, target_state: str, lookahead_struct=None, state_name: str = ""):

    gc = GeneratedCode()

    # state name
    if state_name == "":
        state_name = 'check_'+UID.get()
    gc.get_parser().writeln('state {}{{'.format(state_name))
    gc.get_parser().increase_indent()

    # lookahead if required
    if lookahead_struct != None:
        struct_name, header_code = gen_struct(lookahead_struct)
        gc.get_headers().write(header_code)
        gc.get_parser().writeln("{} tmp = pkt.lookahead<{}>();\n".format(struct_name, struct_name))

    # select
    def get_handle(f):
        if isinstance(f, StandardField):
            return f.get_handle()
        elif lookahead_struct != None:
            d = {k: 'tmp.'+f for k, _ in lookahead_struct}
            if f in d:
                return d[f]
        raise Exception('unknown field '+str(f))

    gc.get_parser().write("transition select(", indent=True)
    gc.get_parser().write(','.join([get_handle(c) for c, _ in conditions]))
    gc.get_parser().write("){")
    gc.get_parser().new_line()

    # cases
    gc.get_parser().increase_indent()
    gc.get_parser().writeln(
        '('+','.join([str(c) for _, c in conditions]) + ') : '+target_state+';')
    gc.get_parser().writeln('default: '+next_state+';')
    gc.get_parser().decrease_indent()
    gc.get_parser().writeln('}')

    gc.get_parser().decrease_indent()
    gc.get_parser().writeln('}')

    return state_name, gc


def gen_header(description,name=None):
    cw = CodeWriter()
    
    # decide name and handle
    uid = UID.get()
    if name==None:
        name="genhdr"
    handle = name+"_"+uid
    name = handle+'_h'
    
    # generate definition
    cw.writeln("header "+name+"{")
    for n,t in description:
        cw.writeln("\t{} {};".format(t.get_p4_type(),n))
    cw.writeln("}")
    return name,handle,cw.get_code()


def gen_header_parser_state(header_handle: str, state_name: str = ""):

    gc = GeneratedCode()

    # state name
    if state_name == "":
        state_name = 'parse_'+UID.get()
    gc.get_parser().writeln('state {}{{'.format(state_name))
    gc.get_parser().increase_indent()

    gc.get_parser().writeln('pkt.extract(hdr.{});'.format(header_handle))
    
    gc.get_parser().writeln('transition accept;')

    gc.get_parser().decrease_indent()
    gc.get_parser().writeln('}')

    return state_name, gc



class SharedElement:
    
    def get_name(self):
        raise NotImplementedError()

    def get_type(self):
        raise NotImplementedError()

    def get_generated_code(self):
        raise NotImplementedError()    
    
    def get_properties(self):
        return {}

class FlowProcessor:
    '''
    The FlowProcessor defines the input-output structures and the processing steps for a given packet.
    '''

    def __init__(self, istruct, ostruct=None, mstruct=None, locals=None, helpers=None, method='READ', iname=None, oname=None, standard_fields=[], state:List[SharedElement]=None, **kwargs):
        self.istruct = istruct
        self.ostruct = ostruct
        self.mstruct = mstruct
        self.locals = locals
        self.helpers = helpers
        self.method = method
        self.iname = iname
        self.oname = oname
        self.gc = None  # generated code
        self.ihandle = None
        self.iparser = None
        self.standard_fields = standard_fields
        self.state = []
        if state!=None:
            self.state = state

        self.iname, self.ihandle, self.icode = gen_header(self.istruct, self.iname)

        if self.ostruct!=None:
            self.oname, self.ohandle, self.ocode = gen_header(self.ostruct, self.oname)
        else:
            self.oname, self.ohandle, self.ocode = None, None, None

        if self.mstruct!=None:
            self.mname, self.mhandle, self.mcode = gen_header(self.mstruct)
        else:
            self.mname, self.mhandle, self.mcode = None, None, None

        self.env = Environment(self.istruct,self.ostruct,self.mstruct,self.locals,self.helpers,self.ihandle,self.ohandle,self.mhandle,self.standard_fields,state)

        self.block = Block(self.env)

    def get_generated_code(self,add_else=False):
        # check if it is already generated
        if self.gc != None:
            return self.gc
        self.gc = GeneratedCode()

        # header definitions
        self.gc.get_hdrlist().writeln('{} {};'.format(self.iname, self.ihandle))
        self.gc.get_headers().write(self.icode)

        if self.ostruct != None:
            self.gc.get_hdrlist().writeln('{} {};'.format(self.oname, self.ohandle))
            self.gc.get_headers().write(self.ocode)

        if self.mstruct != None:
            self.gc.get_hdrlist().writeln('{} {};'.format(self.mname, self.mhandle))
            self.gc.get_headers().write(self.mcode)

        # parser state
        iparser, tmpgc = gen_header_parser_state(self.ihandle,state_name='parse_'+self.ihandle)
        self.gc.concat(tmpgc)

        # apply parts
        self.gc.get_apply().writeln('if (hdr.{}.isValid()){{'.format(self.ihandle))
        self.gc.get_apply().increase_indent()

        if self.ostruct != None:
            self.gc.get_apply().writeln('hdr.{}.setValid();'.format(self.ohandle))
            self.gc.get_apply().writeln('#define OUTPUT_HEADER_SIZE {}'.format(hdr_len(self.ostruct)))
        else:
            self.gc.get_apply().writeln('#define OUTPUT_HEADER_SIZE {}'.format(hdr_len(self.istruct)))

        if self.mstruct != None:
            self.gc.get_apply().writeln('hdr.{}.setValid();'.format(self.mhandle))

        if self.locals != None:
            for n,t in self.locals:
                self.gc.get_apply().writeln('{} {};'.format(t.get_p4_type(),n))
        
        if self.helpers != None:
            for n,t in self.helpers:
                self.gc.get_decl().writeln('{} {};'.format(t.get_p4_type(),n))

        self.gc.concat(self.block.get_generated_code())

        if self.mstruct != None:
            self.gc.get_apply().writeln('hdr.{}.setInvalid();'.format(self.mhandle))

        if self.ostruct!=None:
            self.gc.get_apply().writeln('hdr.{}.setInvalid();'.format(self.ihandle))

        # adjust changes in packet size
        if self.ostruct!=None:
            diff = hdr_len(self.ostruct) - hdr_len(self.istruct)
            self.gc.get_apply().writeln('meta.size_growth = {};'.format(max(0,diff)))
            self.gc.get_apply().writeln('meta.size_loss = {};'.format(max(0,-diff)))

        
        self.gc.get_apply().writeln('#undef OUTPUT_HEADER_SIZE')
        self.gc.get_apply().decrease_indent()
        
        self.gc.get_apply().writeln('}')
        if add_else:
            self.gc.get_apply().write('else ')

        self.iparser = iparser

        return self.gc

    def get_ihandle(self) -> str:
        if self.gc==None:
            self.get_generated_code()
        return self.ihandle

    def get_iparser(self) -> str:
        if self.gc==None:
            self.get_generated_code()
        return self.iparser

    def add(self, command):
        return self.block.add(command)

    def get_env(self):
        return self.env

    def get_state(self):
        return self.state

    def test(self, test_env):
        return self.block.test(test_env)


class FlowSelector:
    '''
    The FlowSelector directs the packets towards a given FlowProcessor.
    '''

    def __init__(self,chain,conditions,flow_processor,lookahead_struct=None):
        self.chain = chain
        self.conditions = conditions
        self.lookahed_struct = lookahead_struct
        self.flow_processor = flow_processor
        self.gc = None
        self.name = None
        
    def get_generated_code(self,next_state:str):
        if self.gc==None:
            if self.conditions:
                self.name,self.gc = gen_decision_parser_state(self.conditions, next_state, 
                                    target_state=self.flow_processor.get_iparser(),
                                    lookahead_struct=self.lookahed_struct)
            else:
                self.name,self.gc = gen_simple_parser_state(next_state, 
                                    target_state=self.flow_processor.get_iparser(),
                                    lookahead_struct=self.lookahed_struct)
        return self.name,self.gc
    
    def get_chain(self):
        return self.chain


def generate_chain(chain_name:str,selectors:List[FlowSelector]):
    gc = GeneratedCode()
        
    next_state = 'accept'
    for s in reversed(selectors):
        state_name, tmp = s.get_generated_code(next_state=next_state)
        gc.concat(tmp)
        next_state = state_name
    
    gc.get_parser().writeln('#define CHAIN_{}'.format(chain_name.upper()))
    gc.get_parser().writeln('state chain_{}{{'.format(chain_name.lower()))
    gc.get_parser().increase_indent()
    gc.get_parser().writeln('transition {};'.format(next_state))    
    gc.get_parser().decrease_indent()
    gc.get_parser().writeln('}')
    
    return gc


class Solution:
    def __init__(self):
        self.selectors = []
        self.processors = []
        self.state = []
    
    def add_flow_processor(self,fp):
        self.processors.append(fp)
        for s in fp.get_state():
            if s not in self.state:
                self.state.append(s)
    
    def add_flow_selector(self,fs):
        self.selectors.append(fs)
    
    def add_state(self,stateful_element):
        self.state.append(stateful_element)
    
    def get_generated_code(self):
        gc = GeneratedCode()
        
        # generate stateful elements
        for s in self.state:
            tmp = s.get_generated_code()
            gc.concat(tmp)
        
        # generate processing parts
        for i, fp in enumerate(self.processors):
            tmp = fp.get_generated_code(add_else=(i < len(self.processors)-1))
            gc.concat(tmp)
            
        # generate parser chains
        chains = dict()
        for fs in self.selectors:
            if fs.get_chain() not in chains:
                chains[fs.get_chain()] = []
            chains[fs.get_chain()].append(fs)
            
        for chain_name,selectors in chains.items():
            tmp = generate_chain(chain_name,selectors)
            gc.concat(tmp)

        return gc

        

class Environment:
    
    def __init__(self,istruct,ostruct,mstruct,locals,helpers,iheader,oheader,mheader,standard_fields = [],state:List[SharedElement] = []):
        self.info = dict()
        self.standard_fields = standard_fields
        for n,t in istruct:
            if n in self.info:
                raise Exception('name "{}" is not unique'.format(n))
            self.info[n] = { 'name':n, 'type':t, 'writeable':True, 'place': 'istruct', 'handle':'hdr.{}.{}'.format(iheader,n) }
            
        if ostruct!=None:
            for n,t in ostruct:
                if n in self.info:
                    raise Exception('name "{}" is not unique'.format(n))
                self.info[n] = { 'name':n, 'type':t, 'writeable':True, 'place': 'ostruct', 'handle':'hdr.{}.{}'.format(oheader,n) }

        if mstruct!=None:            
            for n,t in mstruct:
                if n in self.info:
                    raise Exception('name "{}" is not unique'.format(n))
                self.info[n] = { 'name':n, 'type':t, 'writeable':True, 'place': 'mstruct', 'handle':'hdr.{}.{}'.format(mheader,n) }
            
        if locals!=None:            
            for n,t in locals:
                if n in self.info:
                    raise Exception('name "{}" is not unique'.format(n))
                self.info[n] = { 'name':n, 'type':t, 'writeable':True, 'place': 'locals', 'handle':'{}'.format(n) }

        if helpers!=None:            
            for n,t in helpers:
                if n in self.info:
                    raise Exception('name "{}" is not unique'.format(n))
                self.info[n] = { 'name':n, 'type':t, 'writeable':True, 'place': 'helpers', 'handle':'{}'.format(n) }

        if state!=None:
            for s in state:
                if s.get_name() in self.info:
                    raise Exception('name "{}" is not unique'.format(n))            
                self.info[s.get_name()] = { 'name':s.get_name(), 'type':s.get_type(), 'place': 'state', 'handle':s.get_name(), 'properties': s.get_properties() }


    def get_varinfo(self,vname:str):
        if vname not in self.info:
            for standard in self.standard_fields:
                if standard.get_handle() == vname:
                    #return standard
                    return { 'name':standard.get_handle(), 'type':standard.get_type(), 'writeable':True, 'place': 'standard', 'handle':standard.get_handle() }
        return self.info[vname]
    
    def has_var(self,vname:str):
        if vname not in self.info:
                for standard in self.standard_fields:
                    if standard.get_handle() == vname:
                        return True
                return False
        else:
            return True
        
        
        
class Command:
    
    def should_return(self):
        return False

    def get_generated_code(self):
        raise Exception('Not implemented by subclass')

    def has_env(self):
        return self.env!=None

    def set_env(self,env):
        self.env = env
    
class Block:
    
    def __init__(self,env):
        self.env = env
        self.seq = []
        
    def add(self,command:Command):
        if not command.has_env():
            command.set_env(self.env)
            command.check()
        
        self.seq.append(command)
        
        if command.should_return():
            return command.get_return_object(self)
        else:
            return self
        
    def get_generated_code(self):
        gc = GeneratedCode()
        for c in self.seq:
            gc.concat(c.get_generated_code())
        return gc
    
    def test(self,test_env):
        for s in self.seq:
            s.execute(test_env)
        return test_env
