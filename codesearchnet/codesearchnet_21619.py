def push(ol,*eles,**kwargs):
    '''
        from elist.elist import *
        ol=[1,2,3,4]
        id(ol)
        new = push(ol,5,6,7)
        new
        id(new)
        ####
        ol=[1,2,3,4]
        id(ol)
        rslt = push(ol,5,6,7,mode="original")
        rslt
        id(rslt)
    '''
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = "new"
    eles = list(eles)
    return(extend(ol,eles,mode=mode))