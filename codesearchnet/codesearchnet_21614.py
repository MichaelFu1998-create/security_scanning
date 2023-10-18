def append(ol,ele,**kwargs):
    '''
        from elist.elist import *
        ol = [1,2,3,4]
        ele = 5
        id(ol)
        append(ol,ele,mode="original")
        ol
        id(ol)
        ####
        ol = [1,2,3,4]
        ele = 5
        id(ol)
        new = append(ol,ele)
        new
        id(new)
    '''
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    if(mode == "new"):
        new = copy.deepcopy(ol)
        new.append(ele)
        return(new)
    else:
        ol.append(ele)
        return(ol)