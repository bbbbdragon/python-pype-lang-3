import pprint as pp
from functools import wraps
import astpretty
import time as tm
from pype3.type_checking import *
from ast import *
import ast

def print_obj(obj,message,verbose):
    '''
    Pretty-prints the object.
    '''
    if verbose:

        print(message)

        # We print out individual trees.
        if is_list(obj):

            for t in obj:

                print('='*30)
                
                if isinstance(t,AST):

                    print('printing fArg tree')
             
                    try:

                        astpretty.pprint(t)

                    except Exception as e:

                        print(ast.dump(t))

                else:

                    print('printing fArg')
                    pp.pprint(t)

        elif is_string(obj) or is_int(obj) or is_float(obj):

            print(obj)

        else:

            pp.pprint(obj)
            


def print_and_eval(obj,tree,fArg):
    
    print('&'*30)
    print('displaying fArgs')
    print_obj(fArg,'original fArg is:',True)
    print_obj(tree,'parse tree is:',True)
    print_obj(obj,'value is:',True)

    return obj


def time_func(func):

    originalFuncName=func.__name__

    @wraps(func)
    def timed(*args):

        t0=tm.time()
        v=func(*args)
        print(f'time to run {originalFuncName}: {tm.time() - t0}')

        return v

    return timed


def keystep(obj):

    print('press key to continue')
    input()

    return obj


def embedding_functions(*args):

    return [f for v,f in zip(args[::2],args[1::2]) if v]


############################
# HELPERS FOR VERBOSE MODE #
############################

def build_key_step(message,buildKeyStep):

    if buildKeyStep:

        print(message)
        print('press enter to continue ...')
        input()


def print_tree(tree,message,verbose,buildKeyStep=False):
    '''
    Helper function to print trees mid-optimization.
    We can only do buildKeyStep is verbose is true as well.
    '''
    # print('print_tree')
    # print(f'{verbose} is verbose')

    if verbose:

        print('*'*30)
        print(message)
        astpretty.pprint(tree)
        print('*'*30)

    else:

        buildKeyStep=False

    build_key_step(message,buildKeyStep)


