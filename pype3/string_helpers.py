import re

def join_st(ls,joiner=' '):
 
    return joiner.join(ls)


def join_lines(ls,num=1):

    jnr='\n'*num

    return jnr.join(ls)


def split_st(st,splitter=' '):

    return str(st).split(splitter)


def split_lines(st):

    return [l for l in str(st).split('\n') if l]


def encase(st,left='(',right=None):

    if right is None:

        right=left

    return f'{left}{st}{right}'


def parens(st):

    return encase(st,'(',')')


def square_bracekts(st):

    return encase(st,'[',']')


def pipes(st):

    return encase(st,'|')


def st_replace(st,replaced,replacer=' '):

    return st.replace(replaced,replacer)


def st_title(st):

    return st.title()


def re_sub(regx,text,rep=''):

    return regx.sub(rep,text)


def quote(st):

    return f'"{st}"'


def re_findall(regx,txt):

    return regx.findall(txt)


STRIP_SPACES=re.compile(r'\s+')

def strip_spaces(st):

    sb=re.sub(r'^\s+','',st)
    sb=re.sub(r'\s+$','',sb)

    return re.sub(r'\s+',' ',sb)


