def delitem_via_sibseqs(ol,*sibseqs):
    '''
        from elist.elist import *
        y = ['a',['b',["bb"]],'c']
        y[1][1]
        delitem_via_sibseqs(y,1,1)
        y
    '''
    pathlist = list(sibseqs)
    this = ol
    for i in range(0,pathlist.__len__()-1):
        key = pathlist[i]
        this = this.__getitem__(key)
    this.__delitem__(pathlist[-1])
    return(ol)