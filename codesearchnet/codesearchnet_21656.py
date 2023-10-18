def remove_some(ol,value,*seqs,**kwargs):
    '''
        from elist.elist import *
        ol = [1,'a',3,'a',5,'a',6,'a']
        id(ol)
        new = remove_some(ol,'a',1,3)
        ol
        new
        id(ol)
        id(new)
        ####
        ol = [1,'a',3,'a',5,'a',6,'a']
        id(ol)
        rslt = remove_some(ol,'a',1,3,mode="original")
        ol
        rslt
        id(ol)
        id(rslt)
    '''
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    seqs = list(seqs)
    new = []
    length = ol.__len__()
    seq = -1
    cpol = copy.deepcopy(ol)
    for i in range(0,length):
        if(cpol[i]==value):
            seq = seq + 1
            if(seq in seqs):
                pass
            else:
                new.append(cpol[i])
        else:
            new.append(cpol[i])
    if(mode == "new"):
        return(new) 
    else:
        ol.clear()
        ol.extend(new)
        return(ol)