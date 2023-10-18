def shift(ol,**kwargs):
    '''
        from elist.jprint import pobj
        from elist.elist import *
        ol = [1,2,3,4]
        id(ol)
        rslt = shift(ol)
        pobj(rslt)
        ol
        id(ol)
        id(rslt['list'])
        ####
        ol = [1,2,3,4]
        id(ol)
        rslt = shift(ol,mode="original")
        rslt
        ol
        id(ol)
    '''
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = "new"
    length = ol.__len__()
    rslt = pop(ol,0,mode=mode)
    return(rslt)