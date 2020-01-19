'''
python3 filters.py 

python3 watch_file.py -p2 python3 filters.py -p1 ./reinstall_from_source.sh -d /Users/bennettbullock/python-pype-lang-3
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

###########
# FILTERS #
###########

def filter_gt(obj):
    '''
    The curly brackets enclose a booleanfArg, in this case the expression _>1.
    When the accum (obj) is a list, we return every element where this fArg
    evaluates as true.  
    When it is a dict, we apply the fArg to every value.
    '''
    ({_>1},
    )


def filter_is_in(obj,st):
    '''
    Here, if obj is a list, we apply the filter fArg _ >> st to every element
    of that list.  If obj is a dict, we apply that filter to every value.

    _ >> st means, is the list element/dictionary value in the set st.
    '''
    ({_ >> st},
    )


####################
# EMBEDDED FILTERS #
####################

'''
The following two functions run embedded loops on obj.
'''

def embedded_filter_gt(obj):
    '''
    Here, we are applying the filter to embedded lists or dicts.
    '''
    ([{_>1}],
    )


def embedded_filter_gt_cleaned(obj):
    '''
    Here, we are applying the filter to embedded lists or dicts.

    The final fArg, {_}, says "Only include list elements or dict values 
    which evaluate as True.  Empty lists, dicts, sets, strings, or anything
    that evaluates as False is excluded.
    '''
    ([{_>1}],
     {_},
    )
    

pypeify_namespace(globals())

if __name__=='__main__':

    print('*'*30)
    print('list filters')
    print('*'*30)

    ls=[-2,-3,5,-1,-1,2,3,4]
    st=set([5,2,3,4])

    print('-'*30)
    print(f'{ls} is ls')
    print('-'*30)
     
    print('filter_gt(ls)')
    print(filter_gt(ls))

    print('-'*30)
    print(f'{ls} is ls')
    print(f'{st} is st')
    print('-'*30)

    print('map_is_in(ls,st)')
    print(filter_is_in(ls,st))

    print('*'*30)
    print('dict filters')
    print('*'*30)

    js={'a':-2,'b':-3,'c':5,'d':-1,'e':-1,'f':2}
    st=set([5,2,3,4])

    print('-'*30)
    print(f'{js} is js')
    print('-'*30)
     
    print('filter_gt(js)')
    print(filter_gt(js))

    print('-'*30)
    print(f'{js} is ls')
    print(f'{st} is st')
    print('-'*30)

    print('filter_is_in(js,st)')
    print(filter_is_in(js,st))

    print('*'*30)
    print('embedded filters')
    print('*'*30)

    js={'a':[-2,1,5],'b':[2,-3,8,9,10],'c':[8,5,20,1],'d':[-30,-20,-40]}

    print('-'*30)
    print(f'{js} is ls')
    print('-'*30)

    print('embedded_filter_gt(js)')
    print(embedded_filter_gt(js))

    print("notice that 'd' is am empty list, so let's clean it")

    print('embedded_filter_gt_cleaned(js)')
    print(embedded_filter_gt_cleaned(js))
