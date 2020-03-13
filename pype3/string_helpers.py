def join_st(ls,joiner=' '):
 
    return joiner.join(ls)


def split_st(st,splitter=' '):

    return str(st).split(splitter)


def str_replace(st,replaced,replacer=' '):

    return st.replace(replaced,replacer)


def re_sub(regx,text,rep=''):

    return regx.sub(rep,text)
