name='pype3'
__version__='3.0.27'
py_slice=slice
from pype3.build_helpers import *
from pype3.nodes import *
from pype3.trees import *
from itertools import groupby
from functools import reduce
from inspect import signature
from collections import defaultdict
from inspect import getsource
from ast import *
import inspect
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
# We are importhing these symbols for visibility, so you can say from pype3 import _0
from pype3.fargs import _,_0,_1,_2,_3,_4,_5,_6,_7,_8,_9,_10,_last
from pype3.macros import ep,iff,ift,ifp,iftp,db,dbp,mp,l,lm,ifa,ifta,ea,dp
from pype3.macros import select,a,ap,m,d,tup,app,c,is_true,squash,change
from pype3.macros import cl,dm,cl_if,cl_has,cl_app,ext,consec,consec_dct
from pype3.macros import embed,td,tdm
# from numba import njit
# import astor

#######################
# NAIVE PYPE FUNCTION #
#######################

def p(accum,*fArgs):
    '''
    This is the base pype function before compilation.  It returns fArgs.
    '''
    return fArgs

pype_f=p


################
# PYPE ALIASES #
################

def aliases_for_pype(glbls):
    '''
    This searches through the global namespace of a function to find any aliases for
    the pype function.  Helps when pype is given another name, as in:

    from pype import pype as p

    Using try-catch block for objects with ambiguous truth values, like numpy arrays.
    '''
    aliases=set()

    for (alias,f) in glbls.items():

        try:

            if is_callable(f) and glbls[alias] == pype_f:

                aliases.add(alias)

        except Exception as e:
            '''
            print(f'for alias {alias}')
            print(e)
            print('adding alias anyway')
            '''
            pass

    return aliases


###############
# COMPILATION #
###############

def add_main_modules(mod,glbls):

    for name in dir(mod):

        attr=getattr(mod,name)
        modName=''

        if is_callable(attr):

            if hasattr(attr,'__name__') and attr.__name__ in NUMPY_UFUNCS:

                modName='numpy'

            else:

                modName=attr.__module__

        if is_module(attr):

            modName=attr.__name__

        if modName:

            #print(f'importing {modName}')

            glbls[modName]=__import__(modName)

    return glbls


def apply_tree_transformation(tree,replacer,originalFuncName,glbls):
    
    replacerNamespace={}
    
    replacer.visit(tree)
    '''
    Now, we recompile the function into the recompiledReplacedNamespace, and
    extract the fArgs.
    '''
    exec(compile(tree,
                 filename='<ast>',
                 mode='exec'),
         glbls,
         replacerNamespace)

    return tree,replacer,replacerNamespace[originalFuncName]


'''
Stores all optimized functions.
'''
FUNCTION_CACHE={}

import builtins
#import astpretty
#import pprint as pp

def pype_tree(originalFuncName,
              tree,
              args,
              glbls,
              embeddingNodes,
              verbose,
              buildKeyStep,
              aliases,
             ):

    print_tree(tree,'parse tree before:',verbose,buildKeyStep)

    '''
    If function does not have an accum in its returned expression, we put
    one there.
    '''
    noAccumReplacer=NoAccumReplacer(aliases)
    
    noAccumReplacer.visit(tree)
    
    print_tree(tree,'parse tree after no accum replacer:',verbose)
    
    '''
    Now, we see if a return is in the final pype expression.  If it is
    not, then we insert it into the AST.
    '''
    noReturnReplacer=NoReturnReplacer(aliases)
    
    noReturnReplacer.visit(tree)
    
    print_tree(tree,'parse tree after no return replacer:',verbose,buildKeyStep)

    '''
    We make a copy of that tree for the final pass.
    '''
    originalTree=deepcopy(tree)
    
    print_tree(originalTree,'original tree is:',verbose,buildKeyStep)
    
    '''
    Now, we want to replace any name, either in the global variables or the
    function body, that appears in the function body with NameBookmark.
    
    This NameBookmark will allow variables in the scope of the function to
    not be evaluated into literals by the Pyhton interpreter.  When the 
    optimizer gets to them, it will convert them into Name objects.  This
    also allows us to use macros such as _assoc or _iff, which will return
    pype expressions which contain these NameBookmark object.  
    
    We recompile the function into the recompiledReplacedNamespace, and
    extract the fArgs.
    '''
    tree,replacer,f=apply_tree_transformation(tree,
                                              NameBookmarkReplacer(aliases),
                                              originalFuncName,
                                              glbls)
    accumNode=replacer.accumNode
    
    print_tree(tree,'after call name replacer tree is',verbose,buildKeyStep)

    '''
    KwargsReplacer
    '''
    tree,replacer,f=apply_tree_transformation(tree, 
                                              KwargsReplacer(aliases),
                                              originalFuncName,
                                              glbls)

    print_tree(tree,'after kwarg replacer tree is',verbose,buildKeyStep)
    '''
    Now, we want to iterate through the tree and see if there are any BinOp
    nodes, representing expressions such as a+1, len+3, etc.  We are doing
    this so that you no longer have to insert a PypeVal in an arithmatic
    expression to get it to compile, so you can just type 'len + 3' instead
    of 'v(len) + 3'.  This makes your code cleaner.  
    
    The reason we can get away with this is that the Python parser only 
    checks for syntactically valid expressions - the interpreter crashes 
    when it arrives at them.  So we cut the interpreter off at the pass and
    turn the expression into something that the interpreter will compile.
    '''
    tree,replacer,recompiled_f=apply_tree_transformation(tree,
                                                         PypeValReplacer(),
                                                         originalFuncName,
                                                         glbls)
    
    print_tree(tree,'after operator replacer tree is',verbose,buildKeyStep)
    
    '''
    recompiled_pype_func returns the fArgs only, so calling this on *args
    will give us just the fArgs.  Remember, these fArgs will be fArgs in
    the intermediate form, so _assoc('a',1) will appear as ['DCT_ASSOC','a',1].
            
    This allows us to define macro shortcuts like _iff, which returns a 
    switch dict.  
    '''
    fArgs=recompiled_f(*args)

    print_obj(fArgs,'printing fArgs',verbose)

    '''
    Now, we run the optimizations and convert the fArgs into a list of trees.
    Embedding nodes are determined by the keyword arguments, usually they're
    a wrapper that prints something and then returns the value.  
    '''
    fArgTrees=optimize_f_args(fArgs,accumNode,embeddingNodes)
    
    print_obj(fArgTrees,'printing fArg trees',verbose)
    
    '''
    We start compiling.  We use the originalTree, which is the tree with
    a return inserted into the final statement if necessary.
    
    We go through the returned expression and build an AST for 
    that expression using the fArg trees.  aliases helps us find the 
    returned pype call.
    '''
    fArgReplacer=FArgReplacer(fArgTrees,aliases)
    
    fArgReplacer.visit(originalTree)
    
    print_tree(originalTree,'printing final tree',verbose,buildKeyStep)

    return originalTree


def get_glbls(pype_func):

    glbls=pype_func.__globals__
    moduleName=pype_func.__module__
    mod=__import__(moduleName)
    glbls[moduleName]=mod
    glbls=add_main_modules(mod,glbls)
    glbls['builtins']=__import__('builtins')
    glbls['_operator']=__import__('_operator')
    glbls['np']=__import__('numpy')

    return glbls


def pypeify(verbose=False,
            timed=False,
            printAccums=False,
            keyStep=False,
            buildKeyStep=False,
            # njitOptimized=False
           ):
    '''
    TODO: Recursive Functions can't be compiled with explicit build.
    '''

    def build_decorator(pype_func):
        '''
        functionDecorators are functions that are applied to the compiled function.
        nodeEmbedders are functions that are applied to each fArg.
        '''
        '''
        functionDecorators=embedding_functions(njitOptimized,
                                               njit,
                                               timed,
                                               time_func)
        '''
        functionDecorators=embedding_functions(timed,
                                               time_func)
        embeddingNodes=embedding_functions(*[printAccums,
                                             print_and_eval_node,
                                             keyStep,
                                             keystep_node])

        # print(f'{functionDecorators} is functionDecorators')
        '''
        The originalFuncName is used in FUNCTION_CACHE to refer to the function.
        It also is put into the global namespace.  Maybe there's a better way ...
        I have no fucking idea.
        '''
        originalFuncName=pype_func.__name__
        '''
        We extract the source of the function.  Meaning, the function has to be
        somewhere on file.  That's just a rule.  
        '''
        src=getsource(pype_func)
        '''
        Build a namespace containing all the globals of the function, and the
        namespaces of all the modules referenced.  It's really just spaghetti thrown
        against the wall.
        '''
        glbls=get_glbls(pype_func)
        '''
        Grab aliases for pype in the global namespace.
        '''
        aliases=aliases_for_pype(glbls)

        @wraps(pype_func)
        def build_wrapper(*args):
            '''
            If we've already compiled this function, then just grab it from the 
            function cache and evaluate it.
            '''
            if originalFuncName in FUNCTION_CACHE:
                
                return FUNCTION_CACHE[originalFuncName](*args)

            '''
            First, we get a tree from the source code.
            '''
            tree=parse(src)
            
            print_tree(tree,'parse tree before:',verbose,buildKeyStep)

            '''
            We make the transformations on the tree.
            '''
            originalTree=pype_tree(originalFuncName,
                                   tree,
                                   args,
                                   glbls,
                                   embeddingNodes,
                                   verbose,
                                   buildKeyStep,
                                   aliases,
                                  )
            '''
            We compile the new tree, storing the result in recompiledReplacerNamespace.
            '''
            recompiledReplacerNamespace={}

            # print(astor.to_source(originalTree)) # Here we want to_source

            exec(compile(originalTree,
                         filename='<ast>',
                         mode='exec'),
                 glbls,
                 recompiledReplacerNamespace)

            '''
            recompiled_pype_func is the new function.  
            '''
            recompiled_pype_func=recompiledReplacerNamespace[originalFuncName]

            '''
            Now, we apply any function decorators we want.  These are different
            from the embedded nodes in that they are applied to the function,
            rather than the AST.
            '''
            for f in functionDecorators:

                recompiled_pype_func=f(recompiled_pype_func)

            '''
            We put it in the FUNCTION_CACHE. This is called by originalFuncName.
            '''

            FUNCTION_CACHE[originalFuncName]=recompiled_pype_func
            '''
            And we return the first evaluation of that function.
            '''

            return FUNCTION_CACHE[originalFuncName](*args)

        return build_wrapper

    return build_decorator


pype_builder=pypeify


#####################################
# COMPILATION OF ALL PYPE FUNCTIONS #
#####################################

def pypeify_namespace(namespace,
                      functionCache=FUNCTION_CACHE):
    '''
    This function searches a namespace for any pype functions which do not have the
    'pype' decorator.  If the function does not have the 'pype' decorator, then the 
    kwargs for this decorator will build the function in a customized fashion.  If
    the function does not have the decorator, then 'pypeify' will compile this 
    function with the default kwargs.  This allows the user to set the kwargs when
    necessary for debugging.  

    However, in order for this to happen, 'pypeify' has to be declared *after* all
    pype functions without the 'pype' decorator are declared/defined, and 
    *before* any of them are run.  So this will not work:

        pypeify()

        pfunc1(x):

            (x,
             _+1) 

        pfunc1(1) => None
    
    This, however, will work:

        pfunc1(x):

            (x,
             _+1)

        pypeify()

        pfunc1(1) => 2

    As will this:

        pypeify()

        @pype
        pfunc1(x):

            (x,
             _+1)
       
        pfunc1(1) => 2
    '''
    aliases=aliases_for_pype(namespace)
    allPypeFunctions={k:v for (k,v) in namespace.items() \
                      if is_pype_function(v,aliases)}

    for (k,v) in allPypeFunctions.items():
        
        if not is_pype_decorated_function(v):

            f=pype_builder()(v)
            
            namespace[k]=f


def to_python(fileName):

    src=''

    with open(fileName,'r') as f:

        src=f.read()

    

def pypeify_all():

    for fr in inpsect.stack():

        namespace=fr.frame.f_globals

        pypeify_namespace(namespace)        


'''
@build(verbose=True,buildKeyStep=True)
def test_f(x):

    _+1,
'''

