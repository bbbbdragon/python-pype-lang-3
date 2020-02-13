from pype3.fargs import embedded_pype,assoc,concat,l,append,dissoc,build_list,build_dict,merge,closure,_,deep_merge
from pype3.fargs import is_map,is_filter
from pype3.helpers import dct_dissoc,dct_assoc,dct_merge
from pype3.func_helpers import deep_map,deep_filter

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


def dm(fArg):

    return [deep_merge,fArg]


def d(*fArgs):

    return [dissoc,*fArgs]


def squash(fArg):

    return (dct_dissoc,(dct_merge,_,_[fArg]),fArg)


def l(*fArgs):

    return [build_list,*fArgs]


def app(*fArgs):

    return [append,*fArgs]


def c(*fArgs):

    return [concat,*fArgs]


def change(fromKeyFArg,toKeyFArg):

    return (dct_dissoc,(dct_assoc,_,toKeyFArg,_[fromKeyFArg]),fromKeyFArg)


def cl(*fArgs):

    return [closure,*fArgs]


def tup(*fArgs):

    return fArgs,


def ea(*keysAndVal):

    key=keysAndVal[0]

    if len(keysAndVal) == 2:

        val=keysAndVal[1]

        return a(key,val)

    return a(key,ep(_[key],ea(*keysAndVal[1:])))


def lm(callableFArg):

    return (callableFArg,_)


def ifa(*fArgs):

    if len(fArgs) == 1:

        return fArgs[0]

    return iff(fArgs[0],ifa(*fArgs[1:]))


def ifta(*fArgs):

    if len(fArgs) == 1:

        return is_true(fArgs[0])

    return ift(fArgs[0],ifta(*fArgs[1:]))


def dp(fArg,verify=None):

    if is_map(fArg):

        fArg=fArg[0]

        if verify is None:

            return (deep_map,_,fArg)

        else:

            return (deep_map,_,fArg,verify)

    if is_filter(fArg):
        
        fArg=next(iter(fArg))

        return (deep_filter,_,fArg)

    if is_reduce(fArg):

        reduceFArg=fArg[0][0]
        
        '''
        if len(fArgs) == 2:

            iterable=fArgs[1]

            return (reduce_deep,_,_,reduceFArg)
        '''
        if len(fArgs) == 3:

            startVal=fArgs[1]
            iterable=fArgs[2]

            return (reduce_deep,startVal,_,reduceFArg)

    return None
