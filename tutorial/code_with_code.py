'''
python3 code_with_code.py 

python3 watch_file.py -p2 python3 code_with_code.py -p1 ./reinstall_from_source.sh -d /Users/bennettbullock/python-pype-lang-3
'''
from pype3 import pypeify,pypeify_namespace,p,_,_0,_1,_2,_last,cl,lm
from pype3 import ep,db,a,iff,d,ift,squash,ifp
from pype3.time_helpers import *
from pype3.helpers import *
from pype3.vals import Quote as q
from copy import deepcopy
from pype3.numpy_helpers import *
from pype3.type_checking import *

'''
Basic tutorial that covers quotes and using closures to build functions.
'''

###########
# HELPERS #
###########

def add1(n):

    _+1,


def mult2(n):

    _*2,


def add3(n):

    _+3,


def mult3(n):

    _*3,


def sm(a,b):

    _+b,


#######################
# EMBEDDING FUNCTIONS #
#######################

def embedding_function(n,f):
    '''
    This function applies a function to n*2.
    '''
    (f,_*2),


def embedding_function_closure_add1(n):
    '''
    First, we see that we can build a function on the fly using a closure,
    which just applies add1 to the argument.
    '''
    (embedding_function,_,cl(add1)),


def embedding_function_quote_add1(n):
    '''
    However, if we define a closure previously in the code, and then encase
    it in another closure, as in:

    (add << cl(_+1),
     (embedding_function,_,cl(add)),
    )

    the function will return a lambda that returns a function.  This is not
    what we want.  Therefore, we quote the function.  

    It is a strict requirement that q takes *only* names of functions, whether
    they be defined elsewhere in the code, or as a callable.
    '''
    (add << cl(_+1),
     (embedding_function,_,q(add)),
    )


########################
# FUNCTION COMPOSITION #
########################

def complex_function_composition(f1,f2,f3,f4):
    '''
    Here, we are building a function from several components.  Here is a
    thing we need to remember for now.  The compiler does not see f1 ... f4
    as functions, and therefore cannot evaluate them as such.  Therefore,
    we cannot make closures with bare function names - we have to cast them
    to lambdas.  The lm macro helps us to this - lm(f1) <=> (f1,_)

    This will be fixed in future versions, which will record which variables
    in the namespace are declared as callables.
    '''
    (f12 << cl(lm(f1),lm(f2)),
     f34 << cl(lm(f3),lm(f4)),
     cl(lm(f12) + lm(f34)),
    )


def apply_complex_function_composition(n,f1,f2,f3,f4):
    '''
    This builds a function and then applies it to n.
    '''
    ((complex_function_composition,f1,f2,f3,f4),
     (_,n),
    )


############
# CURRYING #
############

def currying(f1,a):

    (cl((f1,a,_)),
    )


def apply_currying(f1,a,b):

    ((currying,f1,a),
     (_,b),
    )


pypeify_namespace(globals())

if __name__=='__main__':

    print('*'*30)
    print('embedding functions')

    print('embedding_function_closure_add1(5)')
    print(embedding_function_closure_add1(5))

    print('embedding_function_quote_add1(5)')
    print(embedding_function_quote_add1(5))

    print('*'*30)
    print('function composition')
 
    print('complex_function_composition(add1,mult2,add3,mult3)')
    print(complex_function_composition(add1,mult2,add3,mult3))

    print('complex_function_composition(add1,mult2,add3,mult3)(0)')
    print(complex_function_composition(add1,mult2,add3,mult3)(0))

    print('apply_complex_function_composition(add1,mult2,add3,mult3)')
    print(apply_complex_function_composition(5,add1,mult2,add3,mult3))

    print('*'*30)
    print('currying')

    print('currying(sm,2)')
    print(currying(sm,2))

    print('currying(sm,2)(1)')
    print(currying(sm,2)(1))

    print('apply_currying(sm,2,1)')
    print(apply_currying(sm,2,1))
