def filter(ol,test_func,*args,**kwargs):
    '''
        from elist.elist import *
        def test_func(ele,x):
            cond = (ele > x)
            return(cond)
        
        ol = [1,2,3,4]
        id(ol)
        new = filter(ol,test_func,3)
        new
        id(new)
        #####
        ol = [10,20,30,40]
        id(ol)
        rslt = filter(ol,test_func,3,mode="original")
        rslt
        id(rslt)
    '''
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = "new"
    length = ol.__len__()
    new = []
    cpol = copy.deepcopy(ol)
    for i in range(0,length):
        cond = test_func(cpol[i],*args)
        if(cond):
            new.append(cpol[i])
        else:
            pass
    if(mode == "new"):
        return(new)
    else:
        ol.clear()
        ol.extend(new)
        return(ol)