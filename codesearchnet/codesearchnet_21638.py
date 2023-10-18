def index_lastnot(ol,value):
    '''
        from elist.elist import *
        ol = [1,'a',3,'a',4,'a',5]
        index_lastnot(ol,'a')
        ####lastIndexOfnot is the same as index_lastnot
        lastIndexOfnot(ol,'a')
    '''
    length = ol.__len__()
    for i in range(length-1,-1,-1):
        if(value == ol[i]):
            pass
        else:
            return(i)
    return(None)