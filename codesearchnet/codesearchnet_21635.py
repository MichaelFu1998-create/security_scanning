def sortDictList(dictList,**kwargs):
    '''
        students = [
            {'name':'john','class':'A', 'year':15},
            {'name':'jane','class':'B', 'year':12},
            {'name':'dave','class':'B', 'year':10}
        ]
        
        rslt = sortDictList(students,cond_keys=['name','class','year'])
        pobj(rslt)
        rslt = sortDictList(students,cond_keys=['name','year','class'])
        pobj(rslt)
        rslt = sortDictList(students,cond_keys=['class','name','year'])
        pobj(rslt)
        rslt = sortDictList(students,cond_keys=['class','year','name'])
        pobj(rslt)
        rslt = sortDictList(students,cond_keys=['year','name','class'])
        pobj(rslt)
        rslt = sortDictList(students,cond_keys=['year','name','class'])
        pobj(rslt)
    '''
    def default_eq_func(value1,value2):
        cond = (value1 == value2)
        return(cond)
    def default_gt_func(value1,value2):
        cond = (value1 > value2)
        return(cond)
    def default_lt_func(value1,value2):
        cond = (value1 < value2)
        return(cond)
    if('eq_func' in kwargs):
        eq_func = kwargs['eq_func']
    else:
        eq_func = default_eq_func
    if('gt_func' in kwargs):
        gt_func = kwargs['gt_func']
    else:
        gt_func = default_gt_func
    if('lt_func' in kwargs):
        lt_func = kwargs['lt_func']
    else:
        lt_func = default_lt_func
    if('reverse' in kwargs):
        reverse = kwargs['reverse']
    else:
        reverse = False
    keys = kwargs['cond_keys']
    def cmp_dict(d1,d2):
        '''
        '''
        length = keys.__len__()
        for i in range(0,length):
            key = keys[i]
            cond = eq_func(d1[key],d2[key])
            if(cond):
                pass
            else:
                cond = gt_func(d1[key],d2[key])
                if(cond):
                    return(1)
                else:
                    return(-1)
        return(0)
    ndl = dictList
    ndl = sorted(ndl,key=functools.cmp_to_key(cmp_dict),reverse=reverse)
    return(ndl)