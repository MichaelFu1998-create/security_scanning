def some(ol,test_func,*args):
    '''
        from elist.elist import *
        def test_func(ele,x):
            cond = (ele > x)
            return(cond)
        
        ol = [1,2,3,4]
        some(ol,test_func,3)
        
        ol = [1,2,1,3]
        some(ol,test_func,3)
    '''
    rslt = {'cond':False,'index':None}
    length = ol.__len__()
    for i in range(0,length):
        cond = test_func(ol[i],*args)
        if(cond):
            return({'cond':True,'index':i})
        else:
            pass
    return(rslt)