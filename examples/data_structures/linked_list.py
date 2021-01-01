'''
python3 linked_list.py

python3 watch_file.py -p1 python3 linked_list.py -d `pwd`
'''
from pype3 import pypeify_namespace,p,ep,a
from pype3 import _,iff,l,app
import pprint as pp

def add_to_ls(linkedList,el):
    '''
    Here, we insert a node at the 'end' element of linkedList.

    node << {'value':el,
              'nxt':None},

    This builds a new node with a null pointer at 'nxt'.

    ~_.ls:{'ls':node,
           'end':node},
    
    If linkedList is not populated, we create two pointers to node, 
    referenced by 'ls' and 'end'.

    'else':a('end',ep(_.end,
                        a('nxt',node),
                        _.nxt))},

    Here, we are taking the 'end' value from linkedList, setting its 'nxt'
    value to node, and setting the 'end' value to that newly-defined 'nxt'
    value.  The a(...) statement assures that the function returns 
    linkedList.
    '''
    (node << {'value':el,
              'nxt':None},
     {~_.ls:{'ls':node,
             'end':node},
      'else':a('end',ep(_.end,
                        a('nxt',node),
                        _.nxt))},
     
    )


def build_list(els,linkedList=None):
    '''
    Run a reduce on els to build the list.
    '''
    ([(add_to_ls,),linkedList,_],
    )

      
def traverse_list(linkedList,els=[]):
    '''
    Traverse the list.

    nxt << _.nxt,
    value << _.value,

    If we are at the top of the data structure, these will be defined
    as False, but will also not be used.  Otherwise, they maintain the
    next item or the value.

    {_.ls:(extract_elements,_.ls),

    If we are at the top of the data structure, we will find the key 'ls',
    so we re-run the function on 'ls'.

    'else':ep(els,
              app(value),
              {nxt:(extract_elements,nxt,_),
               'else':_})},

    Otherwise, we take els, append value, and then see if nxt is None or
    not.  If not, then we run the function on nxt and the accumulator els.
    If it is, we just return the modified els.
    '''
    (nxt << _.nxt,
     value << _.value,
     {_.ls:(extract_elements,_.ls),
      'else':ep(els,
                app(value),
                {nxt:(extract_elements,nxt,_),
                 'else':_})},
    )


     
'''
pipeify goes through all the previously defined pype funcitons and compiles them.
'''
pypeify_namespace(globals())


if __name__=='__main__':

    print('*'*30)
    print("Welcome to pype's computation of a linked list!")

    linkedList=build_list([1,2,3,4])

    pp.pprint(linkedList)

    # elements=extract_elements(linkedList)

    # pp.pprint(elements)
