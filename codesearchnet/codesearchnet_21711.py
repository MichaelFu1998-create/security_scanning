def brkl2kvlist(arr,interval,sub_pos=1,**kwargs):
    '''
        arr = ["color1","r1","g1","b1","a1","color2","r2","g2","b2","a2"]
        brkl2kvlist(arr,5)
        (['color1', 'color2'], [['r1', 'g1', 'b1', 'a1'], ['r2', 'g2', 'b2', 'a2']])
        brkl2kvlist(arr,5,2)
        ([['color1', 'r1'], ['color2', 'r2']], [['g1', 'b1', 'a1'], ['g2', 'b2', 'a2']])
    '''
    lngth = arr.__len__()
    brkseqs1 = init_range(0,lngth,interval)
    brkseqs2 = init_range(sub_pos,lngth,interval)
    brkseqs = interleave(brkseqs1,brkseqs2)
    l = broken_seqs(arr,brkseqs)
    kl = select_evens(l)
    vl = select_odds(l)
    if("single_key" in kwargs):
        single_key = kwargs['single_key']
    else:
        single_key = True
    if(sub_pos == 1):
        if(single_key):
            kl = mapv(kl,lambda ele:ele[0])
        else:
            pass
    else:
        pass
    return((kl,vl))