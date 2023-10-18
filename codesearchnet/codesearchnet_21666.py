def entries(ol):
    '''
        from elist.elist import *
        ol = ['a','b','c']
        rslt = entries(ol)
        rslt
    '''
    rslt = []
    length = ol.__len__()
    for i in range(0,length):
        entry = [i,ol[i]]
        rslt.append(entry)
    return(rslt)