from pype3 import pypeify,pypeify_namespace,p,_,_0,_1,_2,a,ep,tup,iff
from pype3.vals import Quote as q
from pype3.helpers import *

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
