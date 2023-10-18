def pathlist_to_getStr(path_list):
    '''
        >>> pathlist_to_getStr([1, '1', 2])
            "[1]['1'][2]"
        >>>
    '''
    t1 = path_list.__repr__()
    t1 = t1.lstrip('[')
    t1 = t1.rstrip(']')
    t2 = t1.split(", ")
    s = ''
    for i in range(0,t2.__len__()):
        s = ''.join((s,'[',t2[i],']'))
    return(s)