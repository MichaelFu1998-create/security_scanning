def cond_pop(ol,index,**kwargs):
    '''
        from elist.jprint import pobj
        from elist.elist import *
        ol = [{'data':0;'type':'number'},{'data':'x';'type':'str'},{'data':'y';'type':'str'},4]
        #cond_func_args is a array
        def cond_func(index,value,cond_func_args):
            
    '''
    cond_func = kwargs['cond_func']
    cond_func_args = kwargs['cond_func_args']
    index = uniform_index(index,ol.__len__())
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    value = ol[index]
    cond = cond_func(index,value,*cond_func_args)
    if(mode == "new"):
        new = copy.deepcopy(ol)
        if(cond):
            popped = new.pop(index)
        else:
            popped = new
        return({'popped':popped,'list':new})
    else:
        if(cond):
            popped = ol.pop(index)
        else:
            popped = ol
        return(popped)