'''
python3 linked_list.py

python3 watch_file.py -p1 python3 binary_tree.py -d `pwd`
'''
from pype3 import pypeify_namespace,p,ep,a
from pype3 import _,iff,l,app,_0,_1,_2
from pype3.helpers import *
import pprint as pp

def add_to_tree(tree,value):
    '''
    Fundamental funciton for recursive building of a binary tree.

    ~_:l(value,[],[]),

    If tree is an empty list, build a node as a list of form [value,[],[]].

    value > _0:l(_0,(add_to_tree,_1,value),_2),

    If value is greater than the first element in the node, copy the first
    element in the node, recurse into the left node, and then append 
    the right node.

    value < _0:l(_0,_1,(add_to_tree,_2,value)),

    if value is less than the first element in the node, copy the first 
    element, append the left node node, and recurse into the right node.

    'else':_},

    otherwise, the element already exists in the tree, so return it as-is.
    '''
    ({~_:l(value,[],[]),
      value > _0:l(_0,(add_to_tree,_1,value),_2),
      value < _0:l(_0,_1,(add_to_tree,_2,value)),
      'else':_},
    )


def build_tree(ls):
    '''
    We run a reduce on the collection ls, altering the tree with every
    element.
    '''
    ([(add_to_tree,),[],_],
    )


def find_in_tree(tree,value):
    '''
    This finds a value in a tree.

    ~_:False,

    Either the tree is empty or the node is empty, so value is not in
    in the tree.

    value > _0:(find_in_tree,_1,value),

    Recurse into the left node.

    value < _0:(find_in_tree,_2,value),

    Recurse into the right node.

    'else':True},

    Since value is neither greater than nor less than _0, we know it is
    equal, and we have found our value.
    '''
    ({~_:False,
      value > _0:(find_in_tree,_1,value),
      value < _0:(find_in_tree,_2,value),
      'else':True},
    )


def traverse_tree(tree):
    '''
    We build a flat list from all elements in the tree.

    ~_:[],

    List is empty, return the empty list.

    'else':(traverse_tree,_1) + l(_0) + (traverse_tree,_2),

    Otherwise, return a list built from recursing into the left node,
    followed by a singleton list consisting of _0, followed by a list
    built from recursing into the right node.
    '''
    ({~_:_,
      'else':(traverse_tree,_1) + l(_0) + (traverse_tree,_2),
     },
    )


def reverse_tree(tree):
    '''
    Reverses the binary tree.

    {~_:_,

    Empty list, return it as-is.

    'else':l(_0,(reverse_tree,_2),(reverse_tree,_1)),

    Return a node consisting of _0, followed by the right node switched
    to the left position, and the left node switched to the right 
    position.
    '''
    ({~_:_,
      'else':l(_0,(reverse_tree,_2),(reverse_tree,_1)),
     },
    )


'''
pipeify goes through all the previously defined pype funcitons and compiles them.
'''
pypeify_namespace(globals())


if __name__=='__main__':

    print('*'*30)
    print("Welcome to pype's implementation of a binary tree!")

    binaryTree=build_tree([1,4,8,2,3])

    print('Here is the tree')
    pp.pprint(binaryTree)

    result4=find_in_tree(binaryTree,4)
    result16=find_in_tree(binaryTree,16)

    print('Is 4 in the tree?')
    print(result4)

    print('Is 16 in the tree?')
    print(result16)

    print('Now, we traverse the tree.')
    traverse=traverse_tree(binaryTree)

    print(traverse)

    print('Now, we reverse the tree ...')
    
    reverse=reverse_tree(binaryTree)

    print(reverse)

    traverse=traverse_tree(reverse)

    print('... and we traverse it ...')
    print(traverse)
