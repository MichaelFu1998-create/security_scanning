def remove_firstnot(ol,value,**kwargs):
    '''
        from elist.jprint import pobj
        from elist.elist import *
        ol = [1,'a',3,'a',5,'a']
        id(ol)
        new = remove_firstnot(ol,'a')
        ol
        new
        id(ol)
        id(new)
        ####
        ol = [1,'a',3,'a',5,'a']
        id(ol)
        rslt = remove_firstnot(ol,'a',mode="original")
        ol
        rslt
        id(ol)
        id(rslt)
        ####array_removenot is the same as remove_firstnot
    '''
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    length = ol.__len__()
    if(mode == "new"):
        new = copy.deepcopy(ol)
        for i in range(0,length):
            if(new[i] == value):
                pass
            else:
                new.pop(i)
                return(new)
        return(new)
    else:
        for i in range(0,length):
            if(ol[i] == value):
                pass
            else:
                ol.pop(i)
                return(ol)
        return(ol)