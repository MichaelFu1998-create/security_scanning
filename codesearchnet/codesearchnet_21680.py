def select_regex_in(pl,regex):
    '''
        regex = re.compile("^x.*x$")
        pl = ['bcd','xabcxx','xx','y']
        select_regex_in(pl,'abc')
    '''
    def cond_func(ele,index,regex):
        if(type(ele)==type([])):
            cond = regex_in(ele,regex)
        else:
            m = regex.search(ele)
            if(m == None):
                cond = False
            else:
                cond = True
        return(cond)
    arr = cond_select_values_all2(pl,cond_func=cond_func, cond_func_args =[regex])
    return(arr)