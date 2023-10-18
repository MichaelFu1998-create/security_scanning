def delitem_via_pathlist(ol,pathlist):
    '''
        from elist.elist import *
        y = ['a',['b',["bb"]],'c']
        y[1][1]
        delitem_via_pathlist(y,[1,1])
        y
    '''
    this = ol
    for i in range(0,pathlist.__len__()-1):
        key = pathlist[i]
        this = this.__getitem__(key)
    this.__delitem__(pathlist[-1])
    return(ol)