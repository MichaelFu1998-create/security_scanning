def broken_seqs(ol,break_points):
    '''
        ol = initRange(0,20,1)
        ol
        break_points = [1,6,14,9]
        secs = broken_seqs(ol,break_points)
        forEach(secs,print)
    '''
    bps = list(break_points)
    length = ol.__len__()
    rgs = rangize(bps,length)
    rslt = []
    for i in range(0,rgs.__len__()):
        si,ei = rgs[i]
        sec = ol[si:ei]
        rslt.append(sec)
    return(rslt)