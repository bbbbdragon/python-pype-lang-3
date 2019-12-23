'''
python3 watch_file.py -p2 python3 basic_tutorial.py  -p1 ./reinstall_from_source.sh -d /Users/bennettbullock/python-pype-lang-3
'''
from pype3 import pypeify,pypeify_namespace,p,_,_0,_1,_2,ep,tup,db,a,iff,d,ift,squash,ifp
# import sys 
# import json
from pype3.time_helpers import *
from pype3.helpers import *
from pype3.vals import PypeVal as v
from copy import deepcopy
from pype3.numpy_helpers import *
# from pype3.helpers import short_pp
# from pype3.loaders import load_json

'''
Basic tutorial that covers mirrors, indexes, and slices.
'''

'''
def mirror_example(n):

    _,


def f(n):

    return n+1


def callable_example(x):

    f,


def index_example_multi_ls(ls):

    _[0][1],


def index_example_dct(dct):

    _.item,
'''

'''
def index_example_dct_ls(dct):

    _.item[0],


class TestObj(object):

    def __init__(self,val):

        self.vl=val

    def get_val(self):

        return self.vl


def index_example_getitem(obj):

    _.vl, #Can't use val, TODO - make val non-obvious in PypeVals and Getters.


def index_example_call(obj):

    _.get_val,


@pypeify(hardIndexing=True)
def hard_index_example_ls(ls):

    _[2],


@pypeify(hardIndexing=True)
def hard_index_example_multi_ls(ls):

    _[0][1],


@pypeify(hardIndexing=True)
def hard_index_example_dct(dct):

    _.item,


@pypeify(hardIndexing=True)
def hard_index_example_dct_ls(dct):

    _.item[0],
'''


class TestListObj(object):

    def __init__(self,ls):

        self.ls=ls

    def get_ls(self):

        return self.ls


@pypeify(hardIndexing=True,
         verbose=True)
def hard_index_example_obj_val(obj):

    _.ls[0],


@pypeify(verbose=True)
def hard_index_example_get_obj_val(obj):

    _.get_ls,


pypeify_namespace(globals())

if __name__=='__main__':

    '''
    print('*'*30)
    print('mirrors')

    x=mirror_example(1)

    print(mirror_example(1))

    print('*'*30)
    print('callables')
    
    print(callable_example(1))

    print('*'*30)
    print('indexing')

    ls=[[0,1],[2]]

    print(index_example_multi_ls(ls))

    dct={'item':'hi'}

    print(index_example_dct(dct))

    dct={'item':[5,4,3]}

    print(index_example_dct_ls(dct))
    
    obj=TestObj(1)

    print(index_example_getitem(obj))

    print(index_example_call(obj))

    print('*'*30)
    print('hard indexing')

    ls=[1,2,3,4]

    print(hard_index_example_ls(ls))

    ls=[[0,1],[2]]

    print(hard_index_example_multi_ls(ls))
    
    dct={'item':'hi'}

    print(hard_index_example_dct(dct))
    '''

    obj=TestListObj([1,2,3])

    print(hard_index_example_obj_val(obj))

    obj=TestListObj([1,2,3])

    print(hard_index_example_get_obj_val(obj))

    '''
    dct={'item':[5,4,3]}

    print(index_example_dct_ls(dct))
    '''


