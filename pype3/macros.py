from pype3.fargs import embedded_pype,assoc,concat,l,append,dissoc,build_list,build_dict,merge,closure,_,_0,_1,deep_merge
from pype3.fargs import is_map,is_filter,is_mirror
from pype3.helpers import dct_dissoc,dct_assoc,dct_merge,ls_extend,zip_consec,get_call_or_false_core,singleton_dct,dcts_merge_deep,tup_dct
from pype3.func_helpers import deep_map,deep_filter
from pype3.type_checking import *
from pype3.vals import is_pype_val

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


def ext(*fArgs):

    return (ls_extend,_,*fArgs)


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


def cl_if(*fArgs):

    return cl(ifta(*fArgs))


def cl_has(key):

    return cl(ifta(is_dict,_[key]))


def cl_app(*fArgs):

    if not fArgs:

        return cl([h,x],app(x))

    return cl([h,x],app(*fArgs))


def consec(iterable,dct,n):

    return ep((zip_consec,iterable,n),
              [(get_call_or_false_core,dct,True,_)],
              {_})


def consec_dct(iterable,dct,n):

    return ep((zip_consec,iterable,n),
              [l(_,(get_call_or_false_core,dct,True,_))],
              {_1},
              [(singleton_dct,_1,_0)],
              dcts_merge_deep,
             )
      


# def consec_get():
def embed(ln,idx=None):

    if ln == 1:

        return l(_)


    if idx == None:

        idx=0

    if idx == ln-2:

        return l(_[idx],_[idx+1])

    return l(_[idx],embed(ln,idx+1)) 


def td(fArg1,fArg2):

    return ep([l(fArg1,fArg2)],
              tup_dct)


def tdm(fArg):

    return td(_,fArg)


if __name__=='__main__':

    print(embed(_))
