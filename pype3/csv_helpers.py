import csv
from pype3 import pypeify,pypeify_namespace,p,_,_0,_1,_2,a,ep,tup,iff
from pype3.helpers import *
from pype3.mappings import *

EXAMPLE_MAPPING={'CATEGORIZADOR_OLIVIA_DTC':{'replace':'l2Category',
                                             'cast_f':to_string},
                 'VALOR_TRANSACAO_LOCAL':{'replace':'amount',
                                          'cast_f':to_br_float}}

def apply_mapping(mapping,js):

    (dct_items,
     [tup(_1.replace,(_1.cast_f,js[_0]))],
     tup_dct,
    )


def csv_to_dct(f):

    (csv.DictReader,
     list,
     [dict],
    )


def load_csv(fName):

    with open(fName,'r') as f:

        return csv_to_dct(f)


def iter_paths(d):
    '''
    Thanks https://gist.github.com/SegFaultAX/b926fe97c2ac1db1fb313f3a9372ee56
    '''
    def iter1(d, path):

        paths=[]

        if isinstance(d,dict):

            return [iter1(v,path+[k]) for (k,v) in d.items()]

        elif isinstance(d,list):
            
            return [iter1(v,path+[v]) for v in d]

        return path

    return iter1(d,[])

def to_csv(val,line=[]):

    return iter_paths(val)

    '''
    pp.pprint(val)
    pp.pprint(line)
    isDict=isinstance(val,dict)
    isList=isinstance(val,list)
    lines=[]

    if isinstance(val,dict):

        for (k,v) in val.items():

              line.append(k)

              lines.extend(to_csv(v,line))
            
    if isinstance(val,list):

        for v in val:

            line.append(v)
            lines.extend(to_csv(v,line))
    
    else:

        line.append(val)

        return [line]
    '''
pypeify_namespace(globals())
