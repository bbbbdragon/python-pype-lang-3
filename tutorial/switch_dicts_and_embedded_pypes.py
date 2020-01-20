'''
python3 switch_dicts_and_embedded_pypes.py 

python3 watch_file.py -p2 python3 switch_dicts_and_embedded_pypes.py -p1 ./reinstall_from_source.sh -d /Users/bennettbullock/python-pype-lang-3
'''
from pype3 import pypeify,pypeify_namespace,p,_,_0,_1,_2,_last
from pype3 import ep,tup,db,a,iff,d,ift,iftp,squash,ifp
from pype3.time_helpers import *
from pype3.helpers import *
from pype3.vals import PypeVal as v
from copy import deepcopy
from pype3.numpy_helpers import *

'''
Basic tutorial that covers switch dicts and embedded pypes.  

Switch dicts these implement conditional statements.  Embedded pypes do a 
separate evaluation on the accum.
'''

################
# SWITCH DICTS #
################

def switch_dict(n):
    '''
    This is shows the simple functionality of a switch-dict.  If n is equal to
    any key in the switch dict, we evaluate the corresponding fArg value, and
    return it.
    '''
    ({_ == 1:'one',
      _ == 2:'two',
      'else':"I don't know"},
    )


def iff_example(n):
    '''
    The iff macro returns n*100 if n>2, else n.
    '''
    (iff(_>2,_*100),
    )


def ift_example(n):
    '''
    The iff macro returns n*100 if n>2, else False.
    '''
    (ift(_>2,_*100),
    )
    

def func(x,k):
    '''
    This is just a simple polynomial x**2 + x + k. 
    '''
    (_ + _**2 + k,
    )


def sm(a,b):

    (_+b,
    )


def embedded_pype(ls):
    '''
    An embedded pype, or 'ep' takes the accum, and evaluates a sequence of
    fArgs on it.  The ep in this case evaluates:

    func(max(ls)*2,4)
    '''
    ((sm,len,ep(max,
                _*2,
                (func,_,4))),
    )


def embedded_pype_dict(js):
    '''
    An embedded pype, or 'ep' takes the accum, and evaluates a sequence of
    fArgs on it.  The ep in this case evaluates:

    func(max(dct_values(js))*2,4)
    '''
    ((sm,len,ep(dct_values,
                max,
                _*2,
                (func,_,4))),
    )


def switch_dict_and_ep(ls):
    '''
    Here we are going to do some more sophisticated computation.  If the
    ls has a length of less than 3, we apply an 'ep', or 'embedded pype',
    shown in the last function.  Otherwise, we return the length of the list. 
    '''
    ({len < 3:ep(max,
                 _*2,
                 (func,_,4)),
      'else':len},
    )


def ift_example(n):
    '''
    The first argument of an ifp statement is a contitional, and the rest 
    are fArgs for an ep. If the conditional evaluates as True, return the
    results of the ep.  Otherwise, return n.
    '''
    (ift(_ > 2,_*100),
    )


def iftp_example(n):
    '''
    The first argument of an iftp statement is a contitional, and the rest 
    are fArgs for an ep. If the conditional evaluates as True, return the
    results of the ep.  Otherwise, return False.
    '''

    (ifp(_*10,[_+1]),
    )


def ifp_example(n):
    '''
    If the accum is n, evaluate the accum in the fArgs.  Otherwise, 
    return n.
    '''
    (ifp(_*10,[_+1]),
    )




pypeify_namespace(globals())

if __name__=='__main__':

    print('*'*30)
    print('switch dicts')
    print('*'*30)

    print('switch_dict(1)')
    print(switch_dict(1))

    print('switch_dict(2)')
    print(switch_dict(2))

    print('switch_dict(3)')
    print(switch_dict(3))

    print('iff_example(1)')
    print(iff_example(1))

    print('iff_example(3)')
    print(iff_example(3))

    print('ift_example(1)')
    print(ift_example(1))

    print('ift_example(3)')
    print(ift_example(3))
    
    print('*'*30)
    print('embedded pypes for lists')
    print('*'*30)

    ls=[-2,-3,5,-1,-1,2,3,4]

    print('-'*30)
    print(f'{ls} is ls')
    print('-'*30)

    print('embedded_pype(ls)')
    print(embedded_pype(ls))

    print('*'*30)
    print('embedded pypes for dicts')
    print('*'*30)

    js={'a':-2,'b':-3,'c':5,'d':-1,'e':-1,'f':2,'g':3,'h':4}

    print('-'*30)
    print(f'{js} is js')
    print('-'*30)

    print('embedded_pype_dict(js)')
    print(embedded_pype_dict(js))

    print('*'*30)
    print('switch dict and embedded pype')
    print('*'*30)
    
    ls=[-2,-3,5,-1,-1,2,3,4]

    print('-'*30)
    print(f'{ls} is ls')
    print('-'*30)

    print('switch_dict_and_ep(ls)')
    print(switch_dict_and_ep(ls))

    ls=[-2,-3]

    print('-'*30)
    print(f'{ls} is ls')
    print('-'*30)

    print('switch_dict_and_ep(ls)')
    print(switch_dict_and_ep(ls))

    print('ift_example(1)')
    print(ift_example(1))

    print('ift_example(5)')
    print(ift_example(5))

    print('ifp_example([])')
    print(ifp_example([]))

    print('ifp_example([1,2,3,4])')
    print(ifp_example([1,2,3,4]))

    print('iftp_example([])')
    print(iftp_example([]))

    print('iftp_example([1,2,3,4])')
    print(iftp_example([1,2,3,4]))
