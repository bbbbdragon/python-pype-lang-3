'''
python3 cyk.py 

python3 watch_file.py -p2 python3 cyk.py -p1 ./reinstall_from_source.sh -d /Users/bennettbullock/python-pype-lang-3

This is a pype implementation of my functional implementation of the CYK parsing
algorithm in Clojure, at https://bitbucket.org/bbbdragon/bennett-cyk-demo.  It 
demonstrates that an algorithm which has traditionally been implemented as a series
of loops over a static table can be implemented functionally.  

The algorithm is described in full at: https://en.wikipedia.org/wiki/CYK_algorithm

The pype implementation implements the algorithm functionally in the same way that 
the Clojure algorithm does.  The only difference is under-the-hood.  

Because Clojure data structures are so light-weight, it can generate new structures 
with every iteration and not have any performance hits.  In this case, however, the 
same table structure is being updated with each iteration - the code is functional, but
the underlying implementation does not guarantee immutability.

To view the ability to express complex concepts concisely, you may want to take
a look at cyk_no_docstring.py.  There, I strip out the docstrings.
'''
from pype3 import pypeify,pypeify_namespace,p,_,_0,_1,_2,_last
from pype3 import ep,l,db,a,iff,d,ift,iftp,squash,ifp,cl,dm
from pype3.time_helpers import *
from pype3.helpers import *
from pype3.vals import PypeVal as v


'''
In the grammar string, we define a context-free grammar.  The first symbol in each
line is the left-hand-side symbol, or lhs.  The second symbol is the first 
right-hand-side symbol, or rhs1.  The third symbol is the second right-hand-side
symbol, or rhs2.
'''
GRAMMAR_STRING='''
NP Det N
VP V NP
S NP VP
'''

def read_grammar(grammarString):
    '''
    We read the grammar string and convert it into a JSON of the form 
    {rhs1:{rhs2:lhs,...},...}

     _.splitlines,

    This splits the grammar string by line.

     {_},

    {} indicates we are filtering over a list, and including whatever elements in 
    the list evaluate as true.  Since _ is a string, and an empty string evaluates as
    false, this filters out any empty strings.

     [_.split],

    Split the strings by space.


     [(zip_to_dict,_,'lhs','rhs1','rhs2')],

    Build a dictionary from each tuple, with 'lhs' keying the first element
    of the tuple, 'rhs1' keying the second element of each tuple, and 'rhs2'
    keying the third.

    This splits each line into tuples of 3.  The first is assigned to the 'lhs' in
    the dictionary.  The second is 'rhs1'.  The third is 'rhs2'.

    (merge_ls_dct,_,'rhs1'),

    We aggregate these dictionaries by 'rhs1', giving us a dictionary of the form
    {rhs1:[{'rhs1':rhs1,'rhs2':rhs2,'lhs':lhs},...],...}.

    [(merge_ls_dct,_,'rhs2')],

    This performs the same merge on the embeded dictionaries, producing a JSON of
    form: {rhs1:{rhs2:[{'rhs1':rhs1,'rhs2':rhs2,'lhs':lhs}],...},...}

    [[_0]]

    Since rhs1 and rhs2 are keys to single-element lists, we extract the first element
    from this list, so now our JSON is:{rhs1:{rhs2:{'rhs1':rhs1,'rhs2':rhs2,
    'lhs':lhs},...},...}

    [[_.lhs]],

    Now, we want to extract only the 'lhs' from the JSON keyed by rhs1 and rhs2, 
    producing a JSON of the form: {rhs1:{rhs2:lhs,...},...}.

    One thing to note is that this only applies to deterministic Context-Free 
    grammars, which allow only one parse for a string.  This is the case with
    programming languages, but is not the case for Natural Languages. 
    '''
    (_.splitlines,
     {_},
     [_.split],
     [(zip_to_dict,_,'lhs','rhs1','rhs2')],
     (merge_ls_dct,_,'rhs1'),
     [(merge_ls_dct,_,'rhs2')],
     [[_0]],
     [[_.lhs]],
    )


def init_table(seq):
    '''
    Takes a sequence, seq.  Blow-by-blow:

     enumerate,

    Enumerate seq, creating pairs of indices and symbols such as (0,"Dt'),
    (1,"N"), etc.

     [{_0:{_0:{'lhs':_1,
               'tree':l(_1)}}}], 

    Go through each pair, assign the symbol to an 'lhs' field, put the symbol
    in a singleton list, and assign that list to 'tree'.

     [(dct_merge_vals,),{},_],

    Run a reduce to merge the list of dictionaries into an empty dictionary.

    Final output should look like:

    {'Det': {'Det': {'lhs': 3, 'tree': [3]}},
    'N': {'N': {'lhs': 4, 'tree': [4]}},
    'V': {'V': {'lhs': 2, 'tree': [2]}}}
    '''
    (enumerate,
     [{_0:{_0:{'lhs':_1,
               'tree':l(_1)}}}], 
     [(dct_merge_vals,),{},_],
    )


def partitions(seq):
    '''
    In our strategy, we do not want to iterate over a static table, but rather
    iterate over a series of partitions.  Each partition is a JSON of the form:

    {'begin1':begin1,
     'end1':end1,
     'begin2':begin2,
     'end2':end2}

    It defines a partition of the string which the parser will evaluate to generate
    and insert new symbols.  To do this, we take a length of the partition:

      seqLen << len,

    Then, we define 'spans', which defines the maximum range for each partition.

      spans << (range_list,1,seqLen),

    Then, we build a list of i1Begin indices:

     iBegin1s << ep(spans,
                    [(range_list,1,_)],
                    flatten_list),

    These indices specify where the partition index begins.  Then, we build the
    partitions:

     partitions << ep(spans,
                      [(range_list,0,seqLen-_)],
                      flatten_list),

    These tell us where the partition is made.  To find the triplets of
    of (begin,partition,begin+1), we start with the Cartesian product:

     (cartesian,spans,iBegin1s,partitions),

    We want to map these tuples to dictionaries, where 'span' keys the first
    tuple, 'begin1' keys the second tuple, and 'partition' keys the third
    tuple:

     [(zip_to_dict,_,'span','begin1','partition')],

    Finally, we want to build partitions as dictionaries:

     [a('end1',_.begin1 + _.partition)],
     [a('begin2',_.end1 + 1)],
     [a('end2',_.begin1 + _.span)],

    Get rid of the 'partition' field, and filter out every partition where
    the 'begin1' field is greater than the 'end2' field:

     [d('partition')],
     {_.begin2 <= _.end2},

    Get only the unique dictionaries, and sort by their span, and then their
    i1Begin.

     unique_dcts,
     (sort_by_keys,_,'span','i1Begin'),
    
    The end result looks like this:

    [{'begin1': 0, 'begin2': 1, 'end1': 0, 'end2': 1, 'span': 1},
    {'begin1': 1, 'begin2': 2, 'end1': 1, 'end2': 2, 'span': 1},
    {'begin1': 2, 'begin2': 3, 'end1': 2, 'end2': 3, 'span': 1},
    {'begin1': 3, 'begin2': 4, 'end1': 3, 'end2': 4, 'span': 1},
    {'begin1': 0, 'begin2': 1, 'end1': 0, 'end2': 2, 'span': 2},
    {'begin1': 0, 'begin2': 2, 'end1': 1, 'end2': 2, 'span': 2},
    {'begin1': 1, 'begin2': 2, 'end1': 1, 'end2': 3, 'span': 2},
    '''
    (seqLen << len,
     spans << (range_list,1,seqLen),
     begin1s << ep(spans,
                   [(range_list,0,_)],
                   flatten_list),
     partitions << ep(spans,
                      [(range_list,0,seqLen-_)],
                      flatten_list),
     (cartesian,spans,begin1s,partitions),
     [(zip_to_dict,_,'span','begin1','partition')],
     [a('end1',_.begin1 + _.partition)],
     [a('begin2',_.end1 + 1)],
     [a('end2',_.begin1 + _.span)],
     {_.begin2 <= _.end2},
     unique_dcts,
     (sort_by_keys,_,'span','begin1'),
    )


def apply_partition_for_grammar(table,ptn,grammar):
    '''
    This takes a single partition, checks if there's an rhs1-rhs2 pair in the
    grammar, and if there is, we get an lhs that evaluates as True.  If we do,
    then we merge the table with a new dictionary for the new constituent.  
    Otherwise, we return the table as is.

     begin1 << ptn.begin1,
     end2 << ptn.end2,

    Placeholders for later use.

     rhs1 << _[begin1,ptn.end1],
     rhs2 << _[ptn.begin2,end2],
     lhs << grammar[rhs1.lhs,rhs2.lhs],

    rhs1 and rhs2 are recalled from the tables.  lhs is taken from the grammar.
    If the rhs1-rhs2 pair aren't in the grammar, lhs is False.

     iff(lhs,dm({begin1:{end2:{'lhs':lhs,
                               'tree':l(lhs,
                                        rhs1.tree,
                                        rhs2.tree)}}})),

    The iff returns the original table if lhs is False.  dm is a macro that
    does a deep merge of the table, so that the dict with any begin key
    can have multiple end keys.

     {'lhs':lhs,
      'tree':l(lhs,
               rhs1.tree,
               rhs2.tree)}}

    The lhs is a string for the new lhs.  The tree is a list containing the
    lhs, and the trees for rhs1 and rhs2.
    '''    
    (begin1 << ptn.begin1,
     end2 << ptn.end2,
     rhs1 << _[begin1,ptn.end1],
     rhs2 << _[ptn.begin2,end2],
     lhs << grammar[rhs1.lhs,rhs2.lhs],
     iff(lhs,dm({begin1:{end2:{'lhs':lhs,
                               'tree':l(lhs,
                                        rhs1.tree,
                                        rhs2.tree)}}})),
    )


def apply_partitions(seq,grammar):
    '''
    This runs through all partitions, in their proper order, and applies them
    to the table.  

     apply_partition << cl([tb,ptn],
                           (apply_partition_for_grammar,_,ptn,grammar)),

    This closure binds the grammar variable, so we can have a function that 
    has two variables, one for an accumulator (the table) and another for an
    item in the reduce (the partition).  This will allow it to fit into a 
    reduce function.  

     [(apply_partition,),init_table,partitions],

    The start value of the reduce is init_table(seq).  The iteratable is 
    partitions(seq).  
    '''
    (apply_partition << cl([tb,ptn],
                           (apply_partition_for_grammar,_,ptn,grammar)),
     [(apply_partition,),init_table,partitions],
    )


def parse(seq,grammar):
    '''
    Main function.

     (apply_partitions,_.split,grammar),

    _.split splits the string by space. (apply_partitions,_.split,grammar) is
    a lambda called on these two arguments, producing a table.

     _[0,len-1],

    First, len is length of the table, also the lenght of the original sequence.
    len-1 is the final index of the table.  We know that indexing returns False
    if an element is not present at this index path.  Otherwise, we retrieve
    the constituent with 'lhs' and 'tree' fields.

     {_:_.tree,
       'else':'No valid parse'},

    Switch dict - if the accum evaluates as False, we return 'No valid parse',
    otherwise we return the 'tree field of the parse.
    '''
    ((apply_partitions,_.split,grammar),
     _[0,len-1],
     {_:_.tree,
      'else':'No valid parse'},
    )

pypeify_namespace(globals())

if __name__=='__main__':

    seq=['Det','N','V','Det','N']
    seq='Det N V Det N'
    grammar=read_grammar(GRAMMAR_STRING)
    prs=parse(seq,grammar)

    pp.pprint(prs)
