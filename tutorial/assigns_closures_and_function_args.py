'''
python3 watch_file.py -p2 python3 assigns_closures_and_function_args.py -p1 ./reinstall_from_source.sh -d /Users/bennettbullock/python-pype-lang-3
'''
from pype3 import pypeify,pypeify_namespace,p,_,_0,_1,_2,ep,db,a,iff,d,ift,squash,ifp
from pype3 import cl
from pype3.time_helpers import *
from pype3.helpers import *
from pype3.vals import *
from copy import deepcopy
from pype3.numpy_helpers import *

###########
# ASSIGNS #
###########

def assign_example(n):
    '''
    This is an example of how to use assigns in pype.  We use the bitwise left-shift 
    operator to assign a value to a variable.  This variable can then be used in the
    rest of the tuple.

    The bitwise operator was included because the assignment operator = cannot compile
    into syntactic python.  

    It is important to note that an assignment does not alter the value of the accum.
    Notice here that x is assigned the accum n, y is assigned n*x, and the final 
    returned value is n*y.
    '''
    (x << _, # x=n
     y << x*_, # y=x*n
     _*y, # n*y
    )


############
# CLOSURES #
############

def add1(n):

    _+1,


def closure_example_1(n):
    '''
    Here, we deal with a simple closure.  A closure is a function defined using pype
    notation, but with the cl marker.  In this case, we assign the closure to x, and
    then call it in a lambda.  For now, standalone variables cannot be used as callables.
    They must be explicitly cast to lambdas.
    '''
    (x << cl(add1,add1),
     (x,_),
    )


def sm(a,b):

    _+b,


def closure_example_2(n):
    '''
    Here is an example of a closure with arguments.  Whereas the cl(add1,add1) takes a
    single argument, this closure can take two arguments, y and z.  You must provide a
    list with more than one element to specify the arguments of a closure.
    '''
    (x << cl([y,z],
             (sm,_,z)),
     (x,_,3),
    )
    

@pypeify(verbose=True)
def closure_example_var_def(n):

    (cl([y,z],
        (sm,_,z)),
    )


#####################################
# FUNCTIONS AS FIRST CLASS CITIZENS #
#####################################

def function_pass_example(n,func):
    '''
    For now, when you want to pass functions as arguments into a pype funciton, you
    will need to explicitly call them as a lambda.
    '''
    (_+(func,_),
    )


def add2(n):
    
    _+2,


def add3(n):

    _+3,


def function_first_class_example(funcs,n):
    '''
    This shows you how to pass functions as arguments into another function.  We 
    iterate through the funcs, and for each function, pass it into 
    function_pass_example.
    '''
    ([(function_pass_example,n,_)],
    )


pypeify_namespace(globals())

if __name__=='__main__':
    '''
    print('*'*30)
    print('assigns')
    print('*'*30)

    print('assign_example(2)')
    print(assign_example(2))

    print('*'*30)
    print('closures')
    print('*'*30)

    print('closure_example_1(2)')
    print(closure_example_1(2))

    print('closure_example_2(2)')
    print(closure_example_2(2))
    '''
    print('closure_example_var_def(2)')
    print(closure_example_var_def(2))

    
    '''
    print('*'*30)
    print('functions as first-class citizens')
    print('*'*30)
    
    print('function_pass_example(1,add1)')
    print(function_pass_example(1,add1))

    functions=[add1,add2,add3]

    print('-'*30)
    print(f'{functions} is functions')
    print('-'*30)

    print('function_first_class_example(functions,2)')
    print(function_first_class_example(functions,2))
    '''
