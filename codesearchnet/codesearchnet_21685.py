def find_which(ol,which,test_func,*args):
    '''
        from elist.elist import *
        def test_func(ele,x):
            cond = (ele > x)
            return(cond)
        
        ol = [1,2,3,4,5,6,7]
        last = find_which(ol,0,test_func,3)
        last
        last = find_which(ol,2,test_func,3)
        last
    '''
    length = ol.__len__()
    seq = -1
    for i in range(0,length):
        cond = test_func(ol[i],*args)
        if(cond):
            seq = seq + 1
            if(seq == which):
                return({'index':i,'value':ol[i]})
            else:
                pass
        else:
            pass
    return({'index':None,'value':None})