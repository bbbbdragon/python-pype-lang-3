from operator import *
from pype3.type_checking import *
from pype3.helpers import flatten_tuple

##########
# ASSIGN #
##########

class VarAssign(object):

    def __init__(self,assignTo,assignFrom):

        self.assignTo=assignTo
        self.assignFrom=assignFrom

    
    def __repr__(self):

        return f'VarAssign(assignTo={self.assignTo},assignFrom={self.assignFrom})'


class KwargApply(object):

    def __init__(self,applyTo):

        self.assignTo=applyTo

    
    def __repr__(self):

        return f'KwargApply(applyTo={self.applyTo})'


class LamTup(object):
    '''
    This takes expressions and overrides operators for them.
    '''
    def __init__(self,*tup):

        if not tup:

            raise Exception('LamTup.__init__: tup needs to have one '
                            'or more values')

        self._tup_=tup


    def __str__(self):

        return 'L'+str(self._tup_)


    def __repr__(self):

        return self.__str__()


    def __getitem__(self,val):

        # We rewrite and return acceptable expressions.

        if (is_tuple(val) or is_list(val)):

           if len(val) > 1:

               # We are making this definition recursive, since I do not want to 
               # evaluate two different structures for indexing.
               # The first is _[0][0], the second is _[0,0], which should both
               # after delam parse as ((('_pype_mirror_',), [0]), [0])

               return LamTup(self.__getitem__(val[:-1]),(val[-1],))

           else:

               return LamTup(self.val(),(val[0],))

        elif is_slice(val):

            return LamTup(getitem,self.val(),(slice,val.start,val.stop))

        return LamTup(self.val(),(val,))


    def __getattr__(self,val):

        return LamTup(self.val(),(val,))


    def __hash__(self):

        return hash(str(self._tup_))

    def val(self):

        if len(self._tup_) == 1:

            return self._tup_[0]

        return tuple(self._tup_)

    # Unary Arithmetic

    def __neg__(self):

        return LamTup(neg,self.val())

    # Binary Arithmetic 

    def __add__(self,other):

        return LamTup(add,self.val(),other)

    def __radd__(self,other):

        return LamTup(add,other,self.val())

    def __sub__(self,other):

        return LamTup(sub,self.val(),other)

    def __rsub__(self,other):

        return LamTup(sub,other,self.val())


    def __mul__(self,other):

        return LamTup(mul,self.val(),other)

    def __rmul__(self,other):

        return LamTup(mul,other,self.val())


    def __floordiv__(self,other):

        return LamTup(floordiv,self.val(),other)

    def __rfloordiv__(self,other):

        return LamTup(floordiv,other,self.val())

    def __truediv__(self,other):

        return LamTup(truediv,self.val(),other)

    def __rtruediv__(self,other):

        return LamTup(truediv,other,self.val())

    def __mod__(self,other):

        return LamTup(mod,self.val(),other)

    def __rmod__(self,other):

        return LamTup(mod,other,self.val())

    def __pow__(self,other):

        return LamTup(pow,self.val(),other)

    def __rpow__(self,other):

        return LamTup(pow,other,self.val())

    # Comparators

    def __eq__(self,other):

        return LamTup(eq,self.val(),other)

    def __ne__(self,other):

        return LamTup(ne,self.val(),other)

    def __lt__(self,other):

        return LamTup(lt,self.val(),other)

    def __le__(self,other):

        return LamTup(le,self.val(),other)

    def __gt__(self,other):

        return LamTup(gt,self.val(),other)

    def __ge__(self,other):

        return LamTup(ge,self.val(),other)

    # Boolean operators

    def __not__(self):

        return LamTup(not_,self.val())

    def __invert__(self):

        return LamTup(not_,self.val())

    def __and__(self,other):

        return LamTup(and_,self.val(),other)

    def __ror__(self,other):

        return LamTup(or_,self.val(),other)

    def __or__(self,other):

        return LamTup(or_,self.val(),other)

    def __xor__(self,other):

        return LamTup(xor,self.val(),other)

    def __rshift__(self,other):

        return LamTup(contains,other,self.val())

    def __rrshift__(self,other):

        return LamTup(contains,self.val(),other)

    def __lshift__(self,other):

        return VarAssign(self.val(),other)

    def __rlshift__(self,other):

        return VarAssign(other,self.val())

    
###########
# PYPEVAL #
###########

class PypeVal(LamTup):
    '''
    A PypeVal is intended to use all the operator overrites for a LamTup, except
    for a single value.  So len + 1 will not compile with the Python interpreter,
    but PypeVal(len)+1 will compile into something the pype interpreter will interpret
    as a lambda (add,len,1).  This is part of pype's strategy of "making the Python
    parser generate syntactically valid Python expressions that the pype parser 
    consumes."
    '''
    def __init__(self,*val):

        if not val:

            raise Exception('PypeVal.__init__: no value to initialize')

        if len(val) > 2:

            raise Exception('PypeVal.__init__: you need to provide only one value')

        self._tup_=(val[0],)


    def __str__(self):

        return f'PV({str(self._tup_)})'


##################
# KwargsBookMark #
##################

class KwargsBookmark(PypeVal):

    def __init__(self,exp):

        self.exp=exp
        

    def val(self):

        print('calling val')

        return KwargsBookmark(self.exp)


    def __repr__(self):

        return f"KwargsBookmark('{self.exp}')"

    
##########
# GETTER #
##########

class Getter(PypeVal):
    '''
    The getter returns itself only for 'val'.  This is for unique objects.

    Actually, it's deprecated, since _0, _1, _3 are no longer Getter objects, but
    indices.  
    '''
    def val(self):

        return self

    def __str__(self):

        return 'G'+str(self._tup_)


################
# NAMEBOOKMARK #
################

class NameBookmark(PypeVal):
    '''
    This was designed for the compiler only, and should not be used in programming. 
    The idea is that the compiler must identify variables in a pype expression which
    are previously defined, and mark them as Name nodes instead of literals.  

    However, when pype macros are used, such as iff, the compiler first sees the macro
    and not the value that the macro returns.  If these contain variable names,
    we may have to write a node for each macro, which is ridiculous.  So, instead,
    we go through the original syntax tree - the one with the macros - and replace
    any in-scope variables with NameBookmark objects.  Then, we evaluate p, which
    returns a list of raw fArgs in their intermediate form.  So something like:

        a('val',1),

    Gets returned as ['DICT_ASSOC',1], which can then be converted to an AST node by
    the compiler.  However, if the macro contains a reference to an in-scope variable,
    as in:

       a('val',x),

    and the first value of x is 1, then the returned fArg would be ['DICT_ASSOC',1].  To
    prevent this from happening, we declare a NameBookmark around x, so the process 
    becomes:

       a('val',x) => a('val',NameBookmark(x)) => ['DICT_ASSOC',NameBookmark(x)]

    When the compiler sees NameBookmark(x), it generates a node Name(id='x'), which
    refers to the in-scope variable.  
    '''
    def __init__(self,name):

        self.name=name
        

    def val(self):

        return NameBookmark(self.name)


    def __repr__(self):

        return f"NameBookmark('{self.name}')"


#########
# QUOTE #
#########

class Quote(object):
    '''
    This object is for when we want to pass functions or other fArgs into other 
    functions as arguments.  For example, if I had the functions:

        def mult2(x):
        
            return x*2

        def f1(x,f):

            return f(x)+1

    If I were to put f1 in a lambda like this:

        p( 2,
           (f1,_,mult2))

    the function would crash, because 'mult2' is evaluated on 2 instead of being
    passed into 'f1'.  So I do this:

        from pype3.vals import Quote as q

        p( 2,
           (f1,_,q(mult2))) => mult2(2)+1 => 4+1 => 5
    '''
    def __init__(self,v):

        # print(f'intializing quote with v as {v}')
        self.v=v

    def quote_val(self):

        #print('evaluating quote')

        return self.v
        
    def __str__(self):

        return 'Q('+str(self.v)+')'



#################
# TYPE CHECKING #
#################

is_pype_val=lambda x: isinstance(x,PypeVal)
is_getter=lambda x: isinstance(x,Getter)
is_lam_tup=lambda x: isinstance(x,LamTup) and not is_pype_val(x) and not is_getter(x)


#########
# DELAM #
#########

def is_bookmark(fArg):
    '''
    This is a weird hack - I couldn't get isinstance to work on NameBookmark for some
    odd reason.  
    '''
    return "NameBookmark" in str(fArg.__class__)


def is_kwargs(fArg):
    '''
    This is a weird hack - I couldn't get isinstance to work on NameBookmark for some
    odd reason.  
    '''
    return "KwargsBookmark" in str(fArg.__class__)


def delam(expr):
    '''
    This function converts a LamTup, or any of its descendants, into a data structure
    that the compiler can convert into an AST node.

    When we get a LamTup, or any of its descendants, we can't just feed it into the
    pype compiler.  We need to extract the data structure that 'expr' encloses.  We
    do this recursively, because we want to allow LamTups to be embedded in one another.
    For example, the expression:

        v(1)+2+3

    Evaluates as: 

        L(<built-in function add>, (<built-in function add>, 1, 2), 3).  

    When we appy delam to this, it evaluates as:

       (<built-in function add>, (<built-in function add>, 1, 2), 3)

    which the pype compiler can now compile.  
    '''
    #print('*'*30)
    #print('delam')
    #print(f'{expr} is expr')

    # When it is a LamTup, we extract the value, and run delam on that value.
    if is_lam_tup(expr):

        return delam(expr.val())

    # If it is a dictionary, we have to be a bit careful.  If the dictionary
    # contains keys which are lamTups, then we cannot extract them directly, because
    # certain fArg types - mappings for example - are not hashable.  Instead
    # we have to deal with them in the compiler.
    if is_dict(expr):

        # This allows lam tups to appear as keys, but then be evaluated as
        # lambdas in switch dicts and dict builds.

        return {k:delam(v) for (k,v) in expr.items()}

    # If it's a list, then just run it on the list.
    if is_list(expr):

        return [delam(el) for el in expr]

    # Do the same for a tuple, but wrap it in a tuple.
    if is_tuple(expr):

        #print('is tuple')

        return tuple([delam(el) for el in expr])

    # We don't use getters anymore, so don't worry about this.
    if is_getter(expr):

        return expr

    # NameBookmarks we want to keep as is so that the compiler can turn them into
    # Name Nodes.
    if is_bookmark(expr):

        return expr

    if is_kwargs(expr):

        return expr

    # Since PypeVals just enclose a value, run delam on the enclosed value.
    if is_pype_val(expr):

        return delam(expr.val())

    # Sets are tricky, since all their elements must be hashable.  So we're gonna 
    # deal with them in the compiler.  
    if is_set(expr):

        return expr

    # Base Case: Return the extracted data structure. This covers literals and pretty
    # much any other data structure.  
    return expr



#################
# OTHER HELPERS #
#################

'''
Most of these aren't necessary anymore, because the compiler takes care of supplying
PypeVals where necessary.  However, just in case, were gonna keep them.  
'''
def l(*args):
    '''
    This is for when you want to use a lambda in an expression with a binary operator,
    like:

        l(f1,2) + 2

    However, the compiler will accept:

        (f1,2) + 2

    So don't worry.
    '''
    return PypeVal((*args,))

'''
This old trusty thing is used quite often in older versions of pype, but now you
can just use 'len'.
'''
lenf=PypeVal(len)

'''
Other crap I never use.
'''
empty=lambda ls: len(ls) == 0
empty_1=lambda tup: len(tup[1]) == 0
single=lambda ls: len(ls) == 1
single_1=lambda tup: len(tup[1]) == 1

singlef=PypeVal(single)
emptyf=PypeVal(empty)
quote=lambda v: Quote(v)

def not_empty(v):

    return len(v) != 0

