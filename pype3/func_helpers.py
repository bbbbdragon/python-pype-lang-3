from pype3.type_checking import *
from functools import *
from pype3 import pypeify,pypeify_namespace,p,_,_0,_1,_2,a,ep,tup,iff
from pype3.vals import Quote as q
from pype3.helpers import *

def map_deep(obj,verify,transform):

    if verify(obj):

        return transform(obj)

    if is_list(obj):

        return [map_deep(el,verify,transform) for el in obj]

    if is_dict(obj):

        return {k:map_deep(v,verify,transform) for (k,v) in obj.items()}

    return obj


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


def deep_filter(obj,verify):

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

    return False


def deep_reduce(accumulator,obj,transform,verify=None):

    if verify is not None and verify(obj):

        return transform(accumulator,obj)

    if is_list(obj):

        return reduce(transform,
                      [deep_reduce(accumulator,el,transform,verify) \
                       for el in obj],
                      accumulator)

    if is_dict(obj):

        return reduce(transform,
                      [deep_reduce(accumulator,el,transform,verify) \
                       for (k,el) in obj.items()],
                      accumulator)

    if verify is not None and not verify(obj):

        return accumulator

    if verify is None:

        return transform(accumulator,obj)


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


def apply_mapping(mapping,js):

    (dct_items,
     [tup(_1.replace,(_1.cast_f,js[_0]))],
     tup_dct,
    )


pypeify_namespace(globals())
