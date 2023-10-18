def remove_last(ol,value,**kwargs):
    '''
        from elist.elist import *
        ol = [1,'a',3,'a',5,'a']
        id(ol)
        new = remove_last(ol,'a')
        ol
        new
        id(ol)
        id(new)
        ####
        ol = [1,'a',3,'a',5,'a']
        id(ol)
        rslt = remove_last(ol,'a',mode="original")
        ol
        rslt
        id(ol)
        id(rslt)
    '''
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    new = copy.deepcopy(ol)
    new.reverse()
    new.remove(value)
    new.reverse()
    if(mode == "new"):
        return(new)
    else:
        ol.clear()
        ol.extend(new)
        return(ol)