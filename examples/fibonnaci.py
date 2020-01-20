'''
python3 fibonnaci.py

python3 watch_file.py -p1 python3 fibonnaci.py  -d /Users/bennettbullock/python-pype-lang-3
'''
from pype3 import pypeify_namespace,p
from pype3 import _,iff

'''
This shows you how to run the Fibonnaci sequence using three different, but 
syntactically equivalent pype expressions.  Let's take a walk through the main
statement:

    (fib0,_-1)+(fib0,_-2),

The placeholder _ is the variable from the last evaluated fArg, in this case x.  
We are computing the Fibonnaci sequence for x-1 in (fib0,_-1), and for x-2 in 
(fib0,_-2), and adding them together.

However, we only want to do this when x > 1.  If x is 1 or 0, we return x. 

So we are going to show how we can do this, getting simpler and simpler.
'''

def fib0(x):
    '''
    Here, we have a switch dict:

              {_ > 1:(fib0,_-1)+(fib0,_-2),
               'else':_})

    This just means, if x > 1, then return the sum of the function called on x-1 and x-2.
    Otherwise, just return x, which will be 1 or 0.  
    '''
    (x,
     {_ > 1:(fib0,_-1)+(fib0,_-2),
      'else':_})


def fib1(x):
    '''
    Here, however, we use the iff macro.  So for a conditional fArg cond, and a 
    statement, iff(cond,statement) evaluates as:

              {cond:statement,
               'else':_}

    So, we only apply the sum to x if it's above 1.
    '''
    (x,
     iff(_ > 1,(fib1,_-1)+(fib1,_-2)))


def fib2(x):
    '''
    And now, we are even stripping out the pype call, which the compiler can handle.
    '''
    (x,
     iff(_ > 1,(fib2,_-1)+(fib2,_-2)))


def fib3(x):
    '''
    And last but not least, we are enclosing this in a singleton tuple with no 
    reference to x (note the , at the end).  We can do this because the compiler
    infers that _ can only refer to x, since there are no other variables in the
    scope of the function. 
    '''
    iff(_ > 1,(fib3,_-1)+(fib3,_-2)),


'''
pipeify goes through all the previously defined pype funcitons and compiles them.
'''
pypeify_namespace(globals())


if __name__=='__main__':

    print('*'*30)
    print("Welcome to pype's computation of the Fibonnaci sequence!")

    print('*'*30)
    print('running on fib0')

    for x in range(13):

        print(f'fib0({x}) is {fib0(x)}')

    print('*'*30)
    print('running on fib1')

    for x in range(13):

        print(f'fib1({x}) is {fib1(x)}')


    print('*'*30)
    print('running on fib2')

    for x in range(13):

        print(f'fib2({x}) is {fib2(x)}')

    print('*'*30)
    print('running on fib3')
    for x in range(13):

        print(f'fib3({x}) is {fib3(x)}')

