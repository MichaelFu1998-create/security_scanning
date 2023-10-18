def array_map2(*referls,**kwargs):
    '''
        obseleted just for compatible
        from elist.elist import *
        ol = [1,2,3,4]
        refl1 = ['+','+','+','+']
        refl2 = [7,7,7,7]
        refl3 = ['=','=','=','=']
        def map_func(ele,ref_ele1,ref_ele2,ref_ele3,prefix,suffix):
            s = prefix+': ' + str(ele) + str(ref_ele1) + str(ref_ele2) + str(ref_ele3) + suffix
            return(s)

        ####
        rslt = array_map2(ol,refl1,refl2,refl3,map_func=map_func,map_func_args=['Q','?'])
        pobj(rslt)
    '''
    map_func = kwargs['map_func']
    if('map_func_args' in kwargs):
        map_func_args = kwargs['map_func_args']
    else:
        map_func_args = []
    length = referls.__len__()
    rslt = []
    anum = list(referls)[0].__len__()
    for j in range(0,anum):
        args = []
        for i in range(0,length):
            refl = referls[i]
            args.append(refl[j])
        args.extend(map_func_args)
        v = map_func(*args)
        rslt.append(v)
    return(rslt)