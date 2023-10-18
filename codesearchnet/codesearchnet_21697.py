def setitem_via_pathlist(ol,value,pathlist):
    '''
        from elist.elist import *
        y = ['a',['b',["bb"]],'c']
        y[1][1]
        setitem_via_pathlist(y,"500",[1,1])
        y
    '''
    this = ol
    for i in range(0,pathlist.__len__()-1):
        key = pathlist[i]
        this = this.__getitem__(key)
    this.__setitem__(pathlist[-1],value)
    return(ol)