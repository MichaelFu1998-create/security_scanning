def divide(ol,interval):
    '''
        ol = elel.initRange(0,20,1)
        interval = 3
        rslt = elel.divide(ol,interval)
        rslt
        rslt = elel.divide(ol,4)
        rslt
    '''
    length = ol.__len__()
    seqs = initRange(0,length,interval)
    rslt = broken_seqs(ol,seqs)
    return(rslt)