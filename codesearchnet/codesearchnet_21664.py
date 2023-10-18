def reverse(ol,**kwargs):
    '''
        from elist.elist import *
        ol = [1,2,3,4]
        id(ol)
        new = reverse(ol)
        ol
        new
        id(ol)
        id(new)
        ####
        ol = [1,2,3,4]
        id(ol)
        rslt = reverse(ol,mode="original")
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
        new.reverse()
        return(new) 
    else:
        ol.reverse()
        return(ol)


    'reverse',
    'sort'