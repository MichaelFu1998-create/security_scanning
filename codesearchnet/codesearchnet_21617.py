def prepend_some(ol,*eles,**kwargs):
    '''
        from elist.elist import *
        ol = [1,2,3,4]
        id(ol)
        prepend_some(ol,5,6,7,8,mode="original")
        ol
        id(ol)
        ####
        ol = [1,2,3,4]
        id(ol)
        new = prepend_some(ol,5,6,7,8)
        new
        id(new)
        #####unshift is the same as prepend_some
        >>> unshift(ol,9,10,11,12)
        [9, 10, 11, 12, 1, 2, 3, 4]
    '''
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    return(prextend(ol,list(eles),mode=mode))