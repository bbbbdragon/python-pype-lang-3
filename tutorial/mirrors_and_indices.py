'''
python3 mirrors_and_indices.py 

python3 watch_file.py -p2 python3 mirrors_and_indices.py -p1 ./reinstall_from_source.sh -d /Users/bennettbullock/python-pype-lang-3
'''
from pype3 import pypeify,pypeify_namespace,p,_,_0,_1,_2,_last
from pype3 import ep,tup,db,a,iff,d,ift,squash,ifp
from pype3.time_helpers import *
from pype3.helpers import *
from pype3.vals import PypeVal as v
from copy import deepcopy
from pype3.numpy_helpers import *
import numpy as np

'''
Basic tutorial that covers mirrors, operators on mirrors, and indices.
'''

###########
# MIRRORS #
###########

def mirror_example(n):
    '''
    Here, we show how the underscore, or 'mirror' stands in for the first
    argument of the function.
    '''
    (_,
    )


def mirror_example_2_args(n,y):
    '''
    When we want to begin the pype expression with something other than 
    the first argument of the function, we put that as the first expression.
    '''
    (y,
     _,
    )


def mirror_add_example(n):
    '''
    Here, we show how basic operators are overridden by pype.  The mirror
    overloads the '+' operator to create a 'LamTup' object, which the pype
    compiler converts into an AST.
    '''
    (_+2,
    )


def mirror_two_vars_example(n,y):
    '''
    This shows how we can reference multiple variables in different pype
    expressions.
    '''
    (n,
     _*2,
     _+y,
    )

def mirror_or_example(truthVal):
    '''
    For boolean operators, we use Python's bitwise operators, & for AND, | 
    for OR, and ~ for NOT.  Because these operators have different precendence
    than the built-in Boolean operators, you must enclose expressions in
    parehtneses.

    This implements a function truthVal OR NOT truthVal
    '''
    (_ | (~_),
    )


def mirror_and_example(truthVal):
    '''
    This implements a function truthVal AND NOT truthVal
    '''
    (_ & (~_),
    )


###########
# INDICES #
###########

def list_index(ls):
    '''
    Here, we are accessing element 2 of ls.
    '''
    (_[2],
    )


def index_arg_first(ls):
    '''
    The _0 symbol stands for the first element of the list. 
    '''
    (_0,
    )


def index_arg_add(ls):
    '''
    The _0 symbol overrides the same operators as _.
    '''
    (_0+1,
    )


def index_arg_last(ls):
    '''
    The _last symbol stands for the last element of the list.
    '''
    (_last,
    )


def embedded_list_index(ls):
    '''
    Here, we are doing multiple list indices.
    '''
    (_[0][1],
    )


def complex_list_index(ls):
    '''
    Here, we are doing multiple list indices using numpy format.
    '''
    (_[0,1],
    )


def slice_index(ls):
    '''
    Pype accomodates slicing by applying it to the mirror operator.
    '''
    (_[:1],
    )


######################
# DICTIONARY INDICES #
######################

def dict_index_brackets(js):
    '''
    Here, we access a dictionary along a path of keys.
    '''
    (_['this']['that'],
    )


def dict_index_getitem(js):
    '''
    This is an alternative way to access dictionary items that is a bit
    less cluttered.
    '''
    (_.this.that,
    )


##################
# OBJECT INDICES #
##################

def object_index_getitem(obj):
    '''
    Here, we are accessing a value of an object.
    '''
    (_.ls,
    )


def object_index_embedded_getitem(obj):
    '''
    Here, we are accessing a value of an object.
    '''
    (_.ls[1],
    )


def object_index_call(obj):
    '''
    Here, we are calling a function of the object.
    '''
    (_.get_ls_val,
    )


def object_index_embedded_call(obj):
    '''
    Here, we are calling a function of the object, and getting an element.
    '''
    (_.get_ls_val[0],
    )


pypeify_namespace(globals())

if __name__=='__main__':

     print('*'*30)
     print('mirrors')
     print('*'*30)

     print('mirror_example(1)')
     print(mirror_example(1))

     print('mirror_example_2_args(1,3)')
     print(mirror_example_2_args(1,3))

     print('mirror_add_example(1)')
     print(mirror_add_example(1))

     print('mirror_or_example(False)')
     print(mirror_or_example(False))

     print('mirror_or_example(True)')
     print(mirror_or_example(True))

     print('mirror_and_example(False)')
     print(mirror_and_example(False))

     print('mirror_and_example(True)')
     print(mirror_and_example(True))

     print('*'*30)
     print('list indices')
     print('*'*30)

     ls=[1,2,3,4,5]

     print('list_index(ls)')
     print(list_index(ls))

     print('index_arg_first(ls)')
     print(index_arg_first(ls))

     print('index_arg_last(ls)')
     print(index_arg_last(ls))

     print(f'complex_list_index(ls)')
     print(complex_list_index(ls))
     
     print('slice_index(ls)')
     print(slice_index(ls))

     ls=[[1,2,3],[2,3,4]]

     print('embedded_list_index(ls)')
     print(embedded_list_index(ls))
     
     print('*'*30)
     print('dict indices')
     print('*'*30)

     js={'this':{'that':1}}

     print('dict_index_brackets(js) with element present')
     print(dict_index_brackets(js))

     js={'this':{'notThat':1}}

     print('dict_index_brackets(js) with no element present')
     print(dict_index_brackets(js))

     js={'this':{'that':1}}

     print('dict_index_getitem(js)')
     print(dict_index_getitem(js))

     print('*'*30)
     print('object indexing')
     print('*'*30)

     class ListObject:

        def __init__(self):

            self.ls=[1,2,3,4]

        def get_ls_val(self):

            return self.ls

     obj=ListObject()

     print('object_index_getitem(obj)')
     print(object_index_getitem(obj))

     print('object_index_embedded_getitem(obj)')
     print(object_index_embedded_getitem(obj))

     print('object_index_call(obj)')
     print(object_index_call(obj))

     print('object_index_embedded_call(obj)')
     print(object_index_embedded_call(obj))


