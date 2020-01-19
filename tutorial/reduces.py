'''
python3 reduces.py 

python3 watch_file.py -p2 python3 reduces.py -p1 ./reinstall_from_source.sh -d /Users/bennettbullock/python-pype-lang-3
'''
from pype3 import pypeify,pypeify_namespace,p,_,_0,_1,_2,_last
from pype3 import ep,tup,db,a,iff,d,ift,squash,ifp
from pype3.time_helpers import *
from pype3.helpers import *
from pype3.vals import PypeVal as v
from copy import deepcopy
from pype3.numpy_helpers import *

'''
Basic tutorial that covers filters.
'''

def add(x,y):

    (_+y,
    )


###########
# REDUCES #
###########

def summation(ls):
    '''
    A simple summation reduce.  The first singleton tuple specifies the reduce 
    function, which has one argument for the accumulator in the reduce.  The
    second fArg expresses the starting value, which is ls in this case.

    Notice that the reduce works with elements of lists and values of
    dictionaries.
    '''
    ([(add,),_],
    )


def summation_start_val(ls,startVal):
    '''
    When the reduce has two fArgs after the singleton tuple, the first fArg
    is a starting value, and the second fArg is the iteration.
    '''
    ([(add,),startVal,_],
    )


def summation_start_val_filtered(ls,startVal):
    '''
    Here, we demonstrate how we can manipulate the iterable and the startVal
    using fArgs. startVal+len means startVal+len(ls), and {_ > -1} means
    all elements in the list greater than -1.
    '''
    ([(add,),startVal+len,{_ > -1}],
    )



pypeify_namespace(globals())

if __name__=='__main__':

    print('*'*30)
    print('reduces on lists')
    print('*'*30)

    ls=[-2,-3,5,-1,-1,2,3,4]
    st=set([5,2,3,4])

    print('-'*30)
    print(f'{ls} is ls')
    print('-'*30)
     
    print('summation(ls)')
    print(summation(ls))

    print('summation_start_val(ls,100)')
    print(summation_start_val(ls,100))

    print('summation_start_val_filtered(ls,100)')
    print(summation_start_val_filtered(ls,100))

    print('*'*30)
    print('reduces on dicts')
    print('*'*30)

    js={'a':-2,'b':-3,'c':5,'d':-1,'e':20,'f':2}

    print('-'*30)
    print(f'{js} is js')
    print('-'*30)
     
    print('summation(js)')
    print(summation(js))

    print('summation_start_val(js,100)')
    print(summation_start_val(js,100))

    print('summation_start_val_filtered(js,100)')
    print(summation_start_val_filtered(js,100))
