from collections import defaultdict
import numpy as np
# from numba import njit
'''
These are just functions to check types of objects.
'''
def is_tuple(x): return isinstance(x,tuple)
def is_dict(x): return isinstance(x,dict)
def is_ddict(x): return isinstance(x,defaultdict)
def is_list(x): return isinstance(x,list)
def is_mapping(x): return  isinstance(x,dict)
def is_bool(x): return  isinstance(x,bool)
def is_object(x): return  isinstance(x,object)
def is_string(x): return isinstance(x,str)
def is_set(x): return isinstance(x,set)
def is_int(x): return isinstance(x,int)
def is_slice(x): return isinstance(x,slice)
def is_iterable(x): return isinstance(x,Iterable)
def is_mapping(x): return isinstance(x,Mapping)
def is_hashable(x): return isinstance(x,Hashable)
def is_ndarray(x): return isinstance(x,np.ndarray)
def is_sequence(x): return isinstance(x,Sequence) or is_ndarray(x)
def is_container(x): return isinstance(x,Container)
def is_float(x): return isinstance(x,float)
def is_integer(x): return isinstance(x,int)
def is_callable(x): return callable(x)
def key(tup): return tup[0]
def val(tup): return tup[1]
slc=lambda ls,start,stop: ls[start:stop]

