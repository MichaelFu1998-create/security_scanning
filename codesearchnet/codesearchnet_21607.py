def array_dualmap2(*refls,**kwargs):
    '''
        from elist.elist import *
        ol = [1,2,3,4]
        refl1 = ['+','+','+','+']
        refl2 = [7,7,7,7]
        refl3 = ['=','=','=','=']
        def index_map_func(index):
            s ="<"+str(index)+">"
            return(s)
        
        def value_map_func(mapped_index,ele,ref_ele1,ref_ele2,ref_ele3,prefix,suffix):
            s = prefix+mapped_index+': ' + str(ele) + str(ref_ele1) + str(ref_ele2) + str(ref_ele3) + suffix
            return(s)
        
        ####
        rslt = array_dualmap2(ol,refl1,refl2,refl3,index_map_func=index_map_func,value_map_func=value_map_func,value_map_func_args=['Q','?'])
        pobj(rslt)
    '''
    def get_self(obj,*args):
        return(obj)
    if('value_map_func_args' in kwargs):
        value_map_func_args = kwargs['value_map_func_args']
    else:
        value_map_func_args = []
    if('index_map_func' in kwargs):
        index_map_func = kwargs['index_map_func']
    else:
        index_map_func = get_self
    if('index_map_func_args' in kwargs):
        index_map_func_args = kwargs['index_map_func_args']
    else:
        index_map_func_args = []
    length = ol.__len__()
    il = list(range(0,length))
    nil = list(map(lambda ele:index_map_func(ele,*index_map_func_args),il))
    refls = list(refls)
    refls = prepend(refls,nil)
    nvl = array_map2(*refls,map_func = value_map_func,map_func_args=value_map_func_args)
    return(nvl)