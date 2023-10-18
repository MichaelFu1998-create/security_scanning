def index_last(ol,value):
    '''
        from elist.elist import *
        ol = [1,'a',3,'a',4,'a',5]
        index_last(ol,'a')
        ####lastIndexOf is the same as index_last
        lastIndexOf(ol,'a')
    '''
    length = ol.__len__()
    for i in range(length-1,-1,-1):
        if(value == ol[i]):
            return(i)
        else:
            pass
    return(None)