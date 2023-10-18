def select_loose_in(pl,k):
    '''
        pl = ['bcd','xabcxx','x','y']
        select_loose_in(pl,'abc')
    '''
    def cond_func(ele,index,k):
        if(type(ele) == type([])):
            cond = loose_in(ele,k)
        else:
            cond = (k in ele)
        return(cond)
    arr = cond_select_values_all2(pl,cond_func=cond_func, cond_func_args =[k])
    return(arr)