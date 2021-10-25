from pype3.fargs import *
from pype3.build_helpers import *
from pype3.vals import LamTup,delam,is_bookmark,NameBookmark
from pype3.fargs import INDEX_ARG_DICT
from pype3.vals import LamTup,VarAssign
from pype3.type_checking import *
from itertools import groupby
from inspect import signature
from collections import defaultdict
from inspect import getsource
from ast import *
import hashlib
import types
import sys
import _operator
import builtins
import numpy as np
from functools import wraps
from copy import deepcopy
import pprint as pp
import astpretty
from inspect import currentframe
import types
import builtins
'''
This module contains the fArg-to-AST-node transformations.  It also contains
optimize_rec and optimize_f_args, which run these transformations on fArgs.
'''
#############
# CONSTANTS #
#############

NUMPY_UFUNCS=set(dir(np))
OPERATOR_FUNCS=set(dir(_operator))
MAJOR_TYPES=[int,str,float]
MAJOR_TYPES={typ:typ.__name__ for typ in MAJOR_TYPES}

##################
# CONSTANT NODES #
##################

ACCUM_STORE=Name(id='accum',ctx=Store())
ACCUM_LOAD=Name(id='accum',ctx=Load())
LAMBDA_ACCUM_LOAD=Name(id='lambda_accum',ctx=Load())

RETURN_ACCUM=[Return(value=ACCUM_LOAD)]
NUMPY_NAME=Name(id='np',ctx=Load())
OPERATOR_NAME=Name(id='_operator',ctx=Load())
PYPE_VALS_NODE=Attribute(value=Name(id='pype3',ctx=Load()),
                         attr='vals',
                         ctx=Load())
PYPE_HELPERS_NODE=Attribute(value=Name(id='pype3',ctx=Load()),
                            attr='helpers',
                            ctx=Load())
PYPE_OPTIMIZE_HELPERS_NODE=Attribute(value=Name(id='pype3',ctx=Load()),
                            attr='build_helpers',
                            ctx=Load())
IMPORT_BUILD=ImportFrom(module='pype3', 
                        names=[alias(name='build', asname=None)], 
                        level=0)
PYPE_RETURN_F_ARGS=Attribute(value=Name(id='pype3',ctx=Load()),
                             attr='p',
                             ctx=Load())
PYPE_FUNC=Attribute(value=Name(id='pype3',ctx=Load()),
                    attr='p',
                    ctx=Load())

LOADED_DICT_KEY=Name(id='k',ctx=Load())
LOADED_DICT_VALUE=Name(id='v',ctx=Load())
STORED_DICT_KEY=Name(id='k',ctx=Store())
STORED_DICT_VALUE=Name(id='v',ctx=Store())

IS_DICT_NODE=Attribute(value=PYPE_HELPERS_NODE,
                       attr='is_dict',
                       ctx=Load())

LOADED_LIST_ELEMENT=Name(id='list_element',ctx=Load())
STORED_LIST_ELEMENT=Name(id='list_element',ctx=Store())

DO_LAMBDA_ARG=Name(id='do_lambda_arg',ctx=Load())
CLOSURE_LAMBDA_ARG=Name(id='closure_lambda_arg',ctx=Load())
NONE_NODE=NameConstant(value=None)

#############################
# PRINT NODES FOR DEBUGGING #
#############################

PYPE_HELPERS_NODE=Attribute(value=Name(id='pype3',ctx=Load()),
                            attr='build_helpers',
                            ctx=Load())
PRINT_AND_EVAL_NODE=Attribute(value=PYPE_HELPERS_NODE,
                              attr='print_and_eval',
                              ctx=Load())
KEYSTEP_NODE=Attribute(value=PYPE_HELPERS_NODE,
                       attr='keystep',
                       ctx=Load())


###########
# HELPERS #
###########

def pype_call_node(args):

    return Call(func=PYPE_FUNC,
                args=args,
                keywords=[])


def is_f_arg_for_node(v):

    return is_f_arg(v) or is_bookmark(v)


def is_module(v):

    return isinstance(v,types.ModuleType)


def get_name(fArg):
    '''
    https://stackoverflow.com/questions/18425225/getting-the-name-of-a-variable-as-a-string/18425523
    '''
    callersLocalVars=currentframe().f_back.f_locals.items()
    varNames=[varName for (varName,varVal) in callersLocalVars if varVal is fArg]

    if not varNames:

        return varNames

    return varNames[0]


def get_module_alias(fArg):

    moduleName=fArg.__module__
    #print(f'{moduleName} is moduleName')
    #callersLocalVars=currentframe().f_back.f_globals.items()
    #names=[(varName,varVal) for (varName,varVal) in callersLocalVars \
    #          if isinstance(varVal,types.ModuleType)]
    #print(f'{names} is names')
    callersLocalVars=currentframe().f_back.f_locals.items()
    varNames=[varName for (varName,varVal) in callersLocalVars \
              if isinstance(varVal,types.ModuleType) \
              and varVal.__name__ == moduleName]

    if not varNames:

        return varNames

    return varNames[0]

###################
# DEBUGGING NODES #
###################

def print_and_eval_node(tree,fArg):

    return Call(func=KEYSTEP_NODE,
                args=[tree], 
                keywords=[])


def keystep_node(tree,fArg):

    try:

        treePrintout=astpretty.pformat(tree)

    except Exception as e:

        treePrintout=ast.dump(tree)

    fArgString=pp.pformat(fArg)

    return Call(func=PRINT_AND_EVAL_NODE,
                args=[tree,Str(s=treePrintout),Str(s=fArgString)], 
                keywords=[])


#################
# KWARGS HELPER #
#################

def args_to_keywords(callableArgs):

    return [keyword(arg=None,value=arg) for arg in callableArgs]



##########
# MIRROR #
##########

def mirror_node(fArgs,accum=ACCUM_LOAD,kwargs=False):
    # print('mirror_node')
    # print(f'{fArgs} is fArgs')
    # print(f'{accum} is accum')

    return accum


############
# CALLABLE #
############

import importlib

def module_attribute(moduleStrings):

    if len(moduleStrings) == 1:

        return Name(id=moduleStrings[0],ctx=Load())

    return Attribute(value=module_attribute(moduleStrings[1:]),
                     attr=moduleStrings[0],
                     ctx=Load())


def get_last_attribute(fArg):

    if isinstance(fArg,Call):

        return get_last_attribute(fArg.func)

    if isinstance(fArg,Attribute):

        return fArg.attr


def find_type(name):

    for typ,typName in MAJOR_TYPES.items():

        if hasattr(typ,name):

            return typName

    return ''


def function_node(fArg,accum=ACCUM_LOAD,kwargs=False):

    #print('>'*30)
    #print('function_node')
    #print(f'{fArg} is fArg')

    fArgName=fArg.__name__

    if fArgName in OPERATOR_FUNCS:

        return Attribute(value=OPERATOR_NAME,
                         attr=fArg.__name__,
                         ctx=Load())

    if fArgName in NUMPY_UFUNCS:

        return Attribute(value=NUMPY_NAME,
                         attr=fArg.__name__,
                         ctx=Load())

    #print(f'id is {fArg.__name__}')
    #print(f'moduRanle is {fArg.__module__}')
    #print(f'{hasattr(builtins,fArg.__name__)} is name in builtins')

    if fArg.__module__ is not None:

        if fArg.__module__ == '__main__':

            #print('is main module')

            return Name(id=fArgName,ctx=Load())

        #print(f'{get_module_alias(fArg)} is get_module_alias(fArg)')

        moduleStrings=fArg.__module__.split('.')
        
        moduleStrings.reverse()

        return Attribute(value=module_attribute(moduleStrings),
                         attr=fArg.__name__,
                         ctx=Load())

    # Else its a builtin?

    if hasattr(builtins,fArg.__name__):

        return Attrubute(value='builtins',
                         attr=fArg.__name__,
                         ctx=Load())

    typ=find_type(fArg.__name__)

    #print(f'type is {typ}')

    if typ:

        return Attribute(value=typ,
                         attr=fArg.__name__,
                         ctx=Load())
    
    return None


def callable_node_with_args(fArg,callableArgs,kwargs=False):

    #print('='*30)
    #print('callable node with args')
    #print(f'{fArg} is fArg')
    #print(f'{[dump(n) for n in callableArgs]} is callableArgs')

    argsOrKwargs={'args':callableArgs,
                  'keywords':[]}

    if kwargs:

        argsOrKwargs={'args':[],
                      'keywords':args_to_keywords(callableArgs)}

    if isinstance(fArg,Call):

        # It stops here!
        #print('is call')

        return Call(func=fArg,**argsOrKwargs)

    if hasattr(fArg,'__name__'):

        fArg=function_node(fArg)

    return Call(func=fArg,**argsOrKwargs)

                          

def callable_node(fArg,accumLoad=ACCUM_LOAD,kwargs=False):

    return callable_node_with_args(fArg,[accumLoad],kwargs=kwargs)



#############
# INDEX ARG #
#############

def index_arg_node(fArg,accum=ACCUM_LOAD,kwargs=False):

    return Subscript(value=accum,
                     slice=Index(value=Num(n=INDEX_ARG_DICT[fArg])),
                     ctx=Load())


#########
# INDEX #
#########

from operator import getitem

def has_getitem(fArgs):

    #print(f'is_getter(fArgs[0]) is {is_getter(fArgs[0])}')

    if not fArgs:

        return False

    if is_callable(fArgs) and fArgs == getitem:

        return True

    if (is_list(fArgs) or is_tuple(fArgs)) and len(fArgs) > 1:

        return has_getitem(fArgs[0])

    if is_getter(fArgs):

        #print(f'{fArgs} is getter')

        return True

    return False


#########
# SLICE #
#########


def slice_node(fArg,accum,kwargs=False):

    # print(f'computing slice for {fArg}')

    lower=optimize_rec(fArg[1],accum,kwargs=kwargs)
    upper=optimize_rec(fArg[2],accum,kwargs=kwargs)

    # print(f'{lower} is lower')
    # print(f'{upper} is upper')
    # print(f'{upper is None} is upper is None')

    return Call(func=Name(id='slice',
                          ctx=Load()),
                args=[lower,upper,NONE_NODE],
                keywords=[])


#########
# INDEX #
#########

# Don't quite understand what this is - Index should be (fArg1,[fArg2]) 
# or (index,[fArg])
'''
def is_index(fArg):

    return pyp.is_index(fArg) \
        or (is_tuple(fArg) \
        and len(fArg) == 3 \
        and has_getitem(fArg))
'''

def index_val_node(val,kwargs=False):

    if isinstance(val,int):

        val=Num(n=val)

    if isinstance(val,str):

        val=Str(s=val)

    '''
    if is_ast_name(val):

        val=val
    '''

    return val

    '''
    return Subscript(value=chain_indices(indexedObject,indices[1:]),
                     slice=Index(value=val),
                     ctx=Load())
    '''


def index_node(fArgs,
               accum=ACCUM_LOAD,
               getFunc=get_call_or_false,
               kwargs=False):

    # print('='*30)
    # print('index_node')
    # print(f'computing index node {fArgs}')
    
    indexedObject=fArgs[0] 
    indices=[f[0] for f in fArgs[1:]]

    if is_callable(fArgs[0]) and fArgs[0] == getitem:
        
        indexedObject=fArgs[1]
        indices=fArgs[2:]
    
    # print(f'{indexedObject} is indexedObject')
    # print(f'{dump(accum)} is accum')
    
    optimizedIndexedObject=optimize_rec(indexedObject,
                                        accum,
                                        kwargs=kwargs) # Should just be a mirror
    optimizedIndices=[optimize_rec(i,
                                   accum,
                                   kwargs=kwargs) \
                      if is_f_arg_for_node(i) \
                      else i for i in indices]
    optimizedIndicesNodes=[index_val_node(index) \
                           for index in optimizedIndices]
    
    # print('callable_node_with_args')
    # print(f'{[dump(n) for n in optimizedIndicesNodes]} is optimizedIndicesNodes')
    # print(f'{dump(optimizedIndexedObject)} is optimizedIndexedObject')

    nodes=[optimizedIndexedObject]+optimizedIndicesNodes

    return callable_node_with_args(getFunc,
                                   nodes,
                                   kwargs=kwargs)


def lambda_index_node(fArgs,accum=ACCUM_LOAD,kwargs=False):

    return index_node(fArgs,accum,get_or_false,kwargs=kwargs)

    
##########
# LAMBDA #
##########

import ast


def lambda_node(fArgs,accum=ACCUM_LOAD,kwargs=False):
    # First element of lambda must be callable.  Replace with real fArg when you can.
    # print('*'*30)
    # print('lambda_node')
    # print(f'{fArgs} is fArgs')
    # print(f'{ast.dump(accum)} is accum')

    callableFArg=optimize_rec(fArgs[0],
                              accumNode=accum,
                              optimizePairs=LAMBDA_OPTIMIZE_PAIRS,
                              kwargs=kwargs)

    # This has just an "accum" as an args list.  So we need to see if there are
    # other args.

    optimizedLambdaArgs=[optimize_rec(fArg,
                                      accum,
                                      kwargs=kwargs) \
                         for fArg in fArgs[1:]]


    return callable_node_with_args(callableFArg,
                                   optimizedLambdaArgs,
                                   kwargs=kwargs)


##############################
# HELPERS FOR MAP AND FILTER #
##############################


def dict_comp(accum,
              mapValue,
              ifsList=[],
              loadedDictKey=LOADED_DICT_KEY,
              storedDictKey=STORED_DICT_KEY,
              storedDictValue=STORED_DICT_VALUE,
              kwargs=False,
             ):

    if not is_list(ifsList):

        ifsList=[ifsList]

    return DictComp(key=loadedDictKey,
                    value=mapValue,
                    generators=[
                        comprehension(target=Tuple(elts=[storedDictKey,
                                                         storedDictValue],
                                                   ctx=Store()),
                                      iter=Call(func=Attribute(value=accum,
                                                               attr='items',
                                                               ctx=Load()),
                                                args=[],
                                                keywords=[]),
                                      is_async=False,
                                      ifs=ifsList)])



def list_comp( accum,
               loadedListElement,
               storedListElement,
               ifsList=[],
               kwargs=False
             ):

    if not is_list(ifsList):

        ifsList=[ifsList]

    return ListComp(elt=loadedListElement,
                    generators=[comprehension(target=storedListElement,
                                              iter=accum,
                                              is_async=False,
                                              ifs=ifsList)])


#######
# MAP #
#######

def map_list_node(fArg,
                  accum=ACCUM_LOAD,
                  loadedListElement=LOADED_LIST_ELEMENT,
                  storedListElement=STORED_LIST_ELEMENT,
                  kwargs=False):

    #print('is map_list_node')

    if len(fArg) > 1:

        raise Exception(f'Multiple fArgs in maps deprecated.'
                        'Use separate maps instead, like [add1],[add2] ...')

    mapFArg=fArg[0]

    mapNode=optimize_rec(mapFArg,loadedListElement,kwargs=kwargs)
    lsComp=list_comp(accum,mapNode,storedListElement)

    #print(f'{mapNode} is mapNode')
    #print(f'{ast.dump(lsComp)} is lsComp')
    
    return lsComp


def map_dict_node(fArg,
                  accum=ACCUM_LOAD,
                  loadedDictValue=LOADED_DICT_VALUE,
                  kwargs=False):

    if len(fArg) > 1:

        raise Exception(f'Multiple fArgs in maps deprecated.'  
                        'Use separate maps instead.')

    mapFArg=fArg[0]
    mapValue=optimize_rec(mapFArg,loadedDictValue,kwargs=kwargs)

    return dict_comp(accum,mapValue)



def if_list_or_dict(accum,fArg,dict_func,list_func,kwargs=False):


    return IfExp(test=Call(func=IS_DICT_NODE,
                           args=[accum],
                           keywords=[]),
                 body=dict_func(fArg,accum,kwargs=kwargs),
                 orelse=list_func(fArg,accum,kwargs=kwargs))
           

def map_dict_or_list_node(fArg,accum=ACCUM_LOAD,kwargs=False):

    if len(fArg) > 1:

        raise Exception(f'Multiple fArgs in maps deprecated.'  
                        'Use separate maps instead.')
    
    return if_list_or_dict(accum,
                           fArg,
                           map_dict_node,
                           map_list_node,
                           kwargs=kwargs,
                          )


###############
# REDUCE NODE #
###############

def reduce_node(fArgs,accumNode=ACCUM_LOAD,kwargs=False):
    
    callableNode=optimize_rec(fArgs[0][0],
                              optimizePairs=LAMBDA_OPTIMIZE_PAIRS,
                              kwargs=kwargs,
                             )

    if len(fArgs) == 2:

        iterableNode=optimize_rec(fArgs[1],accumNode,kwargs=kwargs)

        return callable_node_with_args(reduce_func,
                                       [callableNode,iterableNode],
                                       kwargs=kwargs,
                                      )

    if len(fArgs) == 3:

        startValNode=optimize_rec(fArgs[1],accumNode,kwargs=kwargs)
        iterableNode=optimize_rec(fArgs[2],accumNode,kwargs=kwargs)
        nodes=[callableNode,startValNode,iterableNode]

        return callable_node_with_args(reduce_func_start_val,
                                       nodes)

    else:

        raise Exception(f'Badly formed reduce fArg {fArg}')

    nodes=[callableNode,startValNode,iterableNode]

    return callable_node_with_args(reduce_func,
                                   nodes,
                                   kwargs=kwargs)


##########
# FILTER #
##########

def any_node(nodes,kwargs=False):

    if len(nodes) < 2:

        return nodes

    return BoolOp(op=Or(),
                  values=nodes)


def filter_list_node(fArgs,
                     accum=ACCUM_LOAD,
                     loadedListElement=LOADED_LIST_ELEMENT,
                     storedListElement=STORED_LIST_ELEMENT,
                     kwargs=False):

    
    ifAnyNode=any_node([optimize_rec(fArg,
                                     loadedListElement,
                                     kwargs=kwargs) \
                        for fArg in fArgs])

    #print('printing and filter list node')
    #print(ifAllNode)

    listComp=list_comp(accum,
                       loadedListElement,
                       storedListElement,
                       ifAnyNode)

    return listComp


def filter_dict_node(fArgs,
                     accum=ACCUM_LOAD,
                     loadedDictValue=LOADED_DICT_VALUE,
                     kwargs=False):

    # print('filter_dict_node')
    # print(f'{fArgs} is fArgs')

    #print('&'*30)
    #print(f'{ast.dump(accum)} is accum')
    ifAnyNode=any_node([optimize_rec(fArg,
                                     loadedDictValue,
                                     kwargs=kwargs) \
                        for fArg in fArgs])
    #dc=dict_comp(accum,loadedDictValue,ifAnyNode)
    #print(f'{ast.dump(dc)} is accum')

    return dict_comp(accum,loadedDictValue,ifAnyNode)
    

def filter_list_or_dict_node(fArg,accum=ACCUM_LOAD,kwargs=False):

    # print('='*30)
    # print('or_filter_list_or_dict_node')
    # print(f'{fArg} is fArg')
    # print(f'{ast.dump(accum)} is accum')

    # print('or_filter_list_or_dict_node')
    # print(f'{fArg} is fArg')
    # print(f'{accum} is accum')

    return if_list_or_dict(accum,
                           fArg,
                           filter_dict_node,
                           filter_list_node,
                           kwargs=kwargs)


###############
# SWITCH_DICT #
###############

def chain_if_else(switchDictList,elseFArg,kwargs=False):
    # Using tail recursion here.
    if not switchDictList:

        return elseFArg

    condition,statement=switchDictList[0]

    return IfExp(test=condition,
                 body=statement,
                 orelse=chain_if_else(switchDictList[1:],elseFArg))
    

def switch_dict_node(fArg,accum=ACCUM_LOAD,kwargs=False):
    # For now, equality checking in switch dict will not be used.  Too inconvenient to
    # parse.
    switchDictList=[(optimize_rec(k,
                                  accum,
                                  kwargs=kwargs),
                     optimize_rec(v,
                                  accum,
                                  kwargs=kwargs)) \
                    for (k,v) in fArg.items() if k != 'else']
    elseFArg=optimize_rec(fArg['else'],
                          accum,
                          kwargs=kwargs)
    
    return chain_if_else(switchDictList,elseFArg)

   

##############
# DICT ASSOC #
##############

def dict_assoc_node(fArgs,accum=ACCUM_LOAD,kwargs=False):

    #print('*'*30)
    #print('dict_assoc_node')
    #print(f'{ast.dump(accum)} is accum')
    #print(f'{fArgs} is fArgs')
    key=fArgs[1]
    fArg=fArgs[2]
    keyNode=parse_literal(key)
    optimizedFArg=optimize_rec(fArg,accum,kwargs=kwargs)

    #print(f'{key} is key')
    #print(f'{fArg} is fArg')
    #print(f'{ast.dump(optimizedFArg)} is optimizedFArg')

    if len(fArgs) == 3:
        
        return callable_node_with_args(dct_assoc,
                                       [accum,keyNode,optimizedFArg])

    return callable_node_with_args(dct_assoc,
                                   [dict_assoc_node(fArgs[2::],accum),
                                    keyNode,
                                    optimizedFArg])


##############
# DICT MERGE #
##############

def dict_merge_node(fArgs,
                    accum=ACCUM_LOAD,
                    kwargs=False,
                   ):

    fArg=fArgs[1]
    optimizedFArg=optimize_rec(fArg,accum,kwargs=kwargs)

    return callable_node_with_args(dct_merge,
                                   [accum,
                                    optimizedFArg])


##############
# DEEP MERGE #
##############

def deep_merge_node(fArgs,
                    accum=ACCUM_LOAD,
                    kwargs=False,
                   ):

    fArg=fArgs[1]
    optimizedFArg=optimize_rec(fArg,accum)

    return callable_node_with_args(dct_merge_deep,
                                   [accum,
                                    optimizedFArg])



##########################
# HELPERS FOR LIST FARGS #
##########################

def get_nodes_for_list_f_arg(node):

    if isinstance(node,List):

        return node.elts[1:]

    elif isinstance(node,Call):

        return node.args

    else:

        raise Exception(f'unacceptable node type {node} for dict dissoc')


def build_list_f_arg(fArgs,node,f,kwargs=False):

    fArgs=fArgs[1:]
    nodes=get_nodes_for_list_f_arg(node)
    nameReplacedFArgs=[replace_with_name_node_rec(fArg,n)\
                       for (fArg,n) in zip(fArgs,nodes)]

    return f(*nameReplacedFArgs)


###############
# DICT DISSOC #
###############
   
def dict_dissoc_node(fArgs,accum=ACCUM_LOAD,kwargs=False):

    key=fArgs[-1]
    keyNode=parse_literal(key)

    if len(fArgs) == 2:

        return callable_node_with_args(dct_dissoc,[accum,keyNode])

    return callable_node_with_args(dct_dissoc,
                                   [dict_dissoc_node(fArgs[:-1],accum),
                                    keyNode])
    

##############
# LIST BUILD #
##############

def list_build_node(fArgs,accum=ACCUM_LOAD,kwargs=False):

    fArgs=fArgs[1:]
    optimizedFArgs=[optimize_rec(fArg,accum) for fArg in fArgs]
    
    return List(elts=optimizedFArgs,
                ctx=Load())


###############
# LIST APPEND #
###############

def list_append_node(fArgs,accum=ACCUM_LOAD,kwargs=False):

    fArgs=fArgs[1:]
    optimizedFArgs=[optimize_rec(fArg,accum) for fArg in fArgs]
    
    return callable_node_with_args(ls_append,
                                   [accum]+optimizedFArgs)


###############
# LIST CONCAT #
###############

def list_concat_node(fArgs,accum=ACCUM_LOAD,kwargs=False):

    fArgs=fArgs[1:]
    optimizedFArgs=[optimize_rec(fArg,accum,kwargs=kwargs) \
                    for fArg in fArgs]
    
    return callable_node_with_args(ls_extend,
                                   optimizedFArgs)
    

##############
# DICT BUILD #
##############

def dict_build_node(fArg,accum=ACCUM_LOAD,kwargs=False):

    #print('*'*30)
    #print('dict_build_node')
    #print(f'{fArg} is fArg')

    if is_explicit_dict_build(fArg):

        #print('is_explicit_dict_build')

        if len(fArg) >= 3:

            keys=fArg[1::2]
            vals=fArg[2::2]

        else:

            # This is for db('key')

            keys=[optimize_rec(fArg[1],accum,kwargs=kwargs)]
            vals=[accum]
            
            return Dict(keys=keys,values=vals,ctx=Load())
            
    else:

        keys=fArg.keys()
        vals=fArg.values()

    keys=[optimize_rec(k,accum,kwargs=kwargs) for k in keys]
    vals=[optimize_rec(v,accum,kwargs=kwargs) for v in vals]

    #print(f'{[ast.dump(n) for n in keys]} is keys')
    #print(f'{[ast.dump(n) for n in keys]} is vals')

    return Dict(keys=keys,values=vals,ctx=Load())


#################
# EMBEDDED PYPE #
#################

def embedded_pype_chain(fArgs,accum,kwargs=False):

    if len(fArgs) == 1:

        return optimize_rec(fArgs[0],accum)

    return optimize_rec(fArgs[0],embedded_pype_chain(fArgs[1:],accum))

    
def embedded_pype_node(fArgs,accum=ACCUM_LOAD,kwargs=False):

    fArgs=fArgs[1:]

    fArgs.reverse()

    pypeChain=embedded_pype_chain(fArgs,accum)

    return pypeChain


######
# DO #
######

def do_lambda_node(node):

    return Lambda(args=arguments(args=[arg(arg='do_lambda_arg', annotation=None)], 
                                 vararg=None,
                                 kwonlyargs=[], 
                                 kw_defaults=[], 
                                 kwarg=None, 
                                 defaults=[]),
                  body=node)



def do_node(fArgs,accum=ACCUM_LOAD):

    fArg=fArgs[1]
    optimizedNode=optimize_rec(fArg,DO_LAMBDA_ARG)
    lambdaNode=do_lambda_node(optimizedNode)
    callNode=callable_node_with_args(do_func,
                                     [accum,
                                      lambdaNode])

    #print(f'{callNode} is callNode')

    return callNode
      

def ast_name_node(fArg,accumNode,kwargs=False):

    bookmarkName=fArg.name

    return Name(id=bookmarkName,ctx=Load())


#########
# QUOTE #
#########

def quote_node(fArg,accum=ACCUM_LOAD):
    # print('*'*30)
    # print('quote_node')
    # print(f'{fArg} is fArg')

    fArg=fArg.quote_val()
    
    # print(f'{fArg} is fArg')

    node=optimize_rec(fArg,ACCUM_LOAD)

    # print(f'{dump(node)} is node')

    return node


################
# CLOSURE NODE #
################

def embedded_closure_chain(fArgs,accum,kwargs=False):

    if len(fArgs) == 1:

        return optimize_rec(fArgs[0],accum)

    return optimize_rec(fArgs[0],embedded_closure_chain(fArgs[1:],accum))


def closure_lambda_node(node,lambdaArgs,kwarg=None):

    return Lambda(args=arguments(args=lambdaArgs, 
                                       vararg=None, 
                                       posonlyargs=[],
                                       kwonlyargs=[], 
                                       kw_defaults=[], 
                                       kwarg=kwarg, 
                                       defaults=[]),
                  body=node)


def closure_node(fArg,
                 accum=ACCUM_LOAD,
                 closureAccum=CLOSURE_LAMBDA_ARG,
                 kwargs=False):

    # print('*'*30)
    # print('closure node')
    # print(ast.dump(accum))

    fArgs=fArg[1:]
    lambdaArgs=[arg(arg='closure_lambda_arg', annotation=None)]
    
    # This is for when there is a list of arguments.
    if is_list(fArgs[0]) and len(fArgs[0]) > 1:

        # print('is closure node')
        # print(f'{fArgs[0]}') 

        lambdaArgNodes=[optimize_rec(fArg,accum) for fArg in fArgs[0]]
        # accum=lambdaArgNodes[0] 
  
        if any([not isinstance(fArg,Name) for fArg in lambdaArgNodes]):

            raise Exception(f'Lambda args {[ast.dump(ag) for ag in lambdaArgNodes]} contains a non-name node')

        # print(f'{[ast.dump(lambdaArg) for lambdaArg in lambdaArgs]}')

        lambdaArgNames=[lambdaArg.id for lambdaArg in lambdaArgNodes]
        lambdaArgs=[arg(arg=lambdaArgName,annotation=None)\
                    for lambdaArgName in lambdaArgNames]

        # print(f'{[ast.dump(a) for a in lambdaArgs]}')

        fArgs=fArgs[1:]

    else:

        accum=closureAccum

    fArgs.reverse()

    # print(fArgs)

    # closureChain=embedded_closure_chain(fArgs,CLOSURE_LAMBDA_ARG)
    closureChain=embedded_closure_chain(fArgs,accum)

    return closure_lambda_node(closureChain,lambdaArgs)


##########
# RETURN #
##########

def pype_return_node(fArgs,accum=ACCUM_LOAD,kwargs=False):

    fArgs=fArgs[1:]
    optimizedFArgs=[optimize_rec(fArg,accum) for fArg in fArgs]
    returnNode=[Return(value=optimizedFArgs[0])]

    return returnNode


##########
# ASSIGN #
##########

def assign_node(fArg,accum=ACCUM_LOAD,kwargs=False):

    assignTo=fArg.assignTo
    assignFrom=fArg.assignFrom
    assignToNode=optimize_rec(assignTo,accum,kwargs=kwargs)
    assignToNode.ctx=Store()
    assignFromNode=optimize_rec(fArg.assignFrom,accum,kwargs=kwargs)

    return Assign(targets=[assignToNode], value=assignFromNode)


##########
# KWARGS #
##########

def kwargs_node(fArg,accum=ACCUM_LOAD,kwargs=False):
 
    # print('found fArg')
    # print(fArg)
    # print('is fArg node')

    exp=optimize_rec(fArg.exp,accum,kwargs=True)

    return exp

    
############
# LITERALS #
############

def parse_literal(fArg):
    
    if fArg is None:

        return NONE_NODE

    if isinstance(fArg,bool):

        return NameConstant(value=fArg)

    if isinstance(fArg,str):

        return Str(s=fArg)

    if isinstance(fArg,int) or isinstance(fArg,float):

        return Num(n=fArg)

    if isinstance(fArg,dict):

        keyValuePairs=[(parse_literal(k),parse_literal(v)) for (k,v) in fArg.items()]
        
        return Dict( keys=[k for (k,v) in keyValuePairs],
                     values=[v for (k,v) in keyValuePairs],
                     ctx=Load())

    if isinstance(fArg,list):

        ls=List( elts=[parse_literal(el) for el in fArg],
                 ctx=Load())
        #print(dump(ls))

        return ls

    if isinstance(fArg,set):

        return Set( elts=[parse_literal(el) for el in fArg],
                    ctx=Load())

    if isinstance(fArg,NameBookmark):

        return Name(id=fArg.name,ctx=Load())

    if is_bookmark(fArg):

        return fArg

    # I have no idea why I did this.

    return Name(id=get_name(fArg),ctx=Load())


########################
# BUILDING ASSIGNMENTS #
########################

def assign_node_to_accum(node,accum=ACCUM_STORE):

    return Assign(targets=[accum],value=node)


#######################
# OPTIMIZER FUNCTIONS #
#######################

SHARED_PAIRS=[(is_lambda,lambda_node),
              (is_slice,slice_node),
              (is_mirror,mirror_node),
              (is_map,map_dict_or_list_node),
              (is_kwargs,kwargs_node),
              (is_bookmark,ast_name_node),
              (is_filter,filter_list_or_dict_node),
              (is_switch_dict,switch_dict_node),
              (is_dict_assoc,dict_assoc_node),
              (is_dict_dissoc,dict_dissoc_node),
              (is_dict_merge,dict_merge_node),
              (is_dict_build,dict_build_node),
              (is_embedded_pype,embedded_pype_node),
              (is_list_build,list_build_node),
              (is_list_append,list_append_node),
              (is_list_concat,list_concat_node),
              (is_do,do_node),
              (is_reduce,reduce_node),
              (is_quote,quote_node),
              (is_closure,closure_node),
              (is_pype_return,pype_return_node),
              (is_assign,assign_node),
              (is_deep_merge,deep_merge_node),
             ]
OPTIMIZE_PAIRS=[(is_bookmark,ast_name_node),
                (is_callable,callable_node),
                (is_index,index_node)]+SHARED_PAIRS
# ITERABLE_PAIRS=[(is_bookmark,call_name_node),
                # (is_callable,callable_node),
                # (is_index,index_node)]+SHARED_PAIRS
LAMBDA_OPTIMIZE_PAIRS=[(is_bookmark,ast_name_node),
                       (is_callable,function_node),
                       (is_index,lambda_index_node),
                      ]+SHARED_PAIRS


def optimize_rec(fArg,
                 accumNode=ACCUM_LOAD,
                 optimizePairs=OPTIMIZE_PAIRS,
                 embeddingNodes=[],
                 kwargs=False,
                 ):

    #print('>'*30)
    #print('optimize_rec')
    #print(f'{fArg} is fArg')

    fArg=delam(fArg)
    optimizers=[opt_f for (evl_f,opt_f) in optimizePairs if evl_f(fArg)]
    evalType=type(fArg)# if evalType is None else evalType

    if not optimizers:

        return parse_literal(fArg)

    #print(f'{optimizers} is optimizers')

    optimizer=optimizers[-1]
    
    #print(f'{optimizer} is optimizer')

    # TODO - either get rid of this or implement it properly
    if is_dict(optimizer):

        #print(f'optimizer is dict')
        #print(f'{evalType} is evalType')

        if evalType in optimizer:

            #print(f'{optimizers} is optimizers')
            #print(f'{evalType} is evalType')
            #print(f'{optimizer} is optimizer')

            optimizer=optimizer[evalType]

        else:

            optimizer=optimizer['default']

    node=optimizer(fArg,accumNode,kwargs=kwargs)

    for embedding_node_func in embeddingNodes:

        node=embedding_node_func(node,fArg)

    return node


def optimize_f_args(fArgs,startNode,embeddingNodes):

    # print('*'*30)
    # print('optimize_f_args')
    # print(f'{ast.dump(startNode)} is startNode')

    assignList=[assign_node_to_accum(startNode)]

    for fArg in fArgs:
 
        opt=optimize_rec(fArg,ACCUM_LOAD,OPTIMIZE_PAIRS,embeddingNodes)
        
        if isinstance(opt,Assign):

            assignList.append(opt)

        elif is_list(opt):

            assignList.extend(opt)

        else:

            assignNode=assign_node_to_accum(opt)
 
            assignList.append(assignNode)

    #print('*'*30)
    #print('optimize_f_args')
    #print(f'{fArgs} is fArgs')
    #print([dump(a) for a in assignList])

    return assignList
