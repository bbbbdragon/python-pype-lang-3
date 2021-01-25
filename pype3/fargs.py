from pype3.helpers import *
from pype3.type_checking import *
from pype3.vals import * #Quote,LamTup,PypeVal,Getter,delam
from operator import *
import numpy as np
import sys
import pprint as pp
import types
from pype3.vals import NameBookmark,VarAssign,KwargsBookmark

#############
# CONSTANTS #
#############

PY_SLICE=slice
MIRROR=Getter('_pype_mirror_')
_=MIRROR
__=MIRROR
MIRROR_SET=set([MIRROR])
_0,_1,_2,_3,_4,_5,_6,_7,_8,_9,_10=[LamTup((_,(i,))) for i in range(11)]
_last=(_,(-1,))

INDEX_ARG_DICT={}
_i=Getter('_i_index_')
_j=Getter('_j_index_')
_k=Getter('_k_index_')
_l=Getter('_l_index_')
FOR_ARG_DICT={k:i for (i,k) in enumerate([_i,_j,_k,_l])}
ALL_GETTER_IDS=set(['_',
                    '__',
                    '_0',
                    '_1',
                    '_2',
                    '_3',
                    '_last',
                    '_i',
                    '_j',
                    '_k',
                    '_l'])
ARGS='pype_args'
embedded_pype='embedded_pype'

# IN CASE YOU THINK THE ABOVE IS MESSY

build_dict='BUILD_DICT'
assoc='DICT_ASSOC'
merge='DICT_MERGE'
dissoc='DICT_DISSOC'
build_list='BUILD_LS'
append='LIST_APPEND'
concat='LIST_CONCAT'
while_loop='WHILE_LOOP'
closure='PYPE_CLOSURE'
deep_merge='DEEP_MERGE'
kwargs='PYPE_KWARGS'
do='FARG_DO'
LIST_ARGS=set([embedded_pype,
               build_dict,
               assoc,
               merge,
               dissoc,
               l,
               append,
               concat,
               while_loop,
               do])


##########
# MIRROR #
##########

def is_mirror(fArg):

    return is_getter(fArg) and fArg in MIRROR_SET


#########
# INDEX #
#########

def is_getitem(el):

    return is_tuple(el) \
        and len(el) == 1


def is_index(fArg):
    # print('is_index')
    # print(f'{fArg} is fArg')
    # print(f'{is_tuple(fArg) and len(fArg) == 2 and is_getitem(fArg[1])}')

    return is_tuple(fArg) \
        and len(fArg) == 2 \
        and is_getitem(fArg[1])


############
# CALLABLE #
############

'''
def is_callable(fArg):

    return callable(fArg)
'''

###########
# STARRED #
###########

KWARGS=set([kwargs])

def is_kwargs(fArg):

    return is_list(fArg) \
        and len(fArg) > 0 \
        and fArg[0] in KWARGS

#######
# MAP #
#######

def is_map(fArg):

    return is_list(fArg) \
        and len(fArg) > 0 
        # and all([is_f_arg(f) for f in fArg])


##########
# REDUCE #
##########

def is_reduce(fArg):

    '''
    print('*'*30)
    print('is_reduce')
    print('{} is fArg'.format(fArg))
    print('is list fArg {}'.format(is_list(fArg)))
    print('len {}'.format(len(fArg) == 1 or len(fArg) == 2))
    print('is tuple {}'.format(is_tuple(fArg[0])))
    print('len fArg {}'.format(len(fArg[0]) == 1))
    print('is_f_arg {}'.format(is_f_arg(fArg[0][0])))
    '''

    return is_list(fArg) \
        and (len(fArg) >= 1 and len(fArg) <= 3) \
        and is_tuple(fArg[0]) \
        and len(fArg[0]) == 1 
        # and is_f_arg(fArg[0][0]) 


###############
# SWITCH DICT #
###############

def is_switch_dict(fArg):

    return is_dict(fArg) and 'else' in fArg


##########
# LAMBDA #
##########


def is_lambda(fArg):

    return is_tuple(fArg) \
        and len(fArg) > 1 \
        and not is_getitem(fArg[1]) \
        and (is_f_arg(fArg[0]) or isinstance(fArg[0],NameBookmark))


##########
# FILTER #
##########

def is_filter(fArg):

    #print('*'*30)
    #print('is_or_filter')
    #print(f'{fArg} is fArg')
    #print(f'{not is_set(fArg)} is not is_set(fArg)')

    # We had to pimp up this function when getting rid of the AND filter. 
    # First, we want to see if it's a singleton set.

    if not is_set(fArg):

        return False

    if len(fArg) == 0:

        return False

    return True
    '''
    # Then, we get the first element of the set ...

    el=next(iter(fArg))

    # print(f'{el} is el')

    # Is it an fArg or a LamTup?
 
    #print(f'{is_f_arg(el)} is is_f_arg(el)')
    #print(f'{ is_lam_tup(el)} is is_lam_tup(el)')

    return is_f_arg(el) \
        or is_bookmark(el) \
        or is_lam_tup(el)
    '''

##############
# DICT BUILD #
##############

DICT_BUILD_ARGS=set([build_dict])

def is_explicit_dict_build(fArg):

    return is_list(fArg) and len(fArg) >= 2 \
        and is_string(fArg[0]) and fArg[0] in DICT_BUILD_ARGS

    '''
    return is_list(fArg) and len(fArg) == 2 \
        and is_string(fArg[0]) and fArg[0] in DICT_BUILD_ARGS \
        and is_dict(fArg[1])
    '''

DICT_FARGS_LIMIT=10

valid_values=lambda ls: any([is_f_arg(el) or is_lam_tup(el) for el in ls])

def dict_values_farg(dct):

    values=list(dct.values())[:DICT_FARGS_LIMIT]

    if valid_values(values):

        return True

    keys=list(dct.keys())[:DICT_FARGS_LIMIT]
    
    if valid_values(keys):

        return True

    return False


def is_implicit_dict_build(fArg):

    return is_dict(fArg) and not 'else' in fArg and dict_values_farg(fArg)


def is_dict_build(fArg):

    # What about mappings??

    return (is_dict(fArg) and not 'else' in fArg and dict_values_farg(fArg)) \
        or is_explicit_dict_build(fArg)


#########
# ASSOC #
#########

DICT_ASSOC_ARGS=set([assoc])

def is_dict_assoc(fArg):

    return is_list(fArg) \
        and len(fArg) >= 3 \
        and is_string(fArg[0]) \
        and fArg[0] in DICT_ASSOC_ARGS


#########
# MERGE #
#########

DICT_MERGE_ARGS=set([merge])

def is_dict_merge(fArg):

    return is_list(fArg) \
        and len(fArg) == 2 \
        and is_string(fArg[0]) and fArg[0] in DICT_MERGE_ARGS 


##############
# MERGE DEEP #
##############

DEEP_MERGE_ARGS=set([deep_merge])

def is_deep_merge(fArg):

    return is_list(fArg) \
        and len(fArg) == 2 \
        and is_string(fArg[0]) and fArg[0] in DEEP_MERGE_ARGS
    

##########
# DISSOC #
##########

DICT_DISSOC_ARGS=set([dissoc])

def is_dict_dissoc(fArg):

    return is_list(fArg) \
        and len(fArg) > 1 \
        and is_string(fArg[0]) and fArg[0] in DICT_DISSOC_ARGS \


##############
# LIST BUILD #
##############

LIST_BUILD_ARGS=set([build_list])

def is_list_build(fArg):

    return is_list(fArg) \
        and len(fArg) > 1 \
        and is_string(fArg[0]) and fArg[0] in LIST_BUILD_ARGS


###############
# LIST APPEND #
###############

LIST_APPEND_ARGS=set([append])

def is_list_append(fArg):

    return is_list(fArg) \
        and len(fArg) > 1 \
        and is_string(fArg[0]) \
        and fArg[0] in LIST_APPEND_ARGS


###############
# LIST CONCAT #
###############

LIST_CONCAT_ARGS=set([concat])

def is_list_concat(fArg):

    return is_list(fArg) \
        and len(fArg) > 1 \
        and is_string(fArg[0]) \
        and fArg[0] in LIST_CONCAT_ARGS


#################
# EMBEDDED PYPE #
#################

PYPE_ARGS=set([embedded_pype])

def is_embedded_pype(fArg):

    #print('*'*30)
    #print('is_embedded_pype')

    return is_list(fArg) \
        and len(fArg) > 1 \
        and is_string(fArg[0]) \
        and fArg[0] in PYPE_ARGS


#########
# QUOTE #
#########

def is_quote(fArg):

    return isinstance(fArg,Quote)


######
# DO #
######

def is_do(fArg):

    return is_list(fArg) and len(fArg) > 1 and fArg[0] == do


#########
# SLICE #
#########

def is_slice(fArg):

    return is_tuple(fArg)\
        and len(fArg) == 3\
        and fArg[0] == PY_SLICE


##########
# ASSIGN #
##########

def is_assign(fArg):

    return isinstance(fArg,VarAssign)


##################
# KwargsBookmark #
##################

import ast

def is_kwargs(fArg):

    # print('*')
    # print('is_kwargs')
    # print(fArg)
    # print('is fArg')
    # print(isinstance(fArg,KwargsBookmark)) 

    return isinstance(fArg,KwargsBookmark)


###########
# CLOSURE #
###########

def is_closure(fArg):

    return is_list(fArg) \
        and len(fArg) > 1 \
        and fArg[0] == closure

    
###########
# IS FARG #
###########

FARGS=[is_mirror,
       is_index,
       is_callable,
       is_map,
       is_reduce,
       is_switch_dict,
       is_lambda,
       is_filter,
       is_dict_build,
       is_dict_assoc,
       is_dict_merge,
       is_dict_dissoc,
       is_list_build,
       is_list_append,
       is_list_concat,
       is_embedded_pype,
       is_quote,
       is_kwargs,
       is_do]


def is_f_arg(fArg,fArgList=FARGS):

    return any([f(fArg) for f in fArgList])
