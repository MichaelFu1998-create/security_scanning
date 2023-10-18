def index_whichnot(ol,value,which):
    '''
        from elist.elist import *
        ol = [1,'a',3,'a',4,'a',5]
        index_whichnot(ol,'a',0)
        index_whichnot(ol,'a',1)
        index_whichnot(ol,'a',2)
    '''
    length = ol.__len__()
    seq = -1
    for i in range(0,length):
        if(value == ol[i]):
            pass
        else:
            seq = seq + 1
            if(seq == which):
                return(i)
            else:
                pass
    return(None)