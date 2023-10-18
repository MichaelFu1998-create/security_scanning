def getitem_via_sibseqs(ol,*sibseqs):
    '''
        from elist.elist import *
        y = ['a',['b',["bb"]],'c']
        y[1][1]
        getitem_via_sibseqs(y,1,1)
    '''
    pathlist = list(sibseqs)
    this = ol
    for i in range(0,pathlist.__len__()):
        key = pathlist[i]
        this = this.__getitem__(key)
    return(this)