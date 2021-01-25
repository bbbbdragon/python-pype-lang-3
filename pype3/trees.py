'''
python3 trees.py
'''
py_slice=slice
from pype3.fargs import *
from pype3.type_checking import *
from pype3.build_helpers import *
from pype3.nodes import *
from pype3.vals import delam,is_bookmark,NameBookmark
from itertools import groupby
from functools import reduce
from inspect import getsource
from ast import *
import ast
import numpy as np
import pprint as pp
import astpretty
from copy import deepcopy
'''
This module contains the AST tree transformations necessary to run the optimizer.
'''
###########
# HELPERS #
###########

def has_pype_call(node,aliases):

    if isinstance(node,Return):

        return has_pype_call(node.value,aliases)

    if isinstance(node,Call):

        return has_pype_call(node.func,aliases)

    if isinstance(node,Name):

        return node.id in aliases

    if isinstance(node,Attribute):

        return node.attr in aliases

    return False


def is_pype_return(node,aliases):

    if is_list(node):

        node=node[-1]

    # print('is_pype_return')
    # print(ast.dump(node))

    return isinstance(node,Return) and has_pype_call(node,aliases)


def is_name_bookmark(node):

    return isinstance(node,Call) \
        and isinstance(node.func,Attribute) \
        and node.func.attr=='NameBookmark'


def pype_return_f_args(accum,*fArgs):
    '''
    FArgs is a tuple, but we want it to be a list - it's just neater.
    '''
    return list(fArgs)


def is_final_tuple(lastNode):

    return isinstance(lastNode,Expr) and isinstance(lastNode.value,Tuple)


#####################
# NO ACCUM REPLACER #
#####################

def tup_expr_node(elements):

    return Expr(value=Tuple(elts=elements,ctx=Load),ctx=Load())


class NoAccumReplacer(NodeVisitor):
    '''
    This is for when there is only one argument to the function, there are no variables
    defined in the function body, there is no return or pype call in the final funciton,
    and the final expression is either a tuple or a single variable whose first element
    is an fArg, like this:

    def add1(x):

        _+1,

    Or, this:

    def add1Mult3(x):

        _+1,
        _*3,

    The strategy is:

    1) If the final expression is a tuple, build a new tuple containing the argument
    first, and then the rest of the elements of that tuple.  This can then be 
    transformed by the NoReturnReplacer into a proper pype statement.

    2) If the final expression is not a tuple, not a pype return, and not a pype call,
    then it is a single fArg.  So we build a new tuple with the argument as the first
    element, and the fArg as the second.  Again, this is consumable by 
    NoReturnReplacer.

    TODO: Update documentation to exclude body length == 1 constraint.
    '''
    def __init__(self,aliases):

        self.aliases=aliases

    def visit_FunctionDef(self,node):

        args=node.args.args
        body=node.body
        lastNode=body[-1]

        '''
        if is_final_tuple(lastNode) and len(body) > 1:

            raise Exception(f'Function body {[ast.dump(n) for n in body]} cannot '
                            'have anything but returned tuples if you are going to not '
                            'include an itial accum.')
        '''

        # print('no_accum_replacer')
        # print([ast.dump(el) for el in body])
        # print(f'{ast.dump(lastNode)} is lastNode')
        # print(f'{is_final_tuple(lastNode)} is final tuple')

        # First, there can only be one args to the function.  Took out the lenght
        # constraint because docstrings lengthen the function.  
        if True:#len(args) == 1: #and len(body) == 1:

            # print('args and body length 1')

            # Let's grab the name of the one argument, and wrap it in a Name object.
            headArg=args[0].arg
            headArgName=Name(id=headArg,
                             ctx=Load())

            # Now, what do we do with this?  It depends on whether the last expression
            # is a tuple, thus containing multiple fArgs, or a raw expression, 
            # containing only one fArg.
            if is_final_tuple(lastNode):

                # print('is final tuple')

                # Get the elements from the tuple. lastNode is an Expr object with
                # a value field.  
                elements=lastNode.value.elts
                firstElement=elements[0]

                # print(f'{isinstance(firstElement,Name)} is firstElement is name')

                # Is the firstElement a name identical to that of the only argument?
                # No?  Then we insert the name of the head argument into the tuple.
                if not (isinstance(firstElement,Name) and firstElement.id == headArg):

                    node.body[-1]=tup_expr_node([headArgName]+elements)

            # Otherwise, is it a single fArg expression?  Then we turn it into 
            # a tuple with headArgName as the first element and lastNode as the 
            # second.
            # Actually we can't do this, its syntactically ambiguous with a lambda.
            # Sorry!
            '''
            elif not is_final_pype_call(lastNode,self.aliases) \
                 and not is_pype_return(node.body,self.aliases):

                print('is single expression')
                print(ast.dump(lastNode))

                if isinstance(lastNode,Expr):

                    lastNode=lastNode.value

                node.body[-1]=tup_expr_node([headArgName,lastNode])
            '''
        node=fix_missing_locations(node)
        node.decorator_list=[]

        self.generic_visit(node)


######################
# NO RETURN REPLACER #
######################

def is_final_pype_call(lastNode,aliases):

    return isinstance(lastNode,Expr) and has_pype_call(lastNode.value,aliases)


class NoReturnReplacer(NodeVisitor):
    '''
    If the function ends with a pype call, but no 'return', then we put in a return.
    This helps with conciseness, since 'return' takes up a lot of uneccessary 
    space.
    '''
    def __init__(self,aliases):

        self.aliases=aliases

    def visit_FunctionDef(self,node):

        # print(f'in functionDef')

        args=node.args.args
        body=node.body
        lastNode=body[-1]

        # print(f'{body} is body')
        # print(f'{ast.dump(lastNode)} is lastNode')
        
        if is_final_pype_call(lastNode,self.aliases):

            # print('is_final_pype_call')

            returnNode=Return(value=lastNode.value)
            node.body[-1]=returnNode
        
        elif is_final_tuple(lastNode):

            # print('is_final_tuple')

            elements=lastNode.value.elts
            node.body[-1]=Return(value=pype_call_node(elements))

        node=fix_missing_locations(node)
        node.decorator_list=[]

        self.generic_visit(node)


#####################
# PYPE VAL REPLACER #
#####################

class PypeValReplacer(NodeVisitor):
    '''
    This finds any instance of a binop in the parse tree, and replaces the first 
    element with a PypeVal for that element.  This allows us to get rid of explicit
    PypeVal declarations in optimized code, so instead of v(len)+1 you can now just
    do len + 1, but again, only in optimized code.

    Because of how delam works, this does not create a problem for the NameBookmarks
    since PypeVals are delam-ed recursively, so v(v(v(1))) evaluates as 1, and
    v(NameBookmark("a")) evaluates as NameBookmark("a").
    '''
    def visit_compare_or_binop(self,node,leftNode,rightNode):

        if not (is_name_bookmark(leftNode) and is_name_bookmark(rightNode)):
        
            newLeftNode=Call(func=Attribute(value=PYPE_VALS_NODE,
                                            attr='PypeVal',
                                            ctx=Load()),
                             args=[leftNode], 
                             keywords=[])
            node.left=newLeftNode
            node.decorator_list=[]
            node=fix_missing_locations(node)

        return node


    def visit_Compare(self,node):

        leftNode=node.left
        rightNode=node.comparators[0]

        node=self.visit_compare_or_binop(node,leftNode,rightNode)
        
        self.generic_visit(node)
       
 
    def visit_BinOp(self,node):

        leftNode=node.left
        rightNode=node.right

        node=self.visit_compare_or_binop(node,leftNode,rightNode)

        self.generic_visit(node)
       

##################
# NAME REPLACERS # 
##################

class NameReplacer(NodeTransformer):
    '''
    This finds any name and converts it into a NameBookmark object, so when the fArgs
    are returned by pype_return_fargs, they contain NameBookmark objects.
    '''
    def visit_Name(self,node):

        self.generic_visit(node)

        newNode=node
        name=node.id
        newNode=Call(func=Attribute(value=PYPE_VALS_NODE,
                                    attr='NameBookmark',
                                    ctx=Load()),
                     args=[Str(s=name)], 
                     keywords=[])
            
        return newNode



class NameReplacerNameSpace(NodeTransformer):
    '''
    This finds any name and converts it into a NameBookmark object when it is in the 
    scope of the function, so when the fArgs returned by pype_return_fargs, they 
    contain NameBookmark objects.
    '''
    def __init__(self,nameSpace=set([])):

        self.nameSpace=set([el for el in nameSpace])


    def visit_Name(self,node):

        self.generic_visit(node)

        newNode=node

        if node.id in self.nameSpace:

            name=node.id
            newNode=Call(func=Attribute(value=PYPE_VALS_NODE,
                                        attr='NameBookmark',
                                        ctx=Load()),
                         args=[Str(s=name)], 
                         keywords=[])
            
        return newNode


##########################
# CLOSURE NAME REPLACERS #
##########################

class ClosureNameReplacer(NodeTransformer):
    '''
    This applies the NameBookmark to closure nodes.
    '''
    def visit_Call(self,node):

        self.generic_visit(node)

        # print(f'{ast.dump(node)} is node before')

        newNode=deepcopy(node)
        
        if (isinstance(node.func,Name) \
            and node.func.id == 'cl' \
            and isinstance(node.args[0],List)):
 
            closureNameSpace=[]
            
            get_body_names(node.args[0],closureNameSpace)

            # print(f'{closureNameSpace} is closureNameSpace')

            newNode=NameReplacerNameSpace(closureNameSpace).visit(newNode)

        # print(f'{ast.dump(newNode)} is node after')

        return newNode
            

###########################
# ASSIGN NAMESPACE FINDER #
###########################

class AssignNameSpaceFinder(NodeVisitor):
    '''
    This specifically craws an fArg node and looks for any assignment operators.
    When it finds one, it adds the assigned-to name to the namespace.
    '''
    def __init__(self,nameSpace):

        self.nameSpace=nameSpace

    def visit_BinOp(self,node):

        if isinstance(node.op,LShift):
            
            leftNodeName=node.left.id

            self.nameSpace.add(leftNodeName)

        self.generic_visit(node)


######################
# CALL NAME REPLACER #
######################

def get_body_names(el,names=[]):
    '''
    Recursively retrieve names from function body.
    '''
    if is_list(el):

        for v in el:

            get_body_names(v,names)

    elif isinstance(el,List):

        elts=el.elts

        for el in elts:

            get_body_names(el,names)

    elif isinstance(el,Assign):

        targets=el.targets
        
        for target in targets:

            get_body_names(target,names)

    elif isinstance(el,Name):

        names.append(el.id)

    elif isinstance(el,Tuple):

        for v in el.elts:

            get_body_names(v,names)


def pype_return_f_args(accum,*fArgs):
    '''
    FArgs is a tuple, but we want it to be a list - it's just neater.
    '''
    return list(fArgs)


IMPORT_OPTIMIZE=ImportFrom(module='pype', 
                           names=[alias(name='optimize', asname=None)], 
                           level=0)
PYPE_RETURN_F_ARGS=Attribute(value=Name(id='optimize',ctx=Load()),
                             attr='pype_return_f_args',
                             ctx=Load())



class NameBookmarkReplacer(NodeVisitor):
    '''
    This class changes any variable in the local namespace into a NameBookmark object, 
    so it is not evaluated by the interpreter as a specific value.  This NameBookmark 
    object is later converted into a Name object.

    I chose the NameBookmark strategy because the simultaneous iteration-mapping
    of fArg elements with nodes on the tree doesn't support pype macros such as 
    _if.  So you'd have to right a simultaneous traversal for each macro.  Instead
    I evaluate the macros with pype_return_f_args, and then parse the fArgs directly
    without any reference to the original tree.

    To illustrate this, let's say we have a macro which is:

    def _if(condition,result):

      return {condition:result,
              'else':_}

    In the call:

    y=2

    return p(x,_if(_ > 2,_+y))

    Under the old pair-traversal strategy, I'd get a parse of the _if statement, 
    and I would need to write both a fArg-to-tree conversion and a replace-name 
    conversion for this particular case.  This is messy and leads to a lot of
    code bloat.

    So here, we replace the call with a function that returns:

    [{_ > 2: _ + NameBookmark('y'),
      'else':_}]

    When the fArg parser finds a NameBookmark object, it replaces it with a Name
    object.  
    '''
    def __init__(self,aliases):

        self.pypeAliases=aliases
        self.nameSpace=set()
        self.accumNode=None

    def visit_FunctionDef(self,node):
        '''
        We are at the function definition.  First, we update the namesSpace
        with all local variables.  This means that using global constants isn't
        permitted in the optimizer - you have to explicitly put them in the 
        function scope.
        '''
        bodyNames=[]
        get_body_names(node.body,bodyNames)
        #print(f'{bodyNames} is bodyNames')
        #bodyNames=[target.id for line in node.body if isinstance(line,Assign) \
        #             for target in line.targets]
        argNames=[arg.arg for arg in node.args.args]
        self.nameSpace|=set(bodyNames+argNames)

        '''
        Is there a pype return at the end of the function definition?

        TODO - Remove IMPORT_OPTIMIZE and PYPE_RETURN_F_ARGS because p() already
        returns fArgs.  
        TODO - Change object name from CallNameReplacer to NameBookmarkReplacer.
        TODO - do this for all pype calls inside a function, which means the 
        accum-assign strategy needs to be replaced.
        '''
        # print(f'{self.pypeAliases} is pype aliases')
        if is_pype_return(node.body,self.pypeAliases):
            # Set the accum node
            self.accumNode=node.body[-1].value.args[0]
            # Insert an import of pype.optimize into the node body.
            # node.body=[IMPORT_OPTIMIZE]+node.body
            # Change the function call from pype to pype_return_f_args, which only
            # returns the fArgs.
            # node.body[-1].value.func=PYPE_RETURN_F_ARGS

            fArgsNodes=node.body[-1].value.args[1:]
            newFArgsNodes=[]

            for fArgNode in fArgsNodes:

                # Look for any new assigned variables, add them to the nameSpace.
                assignFinder=AssignNameSpaceFinder(self.nameSpace)
                
                assignFinder.visit(fArgNode)

                self.nameSpace|=assignFinder.nameSpace

                # Then, replace them as NameBookmarks.

                replacedNode=NameReplacerNameSpace(self.nameSpace).visit(fArgNode)

                # Now we are going to look into closures that contain arguments.

                replacedNode=ClosureNameReplacer().visit(replacedNode)

                newFArgsNodes.append(replacedNode)

            # The new fArgsNodes have NameBookmark anywhere there is a local variable
            # referenced.  So we replace the fArgs in the function body with this.
            node.body[-1].value.args[1:]=newFArgsNodes

        node.decorator_list=[]
        node=fix_missing_locations(node)

        self.generic_visit(node)

#################
# KwargsReplacer #
#################

class KwargsReplacer(NodeVisitor):

    def __init__(self,aliases):

        self.pypeAliases=aliases
    
    def visit_FunctionDef(self,node):

        if is_pype_return(node.body,self.pypeAliases):

            fArgsNodes=node.body[-1].value.args[1:]
            newFArgsNodes=[]

            for fArgNode in fArgsNodes:

                if isinstance(fArgNode,Starred):

                    newNode=Call(func=Attribute(value=PYPE_VALS_NODE,
                                                attr='KwargsBookmark',
                                        ctx=Load()),
                         args=[fArgNode.value],  
                         keywords=[])

                    newFArgsNodes.append(newNode)

                else:

                    newFArgsNodes.append(fArgNode)
            
            node.body[-1].value.args[1:]=newFArgsNodes

        node.decorator_list=[]
        node=fix_missing_locations(node)

        self.generic_visit(node)


#################
# FARG REPLACER #
#################

class FArgReplacer(NodeVisitor):
    '''
    This takes a series of sub-trees in fArgAssigns and the original parse tree.
    It then applies these assignments to the function return.

    TODO - get rid of the accum assigns.
    '''
    def __init__(self,fArgAssigns,aliases):

        self.fArgAssigns=fArgAssigns
        self.pypeAliases=aliases

    def visit_FunctionDef(self,node):

        if is_pype_return(node.body,self.pypeAliases):
        
            # Whereas originally node.body[-1] just contains the return,
            # now we replace it with the funciton body up to the return,
            # plus the accum assigns, plus the return accum.
            node.body=node.body[:-1]+self.fArgAssigns+RETURN_ACCUM

        node.decorator_list=[]
        node=fix_missing_locations(node)

        self.generic_visit(node)


############################
# FIND IF IS PYPE FUNCTION #
############################

class PypeReturnFinder(NodeVisitor):
    '''
    This takes a series of sub-trees in fArgAssigns and the original parse tree.
    It then applies these assignments to the function return.

    TODO - get rid of the accum assigns.
    '''
    def __init__(self,aliases):

        self.aliases=aliases
        self.isReturn=False

    def visit_FunctionDef(self,node):

        if node.body:

            lastNode=node.body[-1]

            # print('in pype return')
            # print(f'{ast.dump(lastNode)} is lastNode')

            self.isReturn|=is_pype_return(lastNode,self.aliases)
            self.isReturn|=is_final_pype_call(lastNode,self.aliases)
            self.isReturn|=is_final_tuple(lastNode)
            
            # if self.isReturn:

                # print(f'{self.isReturn} is pype return')


        self.generic_visit(node)


def is_pype_function(f,aliases):

    try:

        if not is_callable(f):

            return False

        pypeReturnFinder=PypeReturnFinder(aliases)
        src=getsource(f)
        tree=ast.parse(src)
        
        pypeReturnFinder.visit(tree)
        
        return pypeReturnFinder.isReturn

    except Exception as e:

        return False

    return False


################################
# FIND IF THERE IS A DECORATOR #
################################

class PypeDecoratorFinder(NodeVisitor):
    '''
    This takes a series of sub-trees in fArgAssigns and the original parse tree.
    It then applies these assignments to the function return.

    TODO - get rid of the accum assigns.
    '''
    def __init__(self):

        self.hasDecorator=False

    def visit_FunctionDef(self,node):

        for decorator in node.decorator_list:

            # print(f'{ast.dump(decorator)} is decorator')

            self.hasDecorator|=(isinstance(decorator,Call) and \
                                isinstance(decorator.func,Name) and \
                                decorator.func.id=='pypeify')

        self.generic_visit(node)


def is_pype_decorated_function(f):

    try:

        decoratorFinder=PypeDecoratorFinder()
        src=getsource(f)
        tree=ast.parse(src)
        
        decoratorFinder.visit(tree)

        return decoratorFinder.hasDecorator

    except Exception as e:

        return False

    return False
