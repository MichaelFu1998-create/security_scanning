def append_some(ol,*eles,**kwargs):
    '''
        from elist.elist import *
        ol = [1,2,3,4]
        id(ol)
        append_some(ol,5,6,7,8,mode="original")
        ol
        id(ol)
        ####
        ol = [1,2,3,4]
        id(ol)
        new = append_some(ol,5,6,7,8)
        new
        id(new)
    '''
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    return(extend(ol,list(eles),mode=mode))