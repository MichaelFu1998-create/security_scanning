def extend(ol,nl,**kwargs):
    '''
        from elist.elist import *
        ol = [1,2,3,4]
        nl = [5,6,7,8]
        id(ol)
        extend(ol,nl,mode="original")
        ol
        id(ol)
        ####
        ol = [1,2,3,4]
        nl = [5,6,7,8]
        id(ol)
        new = extend(ol,nl)
        new
        id(new)
    '''
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    if(mode == "new"):
        new = copy.deepcopy(ol)
        cpnl = copy.deepcopy(nl)
        new.extend(cpnl)
        return(new)
    else:
        ol.extend(nl)
        return(ol)