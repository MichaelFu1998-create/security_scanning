def htmljoin(ol,sp,**kwargs):
    '''
        ol = [1,2,3,4]
        htmljoin(ol,"option",outer="select")
        
    '''
    if('outer' in kwargs):
        outer = kwargs['outer']
    else:
        outer = ""
    if(outer):
        head = "<" + outer + ">"
        tail = "</" + outer + ">"
    else:
        head = ""
        tail = ""
    rslt = head
    length = ol.__len__()
    begin = "<" + sp + ">"
    end = "</" + sp + ">"
    for i in range(0,length):
        rslt = rslt + begin + str(ol[i]) + end
    rslt = rslt + tail
    return(rslt)