def select_strict_in(pl,k):
    '''
        pl = ['bcd','xabcxx','x','y']
        select_strict_in(pl,'abc')
    '''
    def cond_func(ele,index,k):
        if(type(ele) == type([])):
            cond = (k in ele)
        else:
            cond = (k == ele)
        return(cond)
    arr = cond_select_values_all2(pl,cond_func=cond_func, cond_func_args =[k])
    return(arr)