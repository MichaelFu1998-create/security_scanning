def find_last(ol,test_func,*args):
    '''
        from elist.elist import *
        def test_func(ele,x):
            cond = (ele > x)
            return(cond)
        
        ol = [1,2,3,4]
        last = find_last(ol,test_func,3)
        last
        #####
        ol = [10,20,30,40]
        last = find_last(ol,test_func,3)
        last
    '''
    length = ol.__len__()
    for i in range(length-1,-1,-1):
        cond = test_func(ol[i],*args)
        if(cond):
            return({'index':i,'value':ol[i]})
        else:
            pass
    return({'index':None,'value':None})