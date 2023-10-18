def cond_value_indexes_mapping(l,**kwargs):
    '''
        from elist.elist import *
        l = [('BIGipServer', 'rd19'), ('TS013d8ed5', '0105b6b0'), ('BIGipServer', 'rd19'), ('TS013d8ed5', '0105b6b0'), ('SID', '1'), ('SID', '2')]
        
        def cond_func(ele,*args):
            cond = ele[0]
            return(cond)
        
        desc = cond_value_indexes_mapping(l,cond_func=cond_func)
        pobj(desc)
    
    '''
    cond_func = kwargs['cond_func']
    if('cond_func_args' in kwargs):
        cond_func_args = kwargs['cond_func_args']
    else:
        cond_func_args = []
    if('with_none' in kwargs):
        with_none = kwargs['with_none']
    else:
        with_none = False
    desc = {}
    for i in range(0,l.__len__()):
        ele = l[i]
        cond = cond_func(ele,*cond_func_args)
        if((cond == None)&(not(with_none))):
            pass
        else:
            if(cond in desc):
                desc[cond].append(i)
            else:
                desc[cond] = [i]
    return(desc)