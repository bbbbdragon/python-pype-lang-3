from pype3.fargs import embedded_pype,assoc,concat,l,append,dissoc,build_dict,merge,_
from pype3.helpers import dct_dissoc,dct_assoc,dct_merge

##########
# MACROS #
##########

def ep(*fArgs):

    return [embedded_pype,*fArgs]


def iff(condition,fArg):

    return {condition:fArg,
            'else':_}


def ift(condition,fArg):

    return {condition:fArg,
            'else':False}
    

def ifp(*fArgs):
    
    return {_:ep(*fArgs),
            'else':_}


def iftp(*fArgs):
    
    return {_:ep(*fArgs),
            'else':False}


def is_true(condition):

    return {condition:True,
            'else':False}


def db(*fArgs):

    return [build_dict,*fArgs]


def dbp(*fArgs):

    return [d,fArgs[0],_p(*fArgs[1:])]


def select(*fArgs):

    return {fArg:_[fArg] for fArg in fArgs}



def a(*fArgs):

    return [assoc,*fArgs]

def ap(*fArgs):

    return [assoc,fArgs[0],ep(*fArgs[1:])]


def m(fArg):

    return [merge,fArg]


def mp(*fArgs):

    return [merge,fArgs[0],ep(*fArgs[1:])]


def d(*fArgs):

    return [dissoc,*fArgs]


def squash(fArg):

    return (dct_dissoc,(dct_merge,_,_[fArg]),fArg)


def tup(*fArgs):

    return [l,*fArgs]


def app(*fArgs):

    return [append,*fArgs]


def c(*fArgs):

    return [concat,*fArgs]


def change(fromKeyFArg,toKeyFArg):

    return (dct_dissoc,(dct_assoc,_,toKeyFArg,_[fromKeyFArg]),fromKeyFArg)
