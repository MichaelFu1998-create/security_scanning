def insert_many(ol,eles,locs,**kwargs):
    '''
        from elist.elist import *
        ol = [1,2,3,4,5]
        eles = [7,77,777]
        locs = [0,2,4]
        id(ol)
        new = insert_many(ol,eles,locs)
        ol
        new
        id(new)
        ####
        ol = [1,2,3,4,5]
        eles = [7,77,777]
        locs = [0,2,4]
        id(ol)
        rslt = insert_many(ol,eles,locs,mode="original")
        ol
        rslt
        id(rslt)
    '''
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    eles = copy.deepcopy(eles)
    locs = copy.deepcopy(locs)
    new = []
    length = ol.__len__()
    cpol = copy.deepcopy(ol)
    for i in range(0,locs.__len__()):
        if(locs[i]>=length):
            pass
        else:
            locs[i] = uniform_index(locs[i],length)
    tmp = sorted_refer_to(eles,locs)
    eles = tmp['list']
    locs = tmp['referer']
    label = eles.__len__()
    si = 0
    ei = 0
    for i in range(0,locs.__len__()):
        if(locs[i]>=length):
            label = i
            break
        else:
            ei = locs[i]
            new.extend(cpol[si:ei])
            new.append(eles[i])
            si = ei
    for i in range(label,locs.__len__()):
        new.append(eles[i])
    new.extend(cpol[ei:])
    if(mode == "new"):
        return(new)
    else:
        ol.clear()
        ol.extend(new)
        return(ol)