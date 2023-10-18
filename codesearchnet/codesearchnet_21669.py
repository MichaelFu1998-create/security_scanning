def join(ol,separator=","):
    '''
        from elist.elist import *
        ol = [1,2,3,4]
        join(ol,separator="-")
    '''
    if(ol.__len__() == 0):
        return("")
    else:
        pass
    cond = (type(ol[0])==type(b''))
    if(cond):
        rslt = b''
    else:
        rslt =""
    length = ol.__len__()
    for i in range(0,length-1):
        ele = ol[i]
        if(cond):
            pass
        else:
            ele = str(ele)
        rslt = rslt + ele + separator
    if(cond):
        rslt = rslt + ol[length - 1]
    else:
        rslt = rslt + str(ol[length - 1])
    return(rslt)