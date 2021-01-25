'''
python3 quicksort.py

python3 watch_file.py -p2 python3 quicksort.py -p1 ./reinstall_from_source.sh -d /Users/bennettbullock/python-pype-lang-3/
'''
from pype3 import p,pypeify_namespace,pypeify
from pype3 import _,iff,tup,l
from pype3.helpers import middle
from pype3.func_helpers import to_int

def qs0(ls):
    '''
    middle takes the middle element of the list.  Let's explore the expression:

              {len:(qs0,{_ < pivot}) + [pivot] + (qs0,{_ > pivot}),
               'else':_}

    First, this is a switch dict, meaning that if one of the keys evaluates as true,
    then the corresponding expression also evaluates as true.  So if ls is not
    empty, then len evaluates as true, and we apply the function recursively.  Otherwise
    we return the emply ls.  

              (qs0,{_ < pivot})

    This applies a filter to ls, taking anything below the pivot.  Then we recursively
    apply the function to this list.  
    

              l(pivot)

    This constructs a singleton list with pivot.

              (qs0,{_ > pivot})

    This applies a filter to ls, taking anything above the pivot.  Then we recursively
    apply the function to this list.  

              (qs0,{_ < pivot}) + [pivot] + (qs0,{_ > pivot})

    We concatenate these three lists, and return.
    '''
    pivot=middle(ls)

    (ls,
     {len:(qs0,{_ < pivot}) + l(pivot) + (qs0,{_ > pivot}),
      'else':_}
    )


def qs1(ls):
    '''
    Now, we are going to apply the iff macro. So for a conditional fArg cond, and a 
    statement, iff(cond,statement) evaluates as:

              {cond:statement,
               'else':_}
.
    So, if len evaluates as True (nonzero), then we return the statement, otherwise
    we return the empty list.  
    '''
    pivot=middle(ls)

    (ls,
     iff(len,(qs1,{_ < pivot}) + l(pivot) + (qs1,{_ > pivot}))
    )


def qs2(ls):
    '''
    And we can even take away the accum.  Notice, however, the final comma, making
    the statement a tuple.  
    '''
    pivot=middle(ls)

    iff(len,(qs2,{_ < pivot}) + l(pivot) + (qs2,{_ > pivot})),


def qs3(ls):
    '''
    Finally, we are using the assignment operator.  Notice that middle is a 
    function called on ls.  The result is stored in the variable pivot.
    '''
    (pivot << middle,
     iff(len,(qs3,{_ < pivot}) + l(pivot) + (qs3,{_ > pivot})),
    )


def qs4(ls):
    '''
    Finally, we are using the assignment operator.  Notice that middle is a 
    function called on ls.  The result is stored in the variable pivot.

    There is a bit of weirdness here.  Notice that when we are indexing for
    pivot, we have to wrap the lambda expression in a tup.  This is because
    the indexing automatically interprets a tuple as a set of indices, so we
    have to wrap it in one more tuple to get it to evaluate as a lambda.
    '''
    (ln << len,
     pivot << _[tup(int,ln/2)],
     iff(ln,(qs4,{_ < pivot}) + l(pivot) + (qs4,{_ > pivot})),
    )

'''
pypeify compiles all the functions above ...
'''
pypeify_namespace(globals())

if __name__=='__main__':

    print('*'*30)
    print('Welcome to pype quicksort!')
    ls=[3,5,7,1,4,76]
    print(f'{ls} is ls')

    print('*'*30)
    print('running qs0')
    print(qs0(ls))

    print('*'*30)
    print('running qs1')
    print(qs1(ls))

    print('*'*30)
    print('running qs3')
    print(qs3(ls))

    print('*'*30)
    print('running qs4')
    print(qs4(ls))
