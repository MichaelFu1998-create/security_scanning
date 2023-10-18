def join2(ol,*sps):
    '''
        from elist.elist import *
        ol = [1,2,3,4]
        join2(ol,"-","+","*")
    '''
    rslt =""
    length = ol.__len__()
    for i in range(0,length-1):
        rslt = rslt + str(ol[i]) + sps[i]
    rslt = rslt + str(ol[length - 1])
    return(rslt)