from p4rrot.generator_tools import *


def var_exists(vname:str,env:Environment):
    assert env.has_var(vname), 'Undefined name: {}'.format(vname)


def vars_have_the_same_type(a:str,b:str,env:Environment):
    assert env.get_varinfo(a)['type']==env.get_varinfo(b)['type'], 'Variables {} and {} must be the same type'.format(a,b)


def is_writeable(vname:str,env:Environment):
    info = env.get_varinfo(vname)
    if 'writeable' in info and info['writeable']==True:
        return
    raise Exception('{} is not writeable'.format(vname))
    