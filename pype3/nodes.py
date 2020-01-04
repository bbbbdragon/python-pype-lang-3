from pype3.fargs import *
from pype3.build_helpers import *
from pype3.vals import LamTup,delam,is_bookmark,NameBookmark
from pype3.fargs import INDEX_ARG_DICT
from pype3.vals import LamTup
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
from operator import getitem

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

def pype_call_node(args,**params):

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


def keystep_node(tree,fArg,params):

    try:

        treePrintout=astpretty.pformat(tree)

    except Exception as e:

        treePrintout=ast.dump(tree)

    fArgString=pp.pformat(fArg)

    return Call(func=PRINT_AND_EVAL_NODE,
                args=[tree,Str(s=treePrintout),Str(s=fArgString)], 
                keywords=[])


##########
# MIRROR #
##########

def mirror_node(fArgs,val,params):
    
    # print('mirror_node')
    # print(f'{fArgs} is fArgs')
    # print(f'{accum} is accum')

    return params['accum']


############
# CALLABLE #
############

# helpers 

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


# helper nodes

def function_node(fArg,params,val):

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


def callable_node_with_args(fArg,callableArgs,params):

    #print('='*30)
    #print('callable node with args')
    #print(f'{fArg} is fArg')
    #print(f'{[dump(n) for n in callableArgs]} is callableArgs')

    if isinstance(fArg,Call):

        # It stops here!
        #print('is call')

        return Call(func=fArg,
                    keywords=[],
                    args=callableArgs)

    if hasattr(fArg,'__name__'):

        fArg=function_node(fArg,params)

    return Call(func=fArg,
                keywords=[],
                args=callableArgs)


# nodes                        

def callable_node(fArg,val,params):

    return callable_node_with_args(fArg,[params['accum']],params)


#########
# INDEX #
#########

# constants

DEFAULT_INDEX_PARAMS={'accum':ACCUM_LOAD,
                      'getFunc':get_call_or_false}

# helpers

def is_soft_indexable(fArgs,params):

    print('*'*30)
    print('is_soft_indexable')
    print(f'{fArgs} is fArgs')
    print(f'{params} is params')

    if 'startVal' in params \
       and params['startVal'] is not None:

        obj=params['startVal']
        index=fArgs[1][0]

        if is_object(obj) and is_string(index):

            return True

    if is_callable(fArgs[0]) and fArgs[0] == getitem:

        return True

    return False
   
 
def has_getitem(fArgs):

    return is_callable(fArgs[0]) and fArgs[0] == getitem


# helper nodes

def index_val_node(val,params):

    if isinstance(val,int):

        val=Num(n=val)

    if isinstance(val,str):

        val=Str(s=val)

    '''
    if is_ast_name(val):

        val=val
    '''

    return val



def optimized_indices_nodes(indexedObject,indices,params):
    
    # print('*'*30)
    # print('optimized_indices_nodes')
    # print(f'{indexedObject} is indexedObject')

    optimizedIndexedObject=optimize_rec(indexedObject,params) 
    optimizedIndices=[optimize_rec(i,params) if is_f_arg_for_node(i) \
                      else i for i in indices]
    optimizedIndicesNodes=[index_val_node(index,params) \
                           for index in optimizedIndices]

    return optimizedIndexedObject,optimizedIndicesNodes


def soft_index_node(fArgs,params):

    # print('*'*30)
    # print('soft_index_node')
    # print(f'{fArgs} is fArgs')
    # print(f'{params} is params')

    params={**DEFAULT_INDEX_PARAMS,**params}
    getFunc=params['getFunc'] if 'getFunc' in params else get_call_or_false
    indexedObject=fArgs[0]
    indices=[f[0] for f in fArgs[1:]] 

    # This is for objects.

    if has_getitem(fArgs):

        indexedObject=fArgs[1]
        indices=fArgs[2:]

    optimizedIndexedObject,\
    optimizedIndicesNodes=optimized_indices_nodes(indexedObject,indices,params)

    return callable_node_with_args(getFunc,
                                   [optimizedIndexedObject]+optimizedIndicesNodes,
                                   params)



def hard_index_node(fArgs,params):

    # print('*'*30)
    # print('hard_index_node')
    # print(f'{fArgs} is fArgs')
    
    params={**DEFAULT_INDEX_PARAMS,**params}

    # Here, we cannot run hard indexing on the item, but we know it's indexible,
    # so we run soft-indexing on it.

    if is_soft_indexable(fArgs,params):

        # print('hard indexable is soft indexable')

        return soft_index_node(fArgs,params)

    indexedObject=fArgs[0]
    indices=[f[0] for f in fArgs[1:]]
    optimizedIndexedObject,\
    optimizedIndicesNodes=optimized_indices_nodes(indexedObject,indices,params)

    # print(f'{ast.dump(optimizedIndexedObject)} is optimizedIndexedObject')
    # print([ast.dump(n) for n in optimizedIndicesNodes])
    # print('is optimizedIndicesNodes')

    return Subscript(value=optimizedIndexedObject,
                     ctx=Load(),
                     slice=Index(value=optimizedIndicesNodes[0],
                                 ctx=Load()))


def index_node(fArgs,params=DEFAULT_INDEX_PARAMS):

    if 'hardIndexing' in params and params['hardIndexing']:

        return hard_index_node(fArgs,params)

    return soft_index_node(fArgs,params)


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

OPTIMIZE_PAIRS=[(is_mirror,mirror_node),
                (is_callable,callable_node),
                # (is_index,index_node),
                # (is_lambda,lambda_node),
                # (is_slice,slice_node),
                # (is_map,map_dict_or_list_node),
                # (is_bookmark,name_bookmark_node),
                # (is_filter,filter_list_or_dict_node),
                # (is_switch_dict,switch_dict_node),
                # (is_dict_assoc,dict_assoc_node),
                # (is_dict_dissoc,dict_dissoc_node),
                # (is_dict_merge,dict_merge_node),
                # (is_list_build,list_build_node),
                # (is_dict_build,dict_build_node),
                # (is_embedded_pype,embedded_pype_node),
                # (is_do,do_node),
                # (is_reduce,reduce_node),
                # (is_quote,quote_node),
               ]
'''
LAMBDA_OPTIMIZE_PAIRS=[(is_callable,function_node),
                       (is_mirror,mirror_node),
                       (is_lambda,lambda_node),
                       (is_slice,slice_node),
                       (is_index,lambda_index_node),
                       (is_map,map_dict_or_list_node),
                       (is_bookmark,name_bookmark_node),
                       (is_filter,filter_list_or_dict_node),
                       (is_switch_dict,switch_dict_node),
                       (is_dict_assoc,dict_assoc_node),
                       (is_dict_dissoc,dict_dissoc_node),
                       (is_dict_merge,dict_merge_node),
                       (is_list_build,list_build_node),
                       (is_dict_build,dict_build_node),
                       (is_embedded_pype,embedded_pype_node),
                       (is_do,do_node),
                       ]
'''

######################
# DEFAULT PARAMETERS #
######################

DEFAULT_PARAMS={'accum':ACCUM_LOAD,
                'optimizePairs':OPTIMIZE_PAIRS,
                'embeddingNodes':[]}

########################
# OPTIMIZATION HELPERS #
########################


def eval_node(node,namespace):

    localNamespace={}
    mod=Module(body=[Assign(targets=[Name(id='temporarilyEvaluatedNode', 
                                          ctx=Store())], 
                            value=node)])

    fix_missing_locations(mod)

    exec(compile(mod,
                 filename='<ast>',
                 mode='exec'),
         namespace,
         localNamespace)

    return localNamespace['temporarilyEvaluatedNode']


##########################
# OPTIMIZATION FUNCTIONS #
##########################

def optimize_rec(fArg,
                 params,
                 val=None,
                ):

    '''
    First, deepcopy params, and set default params.
    '''
    params={**DEFAULT_PARAMS,**params}

    '''
    Extract the original fArg using delam.
    '''
    fArg=delam(fArg)

    '''
    Find out the node-building function 'node_f', depending on what kind of 
    fArg structure this is, 'evl_f'.
    '''
    optimizers=[node_f for (evl_f,node_f) in params['optimizePairs'] if evl_f(fArg)]

    '''
    If no evl_f evaluates as true, then it is a literal, so return a literal
    node.
    '''
    if not optimizers:

        return parse_literal(fArg)

    '''
    Get the last node_f.  Node that this implies a precedence relationship.
    '''
    optimizer=optimizers[-1]

    '''
    Let's run the fucker!  Node is an AST node.
    '''
    node=optimizer(fArg,val,params)

    '''
    for embedding_node_func in params['embeddingNodes']:

        node=embedding_node_func(node,fArg,params)
    '''

    return node


def optimize_f_args(fArgs,params=DEFAULT_PARAMS):

    print('*'*30)
    print('optimize_f_args')

    startNode=params['startNode']
    val=None

    if 'namespace' in params:

        val=eval_node(startNode,params['namespace'])

    assignList=[assign_node_to_accum(startNode)]
    
    for fArg in fArgs:

        opt=optimize_rec(fArg,params,val)
        assignNode=assign_node_to_accum(opt)

        assignList.append(assignNode)

        if 'namespace' in params:

            val=eval_node(opt,params['namespace'])

    #print('*'*30)
    #print('optimize_f_args')
    #print(f'{fArgs} is fArgs')
    #print([dump(a) for a in assignList])

    return assignList
