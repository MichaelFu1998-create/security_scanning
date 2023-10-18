def insert_sections_many(ol,secs,locs,**kwargs):
    '''
        ol = initRange(0,20,1)
        ol
        locs = [1,6,14,9]
        secs = [
            ['a','a','a'],
            ['b','b'],
            ['c','c','c','c'],
            ['d','d']
        ]
        rslt = insert_sections_many(ol,secs,locs)
        rslt
        ####
        ol
        locs = [0,3,6,9,12,15,16]
        secs = [
            ['a','a','a'],
            ['b','b'],
            ['c','c','c','c'],
            ['d','d']
        ]
        rslt = insert_sections_many(ol,secs,locs)
        rslt
        ####
        ol
        locs = [1,6,14,9]
        secs = [
            ['a','a','a'],
            ['b','b'],
            ['c','c','c','c'],
            ['d','d'],
            ['e'],
            ['f','f','f','f'],
            [777,777,777,777]
        ]
        rslt = insert_sections_many(ol,secs,locs)
        rslt
    '''
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    secs = copy.deepcopy(secs)
    locs = copy.deepcopy(locs)
    brked = broken_seqs(ol,locs)
    seclen = secs.__len__()
    brklen = brked.__len__()
    if(locs[0]==0):
        new = secs[0]
        length = seclen -1
        if(length < brklen):
            for i in range(0,length):
                new.extend(brked[i])
                new.extend(secs[i+1])
            for i in range(length,brklen):
                new.extend(brked[i])
        elif(length == brklen):
            for i in range(0,length):
                new.extend(brked[i])
                new.extend(secs[i+1])
        else:
            for i in range(0,brklen):
                new.extend(brked[i])
                new.extend(secs[i+1])
            for i in range(brklen,length):
                new.extend(secs[i])
    else:
        new = brked[0]
        length = brklen -1
        if(length < seclen):
            for i in range(0,length):
                new.extend(secs[i])
                new.extend(brked[i+1])
            for i in range(length,seclen):
                new.extend(secs[i])
        elif(length == seclen):
            for i in range(0,length):
                new.extend(secs[i])
                new.extend(brked[i+1])
        else:
            for i in range(0,seclen):
                new.extend(secs[i])
                new.extend(brked[i+1])
            for i in range(seclen,length):
                new.extend(brked[i])
    if(mode == "new"):
        return(new)
    else:
        ol.clear()
        ol.extend(new)
        return(ol)