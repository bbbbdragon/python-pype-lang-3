# Pype3

## Before you begin reading

You can understand the basic syntactic ideas behind pype in the `python-pype-lang-3/tutorial` directory.  To run any script, type the `python3 ...` command in the first docstring.  It is a good idea to tour the language in the following order:

* `mirrors_and_indices.py` - Mirror object, and overloads of arithmetic and Boolean operators, and how to access lists, objects, and dictionaries.
* `callables_and_lambdas.py` - Regular callables and `lambda` structures, which allow you to place variable names where you want them.
* `maps.py` - Examples of maps for flat and embedded dictionaries and lists.
* `filters.py` - Examples of filters for flat and embedded dictionaries and lists.
* `switch_dicts_and_embedded_pypes.py` - Examples of conditionals and embedded pypes.  These two were put into the same category because embedded pypes can define a more sophisticated control flow.
* `dict_and_list_operations.py` - Dictionary/JSON and list manipulations.
* `asigns_closures_and_function_args.py` - How to assign variables inside pype expressions, plus closures and passing functions as arguments.
* `code_with_code.py` - How to use pype closures to build functions in code.  Includes examples of passing functions as arguments, when to use quotes, building complex functions from function arguments, and currying.
* `deep.py` - How to perform maps, reduces, and filters on embedded data structures such as JSON's, using closures.
## What and why?

In the winter of 2017, I was a run-of-the-mill Python Data-Scientist/Code Monkey/Script Kiddie, rocking pandas, scikit-learn, numpy, and scipy.  I began to get bored of Python's imperative style, especially a particularly nasty anti-pattern that appears across many Python scripts and Jupyter notebooks.  What happens is, I'm applying a whole bunch of operations to a single variable:
```
df=pd.read_csv('something.csv')
df=df[columnList]
df.dropna()
...
result=get_result_finally(df)
```
It was then, on a particular NLP-related project, that I discovered Clojure, and its threading ->> macro.  Functional programming was something extremely powerful for me.  I felt as if I switched from a bee-bee gun to an Uzi ... no, a gatling gun.  Before FP, difficult, snarling problems only got angrier as I shot at them.  Now, with the pull of a trigger, they vanished into a peaceful, quiet, red mist.  

But I found another dilemna.  If I wanted to use Clojure, I still needed Python's extremely mature libraries, embedded in microservices that the main Clojure app called through HTTP.  So I started to code functionally in Python.  Here's how pype came about.

To make a long story short, let's say I wanted to implement the following code to find out which age demographic each user was:
```
from collections import defaultdict

ages=[{"name":"bob","age":32},{"name":"susan","age":25},{"name":"joe","age":23},{"name":"mike","age":43}]

agesDct=defaultdict(lambda:list())
agesNames={20:'twenty-somethings',30:'thirty-somethings',40:'fourty-somethings'}

for js in ages:

    name=js['name']
    age=js['age']
    decade=int(age/10)
    ageName=agesNames[decade]
    agesDct[ageName].append(name)
```
Here is how you'd write this in pype:
```
def group_demographic(ages,agesNames):

    ([(ep(_.age, # Get the 'age' value.
          _/10, # divide by 10.
          int, # floor-divide.
          agesNames[_]), # Get the demographic name.
          _.name)], # Iterate through each dict, create a tuple.
     tup_ls_dct, # Create a dictionary with names belonging to each demographic.
    )
```
You may say this is "syntactic sugar".  I hate the expression "syntactic sugar".  Sugar is something you don't need.  Sugar rots your teeth.  Sugar makes you a diabetic.  You sprinkle sugar in your tea at the weekly Princeton University English Department faculty meeting, listening politely to the Dean's passive-aggressive comments about your latest novel.  The metaphor seemed to imply that more concise ways of expressing an idea were bad for you, that if you aren't thinking in terms of "for(int i=0; i <= LENGTH; i++){ ...", you aren't a real programmer.  Here's a little secret - to every programmer, every other programmer is not a real programmer.  We need, collectively, to get over it.

I didn't want "syntactic sugar".  Sugar doesn't change things deeply, make you see things differently.  No, I wanted "syntactic plutonium".    

So I decided to create what I call "pseudo-macros", or "fArgs" - syntactically valid Python expressions which are, in an of themselves, no more than meaningless native Python data structures - lists, tuples, and dictionaries, mostly - but that, when used as arguments to a certain function, perform common FP operations.

This also is why pype can't be called a real programming language.  A pype expression compiles in python, but is then interpreted to run code, so the strategy for interpretation is to examine, with if-thens, the structure and content of the data structure.  Later, I added a just-in-time optimizer which could eventually convert a function returning a pype expression into a function returning the result of a series of native Python expressions, by using AST.   

Pype is distributed under the MIT license.

# Requirements

Pype uses Python3.6 or above.

# Installation

## Using Pip3

You can install pype simply by typing:
```
pip3 install python-pype-lang-3
```
Ensure you are running under root if you do not have proper permissions.  

## From Source

Clone this repo, and cd into `python-pype-lang`.  To install on your local machine, under root, run:

```
cd python-pype-lang-3
pip3 setup.py install
```
To re-install, you will need to run the following script from `python-pype-lang-3`:
```
./reinstall_from_source.sh
```
which will execute, under sudo, the following commands:
```
pip3 uninstall pype
pip3 setup.py install
```
To re-install, you may need to remove the `egg-link` file in your `dist-packages` directory, as root:
```
rm /usr/local/lib/python3.6/dist-packages/pype.egg-link 
```
Now you are ready to test pype in Python3.  Open a file and input the following:
```
from pype import pypeify_namespace,p,_

def say_hello(myName):

    ('Hello ' + _ + ', welcome to pype!',
    )

pypeify_namespace(globals())

if __name__=='__main__':

   print(say_hello('Bennett'))
```
# Examples

Before wading into the documentation, it may be a good idea to look at the `examples` directory to get a feel for how pype really works.  Everything is explained blow-by-blow, and I'd recommend you start programming by copy-pasting some of these examples:

Other examples demonstrate how to implement recursion in pype, and how to build simple microservices in the language, including Machine Learning services:

* `examples/quicksort.py` - recursive quicksort 
* `examples/fibonacci.py` - recursive Fibonacci
* `examples/cyk.py` - A purely functional implementation of the CYK parsing algorithm.
* `examples/cyk_no_docstring.py` - `examples/cyk.py` with the docstrings stripped out to demonstrate pype3's conciseness.
* `examples/data_structures/` - common data structures and algorithms implemented in pype as a POC.

To run any of these files from a command line, just type in the quoted command at the beginning of the file.  For example, `quicksort.py` can be run by typing:
```
python3 quicksort.py
```
# FAQ

* "Is Pype Fast" 

Pype runs as fast as regular Python, because it is.  But also, ask yourself something - you're using Python.  You're not programming microprocessors for toasters in C.  Does it really matter if your program runs in 3 seconds instead of 2?

* "What's wrong with LISP?  What's wrong with Clojure?  What's wrong with Haskell?"

Don't get me wrong, I love these languages.  They're awesome.  But ... try to convince an employer to allow you to use these languages.  With pype, you can say you use Python.  

There is a good LISP library in Python called hy, although seems to have some perfomance issues.  Pype will never be Lisp, ever.  To paraphrase the Zefiro Anejo motto, "hasta el repl, es una obra de arte".  Lisp is a work of art.  Lisp is Mozart.  Use it if you can.  Or use pype.

I think there are three main benefits to using pype over these.  First, you have the richness of Python (pandas, numpy, scikit-learn, various Neural Network libraries) at your fingertips, without having to enclose them in microservices. Second, you can embed pype into any python code you want.  Thirdly, I've found that the expressions for maps, reduces, filters, etc. are actually more concise than many LISP or Clojure expressions.

Why is conciseness valuable?  When you're programing, there's the thought, and there's the code.  Most of programming is going through the mental overhead of translating thought into code.  More verbose languages require more overhead.  But the problem is, you think more slowly, because you try a new idea, translate/implement, try another idea, translate/implement, until you get to the right idea and the right implementation.  And, half the time, your thinking is wrong.  

Because of the implementation's succinctness, debugging pype reduces to two problems - getting the syntax right and getting the thought right.  In other words, it's the difference between thinking for 15 minutes and coding for 18 hours or coding for 30 minutes and thinking for 24 hours.  

* "Is pype readable?"

One way I evaluate a coding style is to write a piece of code and then revisit it several weeks later.  How easy is it to figure out what you're doing?  With C++ or Java, forget it.  I notice when I come back to something written in pype, there's very little overhead trying to re-understand something.

Ask this question for yourself after having done a few projects.  For me, it was yes.


* "Can I build microservices in pype?"

Heck yes you can!  Pype was designed for rapid (and rabid) implementation of microservices.  Since pype excells at transforming JSON's, a routing funciton can simply take the request JSON, make the necessary transformations, and send it back.  When you apply the `optimize` decorator, you'll find that these services are both performant and scalable.  The small Dockerfile lets you Dockerize a service to deploy on AWS Fargate and other production-type server environments.  

By the way, optimized pype and gunicorn are best of friends.  Vote for Pedro.

Examples of pype microservices soon to come.  

* "Can you dynamically generate pype code"

Previously, I remained rather mute on this topic, saying it was theoretically possible.  However, now I am ready to speak - 'yes!' x 1000. There are two ways you can do this.

First, you can write a function that returns a raw pype expression.  `macros.py` are several examples of some code shorthands for common operations.  For example, the `iff(condidtion,expression)` macro returns the evaluated fArg in `expression` if `condition` evaluates as true, otherwise it returns the accum.  You will notice that certain operations, such as list builds have a short macro like `l`.  But if you evaluate them in python, you will find they're much, much uglier:
```
>>> from pype3.macros import *
from pype3.macros import *
>>> from pype3 import _,_0
from pype3 import _,_0
>>> l(4,3)
l(4,3)
['BUILD_LS', 4, 3]
```
We can identify a macro by the fact that it is a Python function call, not an fArg.  During a certain stage in compilation, `l(4,3)` is called as a Python function, which returns `['BUILD_LS', 4, 3]`.  This latter expression is then converted into an Abstract Syntax Tree.

Secondly, you can use closures.  The `code_with_code.py` tutorial will explain to you how to do this, but the general idea is that, when you want a function to build another function, you have the pype expression return a closure as the final argument.  

# Overview

A pype function is a python function ending with a tuple.  Each tuple is an fArg, or an expression which is compiled into Python.  So a typical pype function looks like this:
```
def f(a1,a2,a3...):

    (fArg1,
     fArg2,
     fArg3,
     ...)
``` 
You can also include native Python before the tuple:
```
def f(a1,a2,a3...):

    a1=23

    (fArg1,
     fArg2,
     fArg3,
     ...)
``` 
The grand strategy of a pype function is to apply successive transformations on the "accum".  An accum is the first argument of the function, or the first element of the tuple if it is a native Python expression.  After the second fArg, accum is the result of the previous evaluation.  So in the case of:  
```
def f(a1,a2,a3...):

    (fArg1,
     fArg2,
     fArg3,
     ...)
```
a1 is the accum, and fArg1 is applied to a1, but if:
```
def f(a1,a2,a3...):

    (a2,
     fArg2,
     fArg3,
     ...)
```
then a2 is the accum, and fArg2 is applied to it.

After you have finished defining all your functions, you must include this in the module:
```
pypeify_namespace(globals())
```
This will crawl through the module looking for any function that has a tuple as its final expression.  Using Abstract Syntax Trees (AST's), it will compile the fArgs in the tuple into native Python.

fArgs are the following:

* any Python variable name
* any Python literal
* mirrors - an identity function which returns the accum.
* indices - notation to access elements of iterables.
* maps - Appyling an fArg to each element of an iterable.
* reduces - Taking an iterable, which applies an fArg to update an accumulated value.
* filters - Taking all elements of an iterable which statisfy the conditions.
* lambdas - A shorthand for applying a function to several bound variables and accumulator-specific expressions.
* swtich dicts - Retruns values based on different conditions applied to the accum.
* dictionary operations - Building dictionaries from the accum, adding key-value pairs, deleting keys from dictionaries.
* do expressions - For classes with methods that do not return a value, we can run the code and then return the object.
* list operations - Building lists from the accum, appending items, extending items, concatenation.
* embedded pypes - Specifying pypes within an fArg.
* closures - Declaring pype functions inside pype code.
* assigns - Assigning variables to pype expressions. 

In addition, there are two types of objects, Getter and PypeVal.  These override most operators so that they can be converted into fArgs.  In the latest versions of this, you will not need to worry about these objects, since the compiler takes care of them.

# Pype tuples and accums

A pype tuple is a tuple at the end of a pype function.  This tuple contains fArgs, which perform transforms on the accum.  If the first element of the pype tuple is a native Python expression - a variable name, etc. - then this the accum for the second element of the pype tup;e.  If the first element of the tuple is an fArg, then the accum is the first argument of the function.  

After the first element, the accum is the evaluation returned from the previous element.   
# fArgs

Here we define the fArgs according to a grammar.  We use the following notation:

* `varName` is any legitimate Python variable name.
* `fArg` is any fArg specified below.
* `fArg,+` means "one or more fArgs, seperated by commas".
* `fArg,*` means "zero or more fArgs, seperated by commas".
* `fArg?` means "zero or one fArgs".
* `fArg1`,`fArg2`, etc. refer to the first, second, third fArgs.
* `|` means an OR.
* `<` and `>` bracket an expression, so `<x|y>` means "x or y".
* `hashFArg` means "an fArg which is hashable (not containing a list or dictionary)".
* `callableFArg` means either a Python callable or an fArg which evaluates to a python callable.
* `boolFArg` means "an fArg which is evaluated as a truth value."
* `hashBoolFArg` is an fArg that is both a `boolFArg` and a `hashFArg`.
* `accum` refers to the starting value of a pype function, if the fArg is the first, or the result of the last application of the fArg.
* `expression` refers to a syntactically evaluable Python expression or variable.
* We refer to lists as `[...]`, tuples as `(...)`, and dictionaries as `{...}`.
* We refer to fArgs by their names.
* `<=>` means "functionally equivalent to/gives the same result".

## Callables

A callable is any callable function or callable object in Python3.

~~~~
from pype import pype

add1=lambda x:x+1

def f1(n):

   (add1,
   )

f1(1) <=> 2
~~~~
In certain inconvenient contexts, especially where you have dynamically created a function which the compiler cannot yet see is callable, you may have to convert a function into a lambda.  A macro for this is the `lm` macro:
```
def f2(n):

   ((add1,_),
   )

def f3(n):

   (lm(add1),
   )

f1(1) <=> f2(1) <=> f3(1) <=> 2
```
## Mirrors

`_`

A mirror simply refers to the accum passed to the expression.  It must be explicitly imported from pype, since it overrides the `_` placeholder in Python3.  If you would like to use both, you can import `__`, a double-underscore, but I find the single underscore is much cleaner.

If a mirror is in the first element of the main tuple, it refers to the first argument of the function:

~~~~
from pype import pype,_

def f1(n):
   
   (_,
   )

f1(2) <=> 2

def f2(n,m):
   
   (m,
    _+n,
   )

f2(2,3) <=> 3
~~~~

Mirrors are instances of the `Getter` object, which will be relevant in our discussion of object lambdas and indices.

## Lambdas 

`(<callableFArg>,<expression|fArg>,+)`

Lambdas replace the cumbersome syntax of lambdas in Python3.  The first element of a lambda is a callable or another fArg which evaluates to a callable.  The other elements are arguments to this callable.  If these arguments are fArgs, they are evaluated against the accum:
```
def sm(x,y): return x+y

def f1(n):

    ((sm,_,3),
    )

f1(1) <=> sm(1,3) <=> 5
```
Because fArgs can be used as arguments to lambdas, they can be very expressive:
```
def sm(x,y): return x+y
def mult(x,y): return x*y
def pow2(x): return x**2

def f1(n):

    ((sm,(mult,_,2),(sm,pow2,_+3)),
    )

f1(2) <=> sm(mult(2,2),sm(pow2(2),2+3)) <=> sm(4,sm(4,5)) <=> 13
```

## Index Arg

`<_0|_1|_2|_3|_4|_last>`

If an index arg is defined as `_n`, we access the n-th element of the accum.  The accum must be a list, tuple, or other type of sequence.  n only goes up to 9, and must be explicitly imported:
```
from pype import pype,_0

def f(ls):

    (_0,
    )

f([1,2,3,4,5],_0) <=> [1,2,3,4,5][0] <=> 1
```
The `_last` index arg accesses the last element of the sequence:
```
def f(ls):

    (_0,
    )

f([1,2,3,4,5],_0) <=> [1,2,3,4,5][-1] <=> 5
```

Currently, pype does not allow you to create your own index-arg, and should just be used as a shorthand for often-used list and tuple access expressions.

## Indices

`idx=[<<expression|fArg>+]|.expression|fArg>`
`_idx`

These take a sequence (a list, set or numpy array) or a mapping (dictionary)  as an accum.  If the accum is a sequence, then each `<expression|fArg>` must evaluate to an integer.  If the accum is a mapping, it must evaluate to a key of the mapping:
```
def f1(ls):
    
    (_[0],
    )

f1([1,2,3,4]) <=> [1,2,3,4][0] <=> 1

def f2(js):

    (_['a'],
    )

f2({'a':2,'b;:4}) <=> 2
```
If there are multiple `[<expression|fArg>]`, or if there are multiple bracketed indices, then we evaluate them one at a time:
```
def f1(ls):
    
    (_[0,1],
    )


f1([[1,2,3],[4,5,6]]) <=> [[1,2,3],[4,5,6]][0][1] <=> 2

def f2(ls):
    
    (_[0][1],
    )

f2([[1,2,3],[4,5,6]]) <=> [[1,2,3],[4,5,6]][0][1] <=> 2
```
If the indexed object is a dictionary and the key is not in the dictionary, the expression evaluates as False.  Similarly,
if the indexed object is a list and the index is too high for the list, the expression evaluates as False.  This imitates Clojure's returning nil when an indexed element is not found in a container:
```
def f1(ls):

    (_[3,1],
    )

f1([[1,2,3],[4,5,6]]) <=> [[1,2,3],[4,5,6]][3][1] <=> False

def f2(js):

    (_['c'],
    )

f2({'a':1,'b':2'}) <=> {'a':1,'b':2'}['c'] <=> False 
```
Splices are also available:
```
def f1(ls):
   
   (_[:2],
   )

f1([0,1,2,3]) <=> [0,1,2,3][:2] <=> [0,1]
```
And, fArgs are permitted as arguments to the index as well:
```
def f1(ls):

    (_[len - 1],
    )

f1([1,2,3,4]) <=> 
lenf=PypeVal(len) ls[len(ls) - 1] <=> ls[4 - 1] <=> ls[3] <=> 4
```
You can also use dot notation for more legibility:
```
def f1(js):

    (_.a,
    )

f1({'a':1,'b':2}) <=> {'a':1,'b':2}['a'] <=> 1

def f2(js):

    (_.a.b,
    )

f2({'a':{'b':1,'c':2},'d':2}) <=> {'a':{'b':1,'c':2},'d':2}['a']['b'] <=> {'b':1,'c':2}['b'] <=> 1
```
Also note that indexing is used to access fields of objects:
```
def f1(obj):

    (_.val,
    )

class Obj:
  def __init__(self,val):
    self.val=val
    
f1(Obj(1)) <=> Obj(1).val <=> 1
```
Because the compiler interprets expressions like _[1,0] and _[(1,0)] in the same way, when you want to evaluate a lambda expression inside an index, you will have to wrap it in a tuple:
```
f1(ls):

  (_[tup(add1,_0)], # ls[add1(ls[0])]
  )

f1([1,2,4]) <=> [1,2,4][add1(ls[0])] <=> [1,2,4][add1(1)] <=> [1,2,4][2] <=> 4
```
### Indices and Callables
When the index returns a callable, there are two possibilities.  If the index is the first fArg of a lambda, then the callable is called on the arguments of a lambda:
```
def f1(funcs):

    ((_.sum,1,2),
    )


f1({'sum':sum,'add1':add1}) <=> {'sum':sum,'add1':add1}['sum'](1,2) <=> sum(1,2) <=> 3
```
If the index is not the first fArg of a lambda, the callable will be evaluated on the accum:
```
def add_to_a(dct):
   dct['a']+=1
   return dct

def f1(d):

    (_.add_to_a,
    )
 

d={'add_to_a':add_to_a,'a':1,'b':2}

f1(d) <=> d['add_to_a'](d) <=> {'add_to_a':add_to_a,'a':2,'b':2}
```
This functionality is useful you want to call an object method, and this object method is not in the first position of the lambda, the method gets called on the accum:
```
def f1(obj):

    (_.add1,
    )

class Obj:
  def __init__(self,val):
    self.val=val
  def add1():
    return self.val+1

f1(Obj(1)) <=> 2
```
Or when it is in the first position of a lambda:
```
def f1(obj):

    ((_.add,2),
    )


class Obj:
  def __init__(self,val):
    self.val=val
  def add1():
    return self.val+1
  def add(x):
    return self.val + x
    
f1(Obj(1)) <=> 3
```

## Maps

`[fArg]`

Maps apply apply the fArg to each element in the accum if it is a list, tuple, or other type of sequence, or each value of the accum if it is a dictionary or other type of mapping.

```
def add1(n):
    
    (_+1,
    )

def f1(ls):

    ([add1],
    )

f1([1,2,3]) <=> [add1(1),add1(2),add1(3)] <=> [2,3,4]

f1({3:1,4:2,5:3},[add1]) <=> {3:add1(1),4:add1(2),5:add1(3)} <=> {3:2,4:3,5:4}
```
If you would like to apply a mapping to both the keys and values, you can use the helper function `dct_items` in `pype.helpers`, which gets the items of a dictionary:
```
from pype.helpers import dct_items

def key_value_string(keyValuePair):
  return f'key is {keyValuePair[0]}, value is {keyValuePair[1]}'
  
def d1(js):

    (dct_items,
     [key_value_string],
    )

d1({3:1,4:2,5:3}) <=> ['key is 3, value is 1','key is 4, value is 2','key is 5, value is 3'] 
```
## Reduces

`[(fArg1,),<expression|fArg2>]`
`[(fArg1,),<expression|fArg2>,<expression|fArg3>]`

This is a reduce on an iterable accum.  In the first case `fArg1` is a binary function applied applied to an accumuled value and an element of the accum:
```
def sm(accumulatedValue,element): return accumulatedValue+element

def f1(ls):

    ([(sm,),_],
    )


f1([1,2,3]) <=> 1 + 2 + 3 <=> 6
```
If fArg2 is in the expression, this is evaluated as a starting value for the reduce:
```
def f1(ls):

    ([(sm,),_,10],
    )


f1([1,2,3]) <=> 10 + 1 + 2 + 3 <=> 16
```
fArg1 and fArg2 can be any fArg applied to the accum:
```
def add1(n): return n+1

def f1(ls):

    ([(sm,),[add1],len],
    )


ls=[1,2,3]
f1(ls) <=> len(ls) + add1(1) + add1(2) + add1(3) <=> 3 + 2 + 3 + 4 <=> 12
```
If the accum is a sequence, then `fArg` is applied to the elements of that sequence.  If accum is a mapping, `fArg` is applied to the values of that mapping.
## Filters

`{hashBoolFArg}`

The accum is a sequence or mapping.  If the accum is a sequence, the filter operates on all elements of the sequence, and returns a list.  If it is a mapping, the filter operates on all values of the mapping, and returns a dictionary.

The filter returns all values in the sequence or mapping for which any fArgs can be evaluated as true:
```
def gt1(x): return x>1
def eq0(x): return x == 0

def f1(ls):

    ({gt1},
     {eq0},
    )

ls=[0,-1,2,3,1,9]
f1(ls) <=> [el2 for el2 [el1 for el1 in ls if gt1(el1)] if eq0(el2)] <=> [el for el in ls if el > 1 or el == 0] <=> [0,2,3,9]
```
Note that when there is only one fArg, the expression is equivalent to an AND filter.


## Switch Dicts

`{<hashBoolFArg|expression>:<fArg|expression>,+,'else':<fArg|expression>}`

These implement conditionals.  The switch dict is divided into key-value pairs.  One of these keys must be 'else'.  Each key and value is an fArg.  A switch dict returns the evauation of the value fArg whose corresponding key fArg evaluates to True:
```
def f1(n):

    ({_ == 1:'one',
      _ == 2:'two',
      'else':'no idea'},
    )

f1(1) <=> 'one'
f1(2) <=> 'two'
f1(3) <=> 'no idea'
```
Because Python3.7 orders dictionary keys by insertion, if there are more than one key fArgs which evaluate as True, then the evaluated fArg value for the first key is returned:
```
def f1(n):

    ({_ > 1:'greater than one',
      _ > 2:'greater than two',
      'else':'no idea'},
    )

f1(1) <=> 'no idea'
f1(2) <=> 'greater than two'
f1(3) <=> 'greater than one'
```
### Switch Dict Macros
There are several functions which return a switch dict:
```
iff(cond,expr) => {cond:expr,'else':_}
ift(cond,expr) => {cond:expr,'else':False}
ifp(cond,*fArgs) => {_:ep(*fArgs),'else':_}
iftp(cond,*fArgs) => {cond:ep(*fArgs),'else':False}
```
iff behaves like the logical "if and only if":
```
def f1(n):

    (iff(_>2,_*2),
    )

f1(0) <=> 0
f1(2) <=> 2
f1(3) <=> 6
```
ift is convenient when you want a variable return a False if conditions are not met:
```
def f1(n):

    (ift(_>2,_*2),
    )

f1(0) <=> False
f1(2) <=> False
f1(3) <=> 6
```
ifp and iftp allow multiple fArgs to be executed in an embedded pype:
```
def f1(n):

    (ifp(_>2,_*2,_*100),
    )

f1(0) <=> 0
f1(2) <=> 2
f1(3) <=> 3*2*100 <=> 500

def f2(n):

    (iftp(_>2,_*2,_*100),
    )

f1(0) <=> False
f1(2) <=> False
f1(3) <=> 3*2*100 <=> 500

```
## Do expression

`do(objectCallable)`

This is for instances where objects have methods that change the object, but do not return a value.  `pandas` has a lot of these, such as `dropna`:

```
import pandas as pd
... here df is a pandas dataframe ...
value=df.dropna()

print(value) <=> None
```
So, `do` runs the function and returns the object.  Note that the object must be the accum:
```
def f1(df):

    (do(_.dropna),
    )

f1(df) <=> df after we run dropna on it.
```

## List Build

`l(<expression|fArg>,+)`

This creates a new list, eith either an expression or an evaluated fArg:
```
f1(ls):
    (l(_0+8,_1+10),
    )
    
f1([1,2]) <=> [9,11]
```
These are often used when we want to transform the keys and values of a dictionary, in conjunction with index args, `dct_items` and `tup_dct`, the last of which builds a dictionary from a list of tuples or 2-element lists:
```
from python.helpers import dct_items,tup_dct

def f1(js):

    (dct_items,
     [l(_0+5,_1+10)],
     tup_dct,
    )

f1({1:2,3:4}) <=> {6:20,8:40}
```

## List Append 

`app(<expression|fArg>,+])`

This extends a list with either an expression or an evaluated fArg:
```
from pype import app

def f1(ls):

    (app(3),
    )

f1([1,2]) <=> [1,2,3]
```

## List Concat 

`c([<expression|fArg>,+])`

This concatenates two lists, either expressions or fArgs.

```
from pype import c

def f1(ls):

    (c(_,[3,4]),
    )

f1([1,2]) <=> [1,2,3,4]
```

## Dict Build

`db(<<expression1|fArg1>,<expression2|fArg2>>,*) | {<expression|hashFArg>:<expression|fArg>,+}`

This builds a dictionary.  There are two ways to use the `db(..)` syntax.  First, we can just provide a key:
```
from pype import db

def f1(n):

    (db('n'),
    )

f1(2) <=> {'n':2}
```
Secondly, we can supply a list of fArgs for keys and values, evaluated against the accum:
```
def f1(n):

    (db('a',_+1,'b',_*2,'c',_*10),
    )

f1(2) <=> {'a':3,'b':4,'c':20}
```
If the raw dictionary syntax is used, we must ensure that the dictionary does not contain the key "else", otherwise it will be evaluated as a switch dict:
```
def f1(n):

    ({_+1:_+3,
      _*4:_*3},
    )

f1(2) <=> {2+1:2+3, 2*4:2*3} <=> {3:5, 8:10}
```
## Dict Assoc

`a(<<expression1|fArg1>,<expression2|fArg2>>,+)`

We insert one or more key-value pairs into the accum, where accum is a mapping, in the same way as Dict Build:
```
from pype import a

def f1(js):

    (a('a',4,'b',6),
    )

f1({'c':4}) <=> {'a':4,'b':6,'c':4}
```

## Embedded Dict Assoc
`ea(<<expression1|fArg1>,<expression2|fArg2>>,+)`

This macro allows you to change the values of embedded dictionary expressions.  The first arguments of ea must be the keys of the embedded dictionary, 
and the last argument must be the value:
```
def f1(js,n):

    (ea('a','b','c',n),
    )

js={'a':{'b':{'c':1,'d':8},'e':9}}

f1(js,5) <=> {'a':{'b':{'c':5,'d':8},'e':9}}
```
## Dict Dissoc
`d(<expression|fArg>,+)`

This removes keys specified by `<exppression|fArg>,+` from the accum, which must be a mapping:
```
from pype import d

def f1(js):

    (d('a'),
     d('b'),
    )

f1({'a':1,'b':2,'c':3}) <=> {'c':3}
```


## Dict Merge
`m(<mapping|fArg>)`

This merges a mapping or an fArg that returns a mapping with the accum, which should also be a mapping:
```
from pype import m

def f1(js):

    (m({'b':4}),
    )

f1({'a':2}) <=> {'a':2,'b':4}
```

## Deep Merge
`dm(<mapping|fArg>)`

This does the same thing as a dict merge, except for embedded dicitonaries.  It is syntactic sugar for the following funciton in `pype3/helpers.py`:
```
dct1={'a':{'b':{'c':1},'d':{'e':1,'f':2}},'g':1}
dct2={'a':{'b':{'c':5,'e':6},'d':{'e':2,'f':2}}}

dct_merge_deep(dct1,dct2) <=> {'a': {'b': {'c': 5, 'e': 6}, 'd': {'e': 2, 'f': 2}}, 'g': 1}
```
Notice that {'c':1} becomes {'c': 5, 'e': 6} in the merge.  The existing value
of 'c' was replaced, and a new value 'e' has been added.

The function works according to the following rules:

1) If there is a key-value pair in dct2 that is not in dct1, add that key-value pair to dct1.
2) If there is a key-value pair in dct1 that is in dct2, and both are dictionaries, replace that key-value pair in dct1 with the results of dct_merge_deep for those values.
3) If there is a key-value pair in dct1 that is in dct2, and the values are not dictionaries, the value is the value for dct2.

Here is how it works in pype:
```
from pype import dm

def f1(js):

    (dm({'a':{'b':{'c':5,'e':6},'d':{'e':2,'f':2}}})
    )

f1({'a':{'b':{'c':1},'d':{'e':1,'f':2}},'g':1}) <=> {'a': {'b': {'c': 5, 'e': 6}, 'd': {'e': 2, 'f': 2}}, 'g': 1}
```

## Embedded Pype
`ep(fArg,+)`

This embeds a pype expression in an fArg.  The accum passed to the embedding fArg is also passed to the embedded pype:
```
from pype import ep

def f1(ls):

    ({"number of items greater than 3":ep({_ > 3},
                                          len), 
      "numbers of items less than three":ep({_ < 3},
                                            len)},
    )

f1([1,2,3,4,5,6]) <=> {"number of items greater than 3": 3, "number of itemsless than 3": 2}
```

## Assigns
`varName << <fArg|expression>`

This allows you to declare variables inside a pype tuple.  The benefit of this is that once this variable is declared, you can reference it anywhere below in the tuple.  Let's say, for example, that you wanted to use a dict build to declare a few variables:
```
def f1(n):

    ({'x':_+2,
      'y':_*4,
      'z':_*2},
      _.x+_.y+_.z,
    )

f1(2) <=> 4 + 8 + 4 <=> 16
```
So far, so good.  Now, let's say we wanted to use an ep to add a new value, 'k':
```
def f1(n):

    ({'x':_+2,
      'y':_*4,
      'z':_*2},
      a('k',ep(_.x,_+1,_+1)),
    )
```
Fine, but what happens if we want to multiply the last value in the ep by 'z'?  We just can't do this, because ep can only see 'x' as an accum.  Here is how we would solve this problem:
```
def f1(n):

    (z << _*2,
     {'x':_+2,
      'y':_*4,
      'z':z},
      a('k',ep(_.x,_+1,_+1,_*z)),
    )

```
When we assign a variable, the accum in the next expression is not changed at all.  All this means is that when we refer to this symbol further down in the pype tuple, we have already evaluated it.

## Quotes
`q(callableFArg)`
When you need to pass a callable into another function as an argument, you should use this:
```
from pype3.vals import Quote as q

def f1(n,f2):
   ((f2,_), # f2(n)
   )
   
def f2(n):

   ((f1,_,q(add1)),
   )
   
f2(1) <=> f1(1,add1) <=> add1(1) <=> 1
```
## Closures
`cl(<fArg|expression>,+)|cl([varName,varName,*],<fArg|expression>,+)`

A closure is a way of defining a function within pype code.  It is most frequently used with a lambda.  The first type of closure assumes a single argument, and looks like this:
```
def f1(n):

    (f << cl(add1,add1,add1), # f applies add1 3 times to the argument.
     (f,_), # f(n) <=> add1(add1(add1(n)))   
    )
```
The second type of closure takes a list of arguments of varNames, followed by fArgs.  These do not need to be declared previously - they are the parameters of the closure.  Inside the closure, _ in the first fArg will stand in for the first parameter.
```
def f1(n):

    (f << cl([x,y], # the closure has an x and y as parameters.
             (sm,_,y), # sm(x,y)
             _+1), # sm(x,y)+1
     (f,_,2), # sm(n,2)+1
    )        
```
You can also pass closures into other functions.  This is similar to quotes, except you can define these functions on the fly, similar to how lambdas are used in Python:
```
def f1(n,f2):
 
    (_+f2, # n + f2(n)
    )
    
def f3(n):
 
    ((f1,_,cl(_*8,_+4)), # n + f2(n)
    )
    
f3(2) <=> f1(2,lambda x: x*8+4) <=> 2 + 2*8 + 4 <=> 22
```
However, if you chose to do this, try to include non-callable fArgs in your closure, and use the quote function for callable fArgs.

If you chose to compose closures with functions that are defined in the main function parameters or in a previous assignment, you will need to use them in lambdas - the `lm` macro facilitates this.  This is because the compiler cannot yet see whether a single name is callable or not:
```
def f1(n):
 
    (_*2, # n*2
    )

def f3(n,f1):

    (f3 << cl(f1,_+2), # THIS WILL NOT WORK!
     (f3,_,2), 
    )        

def f3(n,f1):

    (f3 << cl(lm(f1),_+2), # this will
     (f3,_,2), 
    )        

f3(4) <=> (lambda x: f1(x) + 2)(4) <=> f1(4) + 2 <=> 4*2 + 2 <=> 10
```
Finally, you can return closures from pype functions.  The `code_with_code.py` tutorial will give you some pointers on how to do this, but here is an example:
```
def f1(n):

    (_+1,
    )

def f2(n):

    (_*2,
    )

def build_f3(f1,f2):

    (cl(lm(f1) + lm(f2)),
    )
    
build_f3(f1,f2)(2) <=> (lambda x: f1(x) + f2(x))(2) <=> f1(2) + f2(2) <=> (2+1) + (2*2) <=> 3 + 4 <=> 7
```
## Pype Helpers

`pype.helpers` is a module containing many helpful operations on lists and dictionaries.  We have already seen `dct_values` and `tup_dct`, but there are several others that are useful, only a few of which we will cover here (most of the functions are one-liners, so you can just browse the code to learn all of them).

### `tup_ls_dct`

This takes a list of key-value tuples and builds a dictionary of the form `{k1:[el1,..],...}`, where list elements are all values that correspond with a single key:
```
tup_ls_dct([(1,2),(1,3),(4,5),(4,8),(4,9)]) => {1:[2,3],4:[5,8,9]}
```

### `merge_ls_dct(dctLS,key)`

`dctLS` is a list of dictionaries, and `key` is a key that is in all these dictionaries.  It returns an aggregation of the dictionaries by key:
```
merge_ls_dct([{'name':'bobo','payment':20},{'name':'bob','payment':30},{'name':'bob','payment':50},{'name':'susan','payment':10}],'name')
=> {'bobo':[{'name':'bobo','payment':20}],
    'bob':[{'name':'bob','payment':30},{'name':'bob','payment':50}],
    'susan':[{'name':'susan','payment':10}])
```

`merge_ls_dct_no_key` does the same thing, except it deletes the key from the dictionaries.  This is helpful especially when sending out large lists of JSON's via HTTP - where string processing can become a performance bottleneck:
```
merge_ls_dct_no_key([{'name':'bobo','payment':20},
                     {'name':'bob','payment':30},
		     {'name':'bob','payment':50},
		     {'name':'susan','payment':10}],
		     'name')
=> {'bobo':[{'payment':20}],
    'bob':[{'payment':30},{'payment':50}],
    'susan':[{'payment':10}])
```
The usefulness of these two functions becomes more apparent when we show them with pype:
```
from pype import pype
from pype.helpers import merge_ls_dct_no_key

def f1(dctLS):

    ((merge_dct_ls,_,'name'),
     [_['payment']],
    )

dctLS=[{'name':'bobo','payment':20},
       {'name':'bob','payment':30},
       {'name':'bob','payment':50},
       {'name':'susan','payment':10}]
       
f1(dctLs) <=> {'bobo':[20],'bob':[30,50],'susan':[10])
```
### `sort_by_key(ls,key,rev=False)`

This sorts a list of dictionaries by the key provided.  `rev` is just the `reverse` variable in `sorted`:
```
dctLS=[{'name':'bobo','payment':20},
       {'name':'bob','payment':30},
       {'name':'bob','payment':50},
       {'name':'susan','payment':10}]

sort_by_key(dctLS,'payment') <=>
[{'name':'susan','payment':10},
 {'name':'bobo','payment':20},
 {'name':'bob','payment':30},
 {'name':'bob','payment':50}]
```
### `sort_by_index(ls,index,rev=False)`

In this case, `ls` is a list of tuples or lists, and `index` is just an integer for the index:
```
ls=[(1,4),(-1,5),(2,3)]
    
sort_by_index(ls,0) <=> [(-1,5),(1,4),(2,3)]
sort_by_index(ls,1) <=> [(2,3),(1,4),(-1,5)]
```

## Style

I don't know why, but I always found the traditional writing order of Chinese, from top-to-bottom, somehow very beautiful.  Pype reflects this (and perhaps, subconsciously, my admiration for the elegant simplicity of Classical Chinese art), because it encourages you to always separate your fArgs by line:
```
from pype import pype as p

def process_list(ls):
  ([_+1],
   {_ > 2},
   len,
  )
```
The real value of this, though, is that debugging is much easier, because all you need to do is put `#` before each line, and evaluate the expression fArg by fArg.
```
def process_list(ls):
  ([_+1],
   # {_ > 2},
   # len,
  )
```
By the way, while we are on the topic of Chinese writing - in "The Karate Kid", the scrolls for "rule number 1: use karate for defense only, never for attack" actually read, in Chinese, "kong shou wu xian shou", which means, literally, "empty kand (karate) not first hand" - or, "karate is not the first hand".  So much more eloquent and concise than the English.  A pype programmer is an office drone on the outside, theoretically writing in Python.  But, like a martial arts master, although she humbly go through the world and has infinite patience for the fumblings and bloated code of others, she never provokes, she never antagoinzes, but she always leave behind little amounts of virtuous kickassery in a world of wrongness.   

## Feel it? F*ck it ... func it!

By "f*ck it" I mean, in the Big Lubowsky sense, "fuck it ...", "don't worry about it".  The contributors of the pype repository do not in any way encourage innappropriate sexual behavior with your own code.  So don't get any ideas, you pathetic dork.  

Generally, the process of pype programming starts with a large pype expression - in fact, concisely defining program logic is pype's superpower.  As the expression gets longer, you move functionality to other funcitons.  But it's very important to keep each function small, no more than 10-20 lines or so, so you see the entire program logic. 

I do not subscribe to the philosophy of "let the function do its own work", that if a function is only called once, it shouldn't be a function.  That leads to functions that are dozens of lines, which are a nightmare to deal with.  I think a function's primary purpose is to compartmentalize a thought, and expand that thought once you're ready.  The optimizer's upcoming inliner will make remove any performance problems that come from this.

## Scoping
Because the Python interpreter doesn't allow you to refer to unnamed variables, pype doesn't have an equivalent of `let` in Clojure, where you can create scopes on the fly.  To compensate for this I often used dict builds to define an accum which was, in fact, a scope for the succeeding fArg:
```
from pype import pype as p
from pype.val import lenf

def ls_times_itself(ls):
  
  ([_+2],
   {_ < 4},
   {'newLen':lenf*2,
    'ls':_},
   _.ls*_.newLen,
  )
```
Pretty awesome, but be careful - it leads to a lot of bloat.  When you can, define your variables in the function body before the pype expression:
```
from pype import pype as p

def ls_times_itself(ls):
 
 sz=len(ls)*2

 ([_+2],
  {_ < 4},
  _*sz,
 )
```
Much cleaner.  But you could also use pype variable assigns:
```
from pype import pype as p

def ls_times_itself(ls):
 
 (sz << len*2,
  [_+2],
  {_ < 4},
  _*sz,
 )
```
## Mixing Python and Pype
The whole point of Pype is to allow you to program functionally while not having to give up Python's awesome libraries.  So when and where you want, mix mix mix.

For hyper-fast numerical processing, I often find writing functions in imperative numpy or numba and then using pype to define the overall program logic is the most effective.  But I also have a module `numpy_helpers.py` which makes this process easier.

## Loops within loops
[[]] can now be used to run loops on embedded lists or dictionaries:
```
def f1(ls):

    ([[_+1]],
    )

ls=[[1,2,3,3],[2,2]]

f1(ls) <=> [[2,3,4,4],[3,3]]
```
## Immutability

Unfortunately, for performance reasons, we cannot ensure immutability.  This is because many of the dictionary operations act on the original dictionary passed to pype, rather than a copy of it.  Unlike the ultra-light lists and dictionaries of Clojure, Python simply cannot remain performant while creating new dictionaries or lists with every expression.  Therefore, if you are going to call pype more than once on the same data structure, you should use a deepcopy to ensure you are working on the same data.
```
from copy import deepcopy

js1={....}
js2=deepcopy(js1)

val1=some_pype_func(js1)
val2=some_other_pype_func(js2)
```
However, pype's natural habitat is a microservice, so you're going to see/write a lot of code like this:
```
from pype import pype as p
from pype import  db # dict build
from flask import request, jsonify

@app.route('/add',methods=['POST'])
def add():

   (request.get_json(force=True),
    _.numbers,
    sum,
    db('sum'),
    jsonify,
   )  
```
Within the scope of the routing function, you're not going to need a lot of immutability anyway.
# Conclusion

You could do worse.  You probably have.  Use pype.
