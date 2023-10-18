def rangize(break_points,length):
    '''
        break_points = [1,3,9,12,-2]
        length = 15
        secs = rangize(break_points,length)
        forEach(secs,print)
    '''
    bps = array_map(break_points,uniform_index,length)
    bps.sort()
    bps = prepend(bps,0)
    bps = append(bps,length)
    bps = uniqualize(bps)
    bpslen = bps.__len__()
    secs=[(0,bps[0])]
    for i in range(0,bpslen-1):
        r = (bps[i],bps[i+1])
        secs.append(r)
    secs.append((bps[bpslen-1],length))
    if(secs[0][0] == secs[0][1]):
        secs.pop(0)
    else:
        pass
    if(secs[-1][0] == secs[-1][1]):
        secs.pop(-1)
    else:
        pass
    return(secs)