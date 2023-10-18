def cons(head_ele,l,**kwargs):
    '''
        from elist.elist import *
        ol=[1,2,3,4]
        id(ol)
        new = cons(5,ol)
        new
        id(new)
        ####
        ol=[1,2,3,4]
        id(ol)
        rslt = cons(5,ol,mode="original")
        rslt
        id(rslt)
    '''
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = "new"
    return(prepend(l,head_ele,mode=mode))