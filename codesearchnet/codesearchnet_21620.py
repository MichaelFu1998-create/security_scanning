def prextend(ol,nl,**kwargs):
    '''
        from elist.elist import *
        ol = [1,2,3,4]
        nl = [5,6,7,8]
        id(ol)
        id(nl)
        prextend(ol,nl,mode="original")
        ol
        id(ol)
        ####
        ol = [1,2,3,4]
        nl = [5,6,7,8]
        id(ol)
        id(nl)
        new = prextend(ol,nl)
        new
        id(new)
    '''
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    if(mode == "new"):
        new = copy.deepcopy(nl)
        cpol = copy.deepcopy(ol)
        new.extend(cpol)
        return(new)
    else:
        length = ol.__len__()
        nl_len = nl.__len__()
        for i in range(0,nl_len):
            ol.append(None)
        for i in range(length-1,-1,-1):
            ol[i+nl_len] = ol[i]
        for i in range(0,nl_len):
            ol[i] = nl[i]
        return(ol)