def find_allnot(ol,test_func,*args):
    '''
        from elist.elist import *
        from elist.jprint import pobj
        def test_func(ele,x):
            cond = (ele > x)
            return(cond)
        
        ol = [1,2,3,4,5,6,7]
        rslt = find_allnot(ol,test_func,3)
        pobj(rslt)
    '''
    rslt =[]
    length = ol.__len__()
    for i in range(0,length):
        cond = test_func(ol[i],*args)
        if(cond):
            pass
        else:
            rslt.append({'index':i,'value':ol[i]})
    return(rslt)