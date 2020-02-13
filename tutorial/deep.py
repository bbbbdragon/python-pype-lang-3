'''
python3 deep.py 

python3 watch_file.py -p2 python3 deep.py -p1 ./reinstall_from_source.sh -d /Users/bennettbullock/python-pype-lang-3
'''
from pype3 import pypeify,pypeify_namespace,p,_,_0,_1,_2,_last,cl,ifa,ifta
from pype3 import ep,db,a,iff,d,ift,squash,ifp
from pype3.time_helpers import *
from pype3.helpers import *
from pype3.func_helpers import *
from pype3.vals import PypeVal as v, Quote as q
from copy import deepcopy
from pype3.numpy_helpers import *
import pprint as pp

'''
Basic tutorial that covers deep mapping, reducing, and filtering.  Deep 
mapping, reducing, and filtering technique that allows you to perform
these operations on embedded data structures such as JSON's.  
'''

def add1(n):

    (_+1,
    )


#############
# DEEP MAPS #
#############

def deep_map_add(js):
    '''
    We take every value in the JSON and add 1.
    '''
    (add1 << cl(_+1),
     (deep_map,_,add1),
    )


def deep_map_ifa(js):
    '''
    transform << cl(ifa(is_string,
                         ('good' >> _),
                         _+' yes')),

    If the function is a string containing 'good', then we add ' yes' to 
    that string.
    '''
    (transform << cl(ifa(is_string,
                         ('good' >> _),
                         _+' yes')),
     (deep_map,_,transform),
    )


def deep_map_ifta(js):
    '''
    cl(ifta(is_string,
            ('good' >> _))),

    This is returns true if all fArgs evaluate as true, otherwise False.
    '''
    (verify << cl(ifta(is_string,
                       ('good' >> _))),
     transform << cl(_+' yes!'),
     (deep_map,_,transform,verify),
    )


################
# DEEP FILTERS #
################

def deep_filter_ifta(js):
    
    (fil << cl(ifta(is_int,
                    _ > 2)),
     (deep_filter,_,fil),
    )


################
# DEEP REDUCES #
################

def deep_reduce_count(js):
    '''
    aug << cl([s,x],
               s+x),

    Add x to s.

    cl(is_int),

    Is this an integer?
    '''
    (aug << cl([s,x],
               s+x),
     verify << cl(is_int),
     (deep_reduce,0,_,aug,verify),
    )


pypeify_namespace(globals())

if __name__=='__main__':

    print('*'*30)
    print('deep maps')
    print('*'*30)

    js={'a':{'b':[1,2,3]},'c':5,'d':{'b':[[1,2],3]}}

    pp.pprint(js)
    print('is js')

    print('deep_map_add(js)')
    print(deep_map_add(js))

    print('ifa')
    print(ifa(is_string,('good' >> _),_+'yes'))

    js={'a':{'b':[1,2,3]},'c':5,'d':{'b':[[1,2],3]},'good':'this is good'}

    pp.pprint(js)
    print('is js')

    print('deep_map_ifa(js)')
    print(deep_map_ifa(js))

    print('ifta')
    print(ifta(is_string,('good' >> _)))

    print('deep_map_ifta(js)')
    print(deep_map_ifta(js))

    print('deep_filter_ifta(js)')
    print(deep_filter_ifta(js))

    print('deep_reduce_count(js)')
    print(deep_reduce_count(js))
