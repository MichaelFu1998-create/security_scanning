def indexes_all(ol,value):
    '''
        from elist.elist import *
        ol = [1,'a',3,'a',4,'a',5]
        indexes_all(ol,'a')
    '''
    length = ol.__len__()
    indexes =[]
    for i in range(0,length):
        if(value == ol[i]):
            indexes.append(i)
        else:
            pass
    return(indexes)