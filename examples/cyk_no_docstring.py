'''
python3 cyk.py 

python3 watch_file.py -p2 python3 cyk.py -p1 ./reinstall_from_source.sh -d /Users/bennettbullock/python-pype-lang-3
'''
from pype3 import pypeify,pypeify_namespace,p,_,_0,_1,_2,_last
from pype3 import ep,l,db,a,iff,d,ift,iftp,squash,ifp,cl
from pype3.time_helpers import *
from pype3.helpers import *
from pype3.vals import PypeVal as v

GRAMMAR_STRING='''
NP Det N
VP V NP
S NP VP
'''

def read_grammar(grammarString):

    (_.splitlines,
     {_},
     [_.split],
     [{'lhs':_0,
       'rhs1':_1,
       'rhs2':_2}],
     (merge_ls_dct,_,'rhs1'),
     [(merge_ls_dct,_,'rhs2')],
     [[_0]],
     [[_.lhs]],
    )


def init_table(seq):

    (enumerate,
     [{_0:{_0:{'lhs':_1,
               'tree':l(_1)}}}], 
     [(dct_merge_vals,),{},_],
    )


def partitions(seq):

    (seqLen << len,
     spans << (range_list,1,seqLen),
     begin1s << ep(spans,
                   [(range_list,0,_)],
                   flatten_list),
     partitions << ep(spans,
                      [(range_list,0,seqLen-_)],
                      flatten_list),
     (cartesian,spans,begin1s,partitions),
     (zip_to_dicts,_,'span','begin1','partition'),
     [a('end1',_.begin1 + _.partition)],
     [a('begin2',_.end1 + 1)],
     [a('end2',_.begin1 + _.span)],
     {_.begin2 <= _.end2},
     unique_dcts,
     (sort_by_keys,_,'span','begin1'),
    )


def apply_partition_for_grammar(table,ptn,grammar):
    
    (begin1 << ptn.begin1,
     end2 << ptn.end2,
     rhs1 << _[begin1,ptn.end1],
     rhs2 << _[ptn.begin2,end2],
     lhs << grammar[rhs1.lhs,rhs2.lhs],
     iff(lhs,(dct_merge_vals,_,
                             {begin1:{end2:{'lhs':lhs,
                                            'tree':l(lhs,
                                                     rhs1.tree,
                                                     rhs2.tree)}}})),
    )


def apply_partitions(seq,grammar):

    (apply_partition << cl([tb,ptn],
                           (apply_partition_for_grammar,_,ptn,grammar)),
     [(apply_partition,),init_table,partitions],
    )


def parse(seq,grammar):

    ((apply_partitions,_,grammar),
     finalConstituent << _[0,len-1],
     {finalConstituent:finalConstituent.tree,
      'else':'No valid parse'},
    )


pypeify_namespace(globals())

if __name__=='__main__':

    seq=['Det','N','V','Det','N']
    grammar=read_grammar(GRAMMAR_STRING)
    prs=parse(seq,grammar)

    pp.pprint(prs)
