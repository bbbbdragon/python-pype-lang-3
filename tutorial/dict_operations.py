'''
python3 dict_operations.py 

python3 watch_file.py -p2 python3 dict_operations.py -p1 ./reinstall_from_source.sh -d /Users/bennettbullock/python-pype-lang-3
'''
from pype3 import pypeify,pypeify_namespace,p,_,_0,_1,_2,_last
from pype3 import ep,tup,db,a,iff,d,ift,squash,ifp,m,change
from pype3.time_helpers import *
from pype3.helpers import *
from pype3.vals import PypeVal as v
from copy import deepcopy
from pype3.numpy_helpers import *
import numpy
'''
Basic tutorial that covers switch dict/JSON manipulations.
'''

###############
# DICT BUILDS #
###############

def dict_build_simple_1(n):
    '''
    This shows a simple way to build a dictionary, and then add another key
    to it. db('n') takes the accum and builds a singleton dictionary keyed by
    'n'. a('m',_.n+3) adds another key-value pair to the accum, where the
    key is 'm' and the value is the value for 'n' plus 3.
    '''
    (db('n'), # {'n':1}
     a('m',_.n+3), # {'n':1,'m':4}
    )


def dict_build_merge(n,d2={'a':1,'b':2}):
    '''
    This will show how pype can merge dictionaries together in a simple
    and elegant manner. m(d2) merges the accum with d2, replacing any 
    equally-keyed values in the accum with their values in d2.
    '''
    (db('a'), # {'a':2}
     m(d2), # {'a':1,'b':2}
    )


def dict_build_dissoc(n):
    '''
    Here, we show how to delete a key-value pair from the dict.
    '''
    (db('a'), # {'a':2}
     a('b',_.a+3), # {'a':2,'b':4}
     a('c',_.a*_.b), # {'a':2,'b':4,'c':8}
     d('b'), # {'a':2,'c':8} - we drop 'b' from the dictionary.
    )


def dict_build_explicit(n):
    '''
    Here, we are doing an explicit dict build.  This differs from a switch
    dict by not having 'else' as a key.  
    '''
    ({'a':_,
      'b':_+2,
      'c':_*5},
    )


def dict_build_squash(n):
    '''
    The squash function takes an embedded dictionary, and makes its key-value
    pairs part of the embedding dictionary.
    '''
    ({'a':_,
      'b':{'d':_+2,
           'e':_*20},
      'c':_*5}, # ('a':2,'b':{'d':4,'e':40},'c':10}
     squash('b'), # ('a':2,'d':4,'e':40,'c':10}
    )


def dict_build_change(n):
    '''
    The change function changes the key in the dicitonary.
    '''
    (db('a'), # {'a':2}
     change('a','b'), # {'b':2}
    )


def dict_build_std(ls):
    '''
    In this example we compute the median standard deviation.  For a varable
    x, this would be median(|x_i - median(x)|).  

    This also shows how easily pype3 is integrated with numpy.  Notice the
    subtraction of two numpy arrays in _.a - _.median.
    '''
    (np.array, # cast list of Python integers to numpy array.
     {'a':_, # 'a' stores the array.
      'median':np.median}, # we compute the median
     _.a - _.median, # take the difference from the median
     np.abs, # take the absolute values.
     np.median, # take the median of that
    )



pypeify_namespace(globals())

if __name__=='__main__':

    print('*'*30)
    print('dict build')
    print('*'*30)

    print('dict_build_simple_1(1)')
    print(dict_build_simple_1(1))

    print('dict_build_merge(5)')
    print(dict_build_merge(5))

    print('dict_build_dissoc(2)')
    print(dict_build_dissoc(2))

    print('dict_build_explicit(2)')
    print(dict_build_explicit(2))

    print('dict_build_squash(2)')
    print(dict_build_squash(2))

    print('dict_build_change(2)')
    print(dict_build_change(2))

    ls=[1,2,5,3,5,6,6,4,3,66,7,8,4,3,2,3,5,68,7,5,43,2,2,4,565,3,2,2222,22,4]

    print('-'*30)
    print(f'{ls} is ls')
    print('-'*30)

    print(dict_build_std(ls))
    print(dict_build_std(ls))
