def indexes_some(ol,value,*seqs):
    '''
        from elist.elist import *
        ol = [1,'a',3,'a',4,'a',5]
        indexes_some(ol,'a',0,2)
        indexes_some(ol,'a',0,1)
        indexes_some(ol,'a',1,2)
        indexes_some(ol,'a',3,4)
    '''
    seqs = list(seqs)
    length = ol.__len__()
    indexes =[]
    seq = -1
    for i in range(0,length):
        if(value == ol[i]):
            seq = seq + 1
            if(seq in seqs):
                indexes.append(i)
            else:
                pass
        else:
            pass
    return(indexes)