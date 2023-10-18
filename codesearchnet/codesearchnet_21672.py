def cond_uniqualize(l,**kwargs):
    '''
        from elist.elist import *
        l = [('BIGipServer', 'rd100'), ('TS013d8ed5', '00A0'), ('BIGipServer', 'rd200'), ('TS013d8ed5', '00B0'), ('SID', '1'), ('SID', '2')]
        
        def cond_func(ele,*args):
            cond = ele[0]
            return(cond)
        
        uniqualized = cond_uniqualize(l,cond_func=cond_func)
        pobj(uniqualized)
        
        l = [('BIGipServer', 'rd100'), ('TS013d8ed5', '00A0'), ('BIGipServer', 'rd200'), ('TS013d8ed5', '00B0'), ('SID', '1'), ('SID', '2')]
        
        reserved_mapping = {'BIGipServer':0,'TS013d8ed5':1,'SID':1}
        uniqualized = cond_uniqualize(l,cond_func=cond_func,reserved_mapping=reserved_mapping)
        pobj(uniqualized)
        
    '''
    cond_func = kwargs['cond_func']
    if('cond_func_args' in kwargs):
        cond_func_args = kwargs['cond_func_args']
    else:
        cond_func_args = []
    if('reserved_mapping' in kwargs):
        reserved_mapping = kwargs['reserved_mapping']
    else:
        reserved_mapping = None
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = 'new'
    desc = cond_value_indexes_mapping(l,cond_func=cond_func,cond_func_args=cond_func_args,with_none=True)
    keys = list(desc.keys())
    if(None in keys):
        keys.remove(None)
    else:
        pass
    rmapping = {}
    for key in keys:
        rmapping[key] = 0
    if(reserved_mapping == None):
        pass
    else:
        for key in reserved_mapping:
            rmapping[key] = reserved_mapping[key]
    reserved_indexes = []
    for key in keys:
        indexes = desc[key]
        index = indexes[rmapping[key]]
        reserved_indexes.append(index)
    newcopy = copy.deepcopy(l)
    new = select_seqs(newcopy,reserved_indexes)
    ####
    if(None in desc):
        for index in desc[None]:
            new.append(newcopy[index])
    else:
        pass
    ####
    if(mode == "new"):
        return(new)
    else:
        ol.clear()
        ol.extend(new)
        return(ol)