def remove_first(ol,value,**kwargs):
    '''
        from elist.jprint import pobj
        from elist.elist import *
        ol = [1,'a',3,'a',5,'a']
        id(ol)
        new = remove_first(ol,'a')
        ol
        new
        id(ol)
        id(new)
        ####
        ol = [1,'a',3,'a',5,'a']
        id(ol)
        rslt = remove_first(ol,'a',mode="original")
        ol
        rslt
        id(ol)
        id(rslt)
        ####array_remove is the same as remove_first
    '''
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    if(mode == "new"):
        new = copy.deepcopy(ol)
        new.remove(value)
        return(new)
    else:
        ol.remove(value)
        return(ol)