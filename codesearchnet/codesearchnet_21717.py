def is_leaf(obj):
    '''
        the below is for nested-list
        any type is not list will be treated as a leaf
        empty list will be treated as a leaf
        from elist.elist import *
        is_leaf(1)
        is_leaf([1,2,3])
        is_leaf([])
    '''
    if(is_list(obj)):
        length = obj.__len__()
        if(length == 0):
            return(True)
        else:
            return(False)
    else:
        return(True)