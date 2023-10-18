def array_dualmap(ol,value_map_func,**kwargs):
    '''
        from elist.elist import *
        ol = ['a','b','c','d']
        def index_map_func(index,prefix,suffix):
            s = prefix +str(index+97)+ suffix
            return(s)
        
        def value_map_func(mapped_index,ele,prefix,suffix):
            s = prefix+mapped_index+': ' + str(ele) + suffix
            return(s)
        
        ####
        rslt = array_dualmap2(ol,index_map_func=index_map_func,index_map_func_args=[': ',' is '],value_map_func=value_map_func,value_map_func_args=['ord',' yes?'])
        pobj(rslt)
    '''
    def get_self(obj):
        return(obj)
    if('index_map_func_args' in kwargs):
        index_map_func_args = kwargs['index_map_func_args']
    else:
        index_map_func_args = []
    if('value_map_func_args' in kwargs):
        value_map_func_args = kwargs['value_map_func_args']
    else:
        value_map_func_args = []
    if('index_map_func' in kwargs):
        index_map_func = kwargs['index_map_func']
    else:
        index_map_func = get_self
    length = ol.__len__()
    il = list(range(0,length))
    nil = list(map(lambda ele:index_map_func(ele,*index_map_func_args),il))
    nvl = []
    for i in range(0,length):
        ele = ol[i]
        v = value_map_func(nil[i],ele,*value_map_func_args)
        nvl.append(v)
    return(nvl)