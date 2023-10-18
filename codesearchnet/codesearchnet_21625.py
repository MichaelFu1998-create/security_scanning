def insert(ol,start_index,ele,**kwargs):
    '''
        from elist.elist import *
        ol = [1,2,3,4]
        ele = 5
        id(ol)
        insert(ol,2,ele,mode="original")
        ol
        id(ol)
        ####
        ol = [1,2,3,4]
        ele = 5
        id(ol)
        new = insert(ol,2,ele)
        new
        id(new)
    '''
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    if(mode == "new"):
        length = ol.__len__()
        cpol = copy.deepcopy(ol)
        si = uniform_index(start_index,length)
        new = copy.deepcopy(cpol[0:si])
        new.append(ele)
        new.extend(cpol[si:])
        return(new)
    else:
        ol.insert(start_index,ele)
        return(ol)