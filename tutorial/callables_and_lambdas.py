'''
python3 callables_and_lambdas.py 

python3 watch_file.py -p2 python3 callables_and_lambdas.py -p1 ./reinstall_from_source.sh -d /Users/bennettbullock/python-pype-lang-3
'''
from pype3 import pypeify,pypeify_namespace,p,_,_0,_1,_2,_last
from pype3 import ep,db,a,iff,d,ift,squash,ifp
# import sys 
# import json
from pype3.time_helpers import *
from pype3.helpers import *
from pype3.vals import PypeVal as v
from copy import deepcopy
from pype3.numpy_helpers import *

'''
Basic tutorial that covers callables and lambdas.
'''

############
# CALLABLE #
############

def mult2(n):

    (_*2, # n*2
    )


def add1(n):

    (_+1, # n+1
    )


def callable_example_1(n):

    (add1, # add1(n)
    )


def callable_example_2(n):
    '''
    This will take a series of functions and run them iteratively on the
    first argument.
    '''
    (add1, # add1(n)
     add1, # add1(add1(n))
     mult2, # mult2(add1(add1(n)))
    )


############
# CALLABLE #
############

def add(x,y):

    (_+y, # x+y
    )


def lambda_example_1(n):
    '''
    A lambda is defined as (callableFArg,fArg1,fArg2,...).

    The difference between a lambda and a callable is that a callable takes
    only one argument.  A lambda can take multiple arguments.  

    Remember, when a mirror appears as the first element of a pype expression,
    it refers to the *first argument* of the function, in this case 'n'.

    This function is equivalent to callable_example_1.
    '''
    ((add1,_), # add1(n)
    )


def lambda_example_2(n):
    '''
    Here, we show how a lambda accepts multiple arguments.
    '''
    ((add,_,3), # add(n,3)
    )


def lambda_example_3(n):
    '''
    This example shows us how to dynamically define fArg arguments of a 
    lambda.  Notice the second expression is an exponentiation - n**3.
    '''
    ((add,_,_**3), # add(n,n**3)
    )


def lambda_example_4(js,y):
    '''
    The callableFArg in a lambda can also be an fArg, so long as the evaluated
    result is a callable.  
    '''
    ((_.add,y,y**3), # js['add'](y,y**3)
    )


pypeify_namespace(globals())

if __name__=='__main__':

    print('*'*30)
    print('callables')
    print('*'*30)

    print('callable_example_1(1)')
    print(callable_example_1(1))

    print('callable_example_2(1)')
    print(callable_example_2(1))

    print('*'*30)
    print('lambdas')
    print('*'*30)

    print('lambda_example_1(1)')
    print(lambda_example_1(1))

    print('lambda_example_2(1)')
    print(lambda_example_2(1))

    print('lambda_example_3(3)')
    print(lambda_example_3(3))

    js={'add':add}

    print('lambda_example_4(js,3)')
    print(lambda_example_4(js,3))
    
