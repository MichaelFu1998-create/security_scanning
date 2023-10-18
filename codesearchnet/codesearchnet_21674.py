def deinterleave(ol,gnum):
    '''
        ol = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        deinterleave(ol,3)
        
    '''
    def test_func(ele,index,interval,which):
        cond= (index % interval == which)
        return(cond)
    rslt = []
    for i in range(0,gnum):
        arr = cond_select_all2(ol,cond_func = test_func,cond_func_args = [gnum,i])
        rslt.append(arr)
    return(rslt)