def last_continuous_indexes_slice(ol,value):
    '''
        from elist.elist import *
        ol = [1,"a","a",2,3,"a",4,"a","a","a",5]
        last_continuous_indexes_slice(ol,"a")
    '''
    length = ol.__len__()
    end = None
    slice = []
    for i in range(length-1,-1,-1):
        if(ol[i]==value):
            end = i
            break
        else:
            pass
    if(end == None):
        return(None)
    else:
        slice.append(end)
        for i in range(end-1,-1,-1):
            if(ol[i]==value):
                slice.append(i)
            else:
                break
    slice.reverse()
    return(slice)