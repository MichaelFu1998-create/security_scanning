def insert_some(ol,*eles,**kwargs):
    '''
        from elist.elist import *
        ol = [1,2,3,4]
        id(ol)
        insert_some(ol,5,6,7,8,index=2,mode="original")
        ol
        id(ol)
        ####
        ol = [1,2,3,4]
        id(ol)
        new = insert_some(ol,5,6,7,8,index=2)
        new
        id(new)
    '''
    start_index = kwargs['index']
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    length = ol.__len__()
    cpol = copy.deepcopy(ol)
    if(mode == "new"):
        si = uniform_index(start_index,length)
        new = copy.deepcopy(cpol[0:si])
        new.extend(list(eles))
        new.extend(cpol[si:])
        return(new)
    else:
        si = uniform_index(start_index,length)
        new = cpol[0:si]
        new.extend(list(eles))
        new.extend(cpol[si:])
        ol.clear()
        for i in range(0,new.__len__()):
            ol.append(new[i])
        return(ol)