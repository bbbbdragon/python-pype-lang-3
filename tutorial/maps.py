'''
python3 functional.py 

python3 watch_file.py -p2 python3 maps.py -p1 ./reinstall_from_source.sh -d /Users/bennettbullock/python-pype-lang-3
'''
from pype3 import pypeify,pypeify_namespace,p,_,_0,_1,_2,_last
from pype3 import ep,db,a,iff,d,ift,squash,ifp
from pype3.time_helpers import *
from pype3.helpers import *
from pype3.vals import PypeVal as v
from copy import deepcopy
from pype3.numpy_helpers import *

'''
Basic tutorial that covers maps.
'''

def add1(n):

    (_+1,
    )


def add(x,y):

    (_+y, # x+y
    )


def add2(n):

    (_+2,
    )


def mult100(n):

    (_*100,
    )


########
# MAPS #
########

def map_add_1(obj):
    '''
    The square brackets enclose an fArg, in this case the function add1.
    When the accum (obj) is a list, we apply the fArg to every element.  
    When it is a dict, we apply the fArg to every value.
    '''
    ([add1],
    )


def map_add_2(ls,y):
    '''
    Here, the fArg is a lambda, which we apply to every element of obj.
    '''
    ([(add,_,y)],
    )


#################
# EMBEDDED MAPS #
#################

'''
The following two functions run embedded loops on obj.
'''

def embedded_map_add_1(obj):

    ([[add1]],
    )


def embedded_map_add_2(obj,y):

    ([[(add,_,y)]],
    )
    

###########################
# MAPS FOR FUNCTION CALLS #
###########################

def function_map(functions,n):
    '''
    This function shows that we can map through lists of functions or dicts
    with funcitons as values, and apply these functions to another element.

    We do this by building a lambda with a mirror as its first element.
    '''
    ([(_,n)],
    )


pypeify_namespace(globals())

if __name__=='__main__':

    print('*'*30)
    print('list maps')
    print('*'*30)

    ls=[2,3,5,1,1,2,3,4]

    print('-'*30)
    print(f'{ls} is ls')
    print('-'*30)
     
    print('map_add_1(ls)')
    print(map_add_1(ls))

    print('map_add_2(ls,2)')
    print(map_add_2(ls,2))

    print('*'*30)
    print('dict maps')
    print('*'*30)

    dct={'a':2,'b':3,'c':5,'d':1,'e':1,'f':2}

    print('-'*30)
    print(f'{dct} is dct')
    print('-'*30)
     
    print('map_add_1(dct)')
    print(map_add_1(dct))

    print('map_add_2(dct,2)')
    print(map_add_2(dct,2))

    print('*'*30)
    print('embedded maps')
    print('*'*30)

    obj=[[0,1,2,4],[2,3,4,5]]

    print('-'*30)
    print(f'{obj} is obj')
    print('-'*30)

    print('embedded_map_add_1(obj)')
    print(embedded_map_add_1(obj))

    print('embedded_map_add_2(obj,2)')
    print(embedded_map_add_2(obj,2))
    
    obj=[[0,1,2,4],[2,3,4,5]]

    print('-'*30)
    print(f'{obj} is obj')
    print('-'*30)

    print('embedded_map_add_1(obj)')
    print(embedded_map_add_1(obj))

    print('embedded_map_add_2(obj,2)')
    print(embedded_map_add_2(obj,2))

    obj={'a':{'b':2,'c':3,'e':4},'f':{'g':20,'h':30,'i':40}}

    print('-'*30)
    print(f'{obj} is obj')
    print('-'*30)

    print('embedded_map_add_1(obj)')
    print(embedded_map_add_1(obj))

    print('embedded_map_add_2(obj,2)')
    print(embedded_map_add_2(obj,2))

    obj=[{'b':2,'c':3,'e':4},{'g':20,'h':30,'i':40}]

    print('-'*30)
    print(f'{obj} is obj')
    print('-'*30)

    print('embedded_map_add_1(obj)')
    print(embedded_map_add_1(obj))

    print('embedded_map_add_2(obj,2)')
    print(embedded_map_add_2(obj,2))
    
    obj={'a':[2,3,4],'b':[20,30,40]}

    print('-'*30)
    print(f'{obj} is obj')
    print('-'*30)

    print('embedded_map_add_1(obj)')
    print(embedded_map_add_1(obj))

    print('embedded_map_add_2(obj,2)')
    print(embedded_map_add_2(obj,2))

    print('*'*30)
    print('function maps')
    print('*'*30)

    functions=[add1,add2,mult100]

    print('-'*30)
    print(f'{functions} is functions')
    print('-'*30)

    print('function_map(functions,5)')
    print(function_map(functions,5))

    functions={'add1':add1,'add2':add2,'mult100':mult100}

    print('-'*30)
    print(f'{functions} is functions')
    print('-'*30)

    print('function_map(functions,5)')
    print(function_map(functions,5))
