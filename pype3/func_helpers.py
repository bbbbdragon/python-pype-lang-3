'''
python3 watch_file.py -p1 python3 func_helpers.py -d /Users/bennettbullock/python-pype-lang-3/pype3
'''
from pype3.type_checking import *
from functools import *
# from pype3 import pypeify,pypeify_namespace,p,_,_0,_1,_2,a,ep,tup,iff
from pype3.vals import Quote as q
from pype3.helpers import *
import pprint as pp
from collections import Counter
import numpy as np

FLOAT_L=1e-100

def deep_map(obj,transform,verify=None):
 
    if verify is not None and verify(obj):

        return transform(obj)

    if is_list(obj):

        return [deep_map(el,transform,verify) for el in obj]

    if is_dict(obj):

        return {k:deep_map(v,transform,verify) for (k,v) in obj.items()}

    if verify is not None and not verify(obj):

        return obj

    if verify is None:

        return transform(obj)


def deep_dct_delete(obj,field):
 
    if is_list(obj):

        ls=[deep_dct_delete(el,field) for el in obj]

        return [el for el in ls if el]

    if is_dict(obj):

        dct={k:deep_dct_delete(v,field) for (k,v) in obj.items() \
             if k != field}

        return {k:v for (k,v) in dct.items() if v}

    return obj


def default_filter_verify(obj):

    if is_list(obj):

        return False

    if is_dict(obj):

        return False

    if not obj:

        return False

    return True


def num_filter_verify(obj):

    if is_list(obj):

        return False

    if is_dict(obj):

        return False

    if isinstance(obj,int) \
       or isinstance(obj,float) \
       or type(obj).__module__ == np.__name__:

        return True

    if not obj:

        return False

    return True


def non_number_bool(obj):

    if not is_list(obj) \
       and not is_dict(obj) \
       and not isinstance(obj,bool) \
       and (is_int(obj) \
            or is_float(obj) \
            or np.isreal(obj)):

        return True

    return bool(obj)


def deep_filter(obj,verify=default_filter_verify,deleteZeros=False):

    # test_f=lambda x:non_number_bool(x) if not deleteZeros \
           # else lambda x:x


    if is_list(obj):

        null=[]

    elif is_dict(obj):

        null={}

    else:

        null=False

    if verify(obj):

        return obj

    if is_list(obj):

        ls=[deep_filter(el,verify) for el in obj]
        ls=[el for el in ls if non_number_bool(el)]

        if ls:

            return ls

    if is_dict(obj):

        dct={k:deep_filter(el,verify) for (k,el) in obj.items()}
        dct={k:el for (k,el) in dct.items() if non_number_bool(el)}

        if dct:

            return dct

    return null



def deep_filter_container(obj,verify=default_filter_verify):

    if is_list(obj):

        null=[]

    elif is_dict(obj):

        null={}

    else:

        null=False

    if verify(obj):

        return obj

    if is_list(obj):

        ls=[deep_filter(el,verify) for el in obj]
        ls=[el for el in ls if el]

        if ls:

            return ls

    if is_dict(obj):

        dct={k:deep_filter(el,verify) for (k,el) in obj.items()}
        dct={k:el for (k,el) in dct.items() if el}

        if dct:

            return dct

    return null


def filter_recs(ls):

    return [type(el) for el in ls]


def deep_reduce_flatten(obj,verify=lambda x:True):

    # short_pp(obj)

    if verify(obj):

        # print('found object')

        return [obj]

    if is_list(obj):

        ls=[deep_reduce_flatten(el,verify) for el in obj]

        return flatten_lists(ls)

    if is_dict(obj):

        ls=[deep_reduce_flatten(el,verify) \
            for (k,el) in obj.items()]

        return flatten_lists(ls)

    return []


def deep_reduce(accumulator,obj,transform,verify=None):

    ls=deep_reduce_flatten(obj,verify)

    return reduce(transform,ls,accumulator)


def deep_collect(obj,verify):

    def append(ls,x):

        ls.append(x)

        return ls

    return deep_reduce([],obj,append,verify)


def deep_collect_fields(obj,field):

    has_field=lambda dct: isinstance(dct,dict) and field in dct
    dcts=deep_collect(obj,has_field)
    
    return [dct[field] for dct in dcts]


def deep_collect_multi_fields(obj,*fields):

    if is_list(fields[0]):

        fieldSet=set(fields[0])

    else:

        fieldSet=set(fields)

    has_fields=lambda dct: isinstance(dct,dict) \
        and all([field in dct for field in fieldSet])
    dcts=deep_collect(obj,has_fields)
    dctsWithFields=[{k:v for (k,v) in dct.items() if k in fieldSet} \
                    for dct in dcts]

    return dctsWithFields


def deep_collect_fields_first(obj,field):

    fields=deep_collect_fields(obj,field)

    if fields:

        return fields[0]

    return False


def deep_count(obj,verify):

    def increment(n):

        return n+1

    return deep_reduce(0,obj,increment,verify)


def deep_add(obj,verify):

    def increment(c,n):

        return c+n

    return deep_reduce(0,obj,increment,verify)


def deep_prob(obj,verify=is_int):

    sm=deep_add(obj,verify)

    def p(n):

        return n/(sm+FLOAT_L)

    return deep_map(obj,p,verify)


#########################
# EMBEDDED DICTIONARIES #
#########################

def embed_tups(tup):

    if len(tup) == 1:

        return [tup[0]]

    if len(tup) == 2:

        return [tup[0],tup[1]]

    return [tup[0],embed_tups(tup[1:])]


def embed_dcts_rec(obj,final_func):

    # Is this a list?
    if is_list(obj) and obj:

        firstElement=obj[0]

        # If this is not the last tuple, we call tup_ls_dct and recurse into
        # the result.
        if is_list(firstElement):

           if len(firstElement) > 1 \
              and len(firstElement[-1]) > 1:

               return embed_dcts_rec(tup_ls_dct(obj),final_func)


    if is_dict(obj):

        # print("returning dict")

        return {k:embed_dcts_rec(v,final_func) for (k,v) in obj.items()}

    # print('returning obj')
    # short_pp(obj)

    return final_func(obj)


def embed_dcts(obj,final_func=lambda x:x):

    tups=[embed_tups(tp) for tp in obj]
        
    return embed_dcts_rec(tups,final_func)
    

def embed_counters(obj):

    return embed_dcts(obj,lambda x:dict(Counter(x)))
    

############
# OLD JUNK #
############

def map_deep(obj,verify,transform):

    if verify(obj):

        return transform(obj)

    if is_list(obj):

        return [map_deep(el,verify,transform) for el in obj]

    if is_dict(obj):

        return {k:map_deep(v,verify,transform) for (k,v) in obj.items()}

    return obj
 
 
def reduce_deep(accumulator,obj,transform,empty,verify=None):

    if verify is not None and verify(obj):

        return transform(accumulator,obj)

    if is_list(obj):

        return reduce(transform,
                      [reduce_deep(accumulator,el,transform,empty,verify) \
                       for el in obj],
                      accumulator)

    if is_dict(obj):

        return reduce(transform,
                      [reduce_deep(accumulator,el,transform,empty,verify) \
                       for (k,el) in obj.items()],
                      accumulator)

    return empty(obj)


        

def to_type(x,defaultVal,f):

    if not x:

        return defaultVal

    return f(x)


def to_string(x):

    return to_type(x,'',str)


def to_int(x):

    return to_type(x,0,int)


def to_float(x):

    return to_type(x,0.,float)


def to_br_float(x):

    x=x.replace(',','.')

    return to_type(x,0.,float)


def identity(x):

    return x


EXAMPLE_MAPPING={'CATEGORIZADOR_OLIVIA_DTC':{'replace':'l2Category',
                                             'cast_f':to_string},
                 'VALOR_TRANSACAO_LOCAL':{'replace':'amount',
                                          'cast_f':to_br_float}}

'''
def apply_mapping(mapping,js):

    (dct_items,
     [tup(_1.replace,(_1.cast_f,js[_0]))],
     tup_dct,
    )
'''

# pypeify_namespace(globals())

from itertools import product 

def js_type(obj):

    if is_list(obj):

        ls=[js_type(el) for el in obj]
        
        if all([isinstance(el,type) for el in ls]):

            return list(set(ls))

        if all([is_dict(el) for el in ls]):

            # Do they have the same keys?

            keySets=[set(el.keys()) for el in ls]
            diffs=[s1.symmetric_difference(s2) \
                   for (s1,s2) in product(keySets,keySets)]

            if all([len(diff) == 0 for diff in diffs]):

                return [ls[0]]

        return ls

    if is_dict(obj):

        # items=[(k,js_type(v)) for (k,v) in obj.items()]
        dct={k:js_type(v) for (k,v) in obj.items()}

        return dct

    return type(obj)


def is_atom(ob):

    return not is_dict(ob) and not is_list(ob)


def flatten_json_rec(ob):

    if is_dict(ob):

        atoms={k:v for (k,v) in ob.items() if is_atom(v)}
        dcts=[v for (k,v) in ob.items() if is_dict(v)]
        dcts=merge_dcts(dcts) if dcts else {}
        dct={**atoms,**dcts}
        lists=[flatten_json_rec(v) for (k,v) in ob.items() if is_list(v)]
        lists=flatten_lists(lists)

        if lists:

            prod=[(el1,el2) for (el1,el2) in product([dct],lists)]

            return prod

        return dct

    if is_list(ob):

        return [flatten_json_rec(el) for el in ob]

    return ob


def unroll(tup):

    if isinstance(tup,tuple):

        return flatten_lists([tup[0]] + unroll(tup[1]))

    return [tup]


def flatten_dct(ob):

    flattenedTuples=flatten_json_rec(ob)
    unrolled=[unroll(tup) for tup in flattenedTuples]
    
    return [merge_dcts(ls) for ls in unrolled]


if __name__=='__main__':

    js={'a':[1,2,3],
        'b':{'c':2,'d':'this'},
        'e':[{'f':'that','g':'those'},
             {'f':'that','g':'those'},
             {'f':'that','g':'those'}]}

    pp.pprint(js_type(js))
