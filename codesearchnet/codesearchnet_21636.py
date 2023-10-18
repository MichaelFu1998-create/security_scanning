def index_firstnot(ol,value):
    '''
        from elist.elist import *
        ol = [1,'a',3,'a',4,'a',5]
        index_firstnot(ol,'a')
        ####index_firstnot, array_indexnot, indexOfnot  are the same
        array_indexnot(ol,'a')
        indexOfnot(ol,'a')
    '''
    length = ol.__len__()
    for i in range(0,length):
        if(value == ol[i]):
            pass
        else:
            return(i)
    return(None)