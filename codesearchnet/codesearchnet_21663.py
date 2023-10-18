def copy_within(ol,target, start=None, end=None):
    '''
        from elist.elist import *
        ol = [1, 2, 3, 4, 5]
        id(ol)
        rslt = copyWithin(ol,0,3,4)
        rslt
        id(rslt)
        ####
        ol = [1, 2, 3, 4, 5]
        id(ol)
        rslt = copyWithin(ol,0,3)
        rslt
        id(rslt)
        ####
        ol = [1, 2, 3, 4, 5]
        id(ol)
        rslt = copyWithin(ol,-2)
        rslt
        id(rslt)
        ####copyWithin is the same as copy_within
    '''
    length = ol.__len__()
    if(start==None):
        start = 0
    else:
        pass
    if(end==None):
        end = length
    else:
        pass
    target = uniform_index(target,length)
    start = uniform_index(start,length)
    end = uniform_index(end,length)
    cplen = end - start
    cpend = target+cplen
    if(target+cplen > length):
        cpend = length
    else:
        pass
    shift = start - target
    if(shift>=0):
        for i in range(target,cpend):
            ol[i] = ol[i+shift]
    else:
        for i in range(cpend-1,target-1,-1):
            ol[i] = ol[i+shift]
    return(ol)