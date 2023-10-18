def cond_replace_value_some(ol,dst_value,*some,**kwargs):
    '''
        from elist.elist import *
        ol = [1,'X',3,'b',5,'c',6,'A',7,'b',8,'B',9]
        id(ol)
        def afterCH(ele,ch):
            cond = (ord(str(ele)) > ord(ch))
            return(cond)
        
        new = cond_replace_value_some(ol,"REPLACED",0,2,cond_func=afterCH,cond_func_args=['B'])
        ol
        new
        id(ol)
        id(new)
        ####
        ol = [1,'X',3,'b',5,'c',6,'A',7,'b',8,'B',9]
        id(ol)
        rslt = cond_replace_value_some(ol,"REPLACED",0,2,cond_func=afterCH,cond_func_args=['B'],mode="original")
        ol
        rslt
        id(ol)
        id(rslt)
    '''
    cond_func = kwargs['cond_func']
    if('cond_func_args' in kwargs):
        cond_func_args = kwargs['cond_func_args']
    else:
        cond_func_args = []
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    seqs = list(some)
    new = copy.deepcopy(ol)
    selected = find_all(new,cond_func,*cond_func_args)
    selected_indexes = array_map(selected,lambda ele:ele['index'])
    selected_indexes = select_seqs(selected_indexes,seqs)
    new = replace_seqs(new,dst_value,selected_indexes)
    if(mode == "new"):
        return(new)
    else:
        ol.clear()
        ol.extend(new)
        return(ol)