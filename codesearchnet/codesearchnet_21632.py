def sort(ol,**kwargs):
    '''
        from elist.elist import *
        ol = [1,3,4,2]
        id(ol)
        new = sort(ol)
        ol
        new
        id(ol)
        id(new)
        ####
        ol = [1,3,4,2]
        id(ol)
        rslt = sort(ol,mode="original")
        ol
        rslt
        id(ol)
        id(rslt)
    '''
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    if(mode == "new"):
        new = copy.deepcopy(ol)
        new.sort()
        return(new) 
    else:
        ol.sort()
        return(ol)