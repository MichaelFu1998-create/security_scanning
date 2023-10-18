def first_continuous_indexesnot_slice(ol,value):
    '''
        from elist.elist import *
        ol = ["a",0,1,"a","a",2,3,"a",4,"a","a","a",5]
        first_continuous_indexesnot_slice(ol,"a")
    '''
    length = ol.__len__()
    begin = None
    slice = []
    for i in range(0,length):
        if(not(ol[i]==value)):
            begin = i
            break
        else:
            pass
    if(begin == None):
        return(None)
    else:
        slice.append(begin)
        for i in range(begin+1,length):
            if(not(ol[i]==value)):
                slice.append(i)
            else:
                break
    return(slice)