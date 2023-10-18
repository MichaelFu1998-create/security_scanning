def cond_select_indexes_all(ol,**kwargs):
    '''
        from elist.elist import *
        from elist.jprint import pobj
        def test_func(ele,x):
            cond = (ele > x)
            return(cond)
        
        ol = [1,2,3,4,5,6,7]
        rslt = cond_select_indexes_all(ol,cond_func = test_func, cond_func_args = [3])
        pobj(rslt)
    '''
    cond_func = kwargs['cond_func']
    if('cond_func_args' in kwargs):
        cond_func_args = kwargs['cond_func_args']
    else:
        cond_func_args = []
    ####
    founded = find_all(ol,cond_func,*cond_func_args)
    rslt = array_map(founded,lambda ele:ele['index'])
    return(rslt)