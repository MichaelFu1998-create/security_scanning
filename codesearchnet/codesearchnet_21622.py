def cdr(ol,**kwargs):
    '''
        from elist.elist import *
        ol=[1,2,3,4]
        id(ol)
        new = cdr(ol)
        new
        id(new)
        ####
        ol=[1,2,3,4]
        id(ol)
        rslt = cdr(ol,mode="original")
        rslt
        id(rslt)
    '''
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = "new"
    if(mode == "new"):
        cpol = copy.deepcopy(ol)
        return(cpol[1:])
    else:
        ol.pop(0)
        return(ol)