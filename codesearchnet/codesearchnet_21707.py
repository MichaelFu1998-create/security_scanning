def rangize_supplement(spans,lngth):
    '''
        spans = [(0, 3), (4, 7), (8, 10), (11, 12), (13, 16), (17, 20)]
        rangize_supplement(spans,24)
        
    '''
    rslt = []
    si = 0
    ei = spans[0][0]
    if(si == ei):
        pass
    else:
        rslt.append((si,ei))
    prev_ei = spans[0][1]
    for i in range(1,spans.__len__()):
        si = prev_ei
        ei = spans[i][0]
        rslt.append((si,ei))
        prev_ei = spans[i][1]
    if(prev_ei < lngth):
        rslt.append((prev_ei,lngth))
    else:
        rslt.append((prev_ei,lngth+1))
    return(rslt)