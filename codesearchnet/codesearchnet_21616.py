def prepend(ol,ele,**kwargs):
    '''
        from elist.elist import *
        ol = [1,2,3,4]
        ele = 5
        id(ol)
        prepend(ol,ele,mode="original")
        ol
        id(ol)
        ####
        ol = [1,2,3,4]
        ele = 5
        id(ol)
        new = prepend(ol,ele)
        new
        id(new)
    '''
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    if(mode == "new"):
        new = [ele]
        cpol = copy.deepcopy(ol)
        new.extend(cpol)
        return(new)
    else:
        length = ol.__len__()
        ol.append(None)
        for i in range(length-1,-1,-1):
            ol[i+1] = ol[i]
        ol[0] = ele
        return(ol)