def mapiv2(ol,map_func,*args,**kwargs):
    '''
        from elist.elist import *
        ol = ['a','b','c','d']
        #1
        def map_func(index,value,*others):
            return(value * index + others[0] +others[-1])
        mapiv(ol,map_func,'tailA-','tailB')
        #2
        mapiv2(ol,lambda index,value,other:(value*index+other),['-'])
        mapiv2(ol,lambda index,value,other:(value*index+other),'-')
        mapiv2(ol,lambda index,value:(value*index))
    '''
    args = list(args)
    if(args.__len__() > 0):
        map_func_args = args
    else:
        if('map_func_args' in kwargs):
            map_func_args = kwargs['map_func_args']
        else:
            map_func_args = []
    lngth = ol.__len__()
    rslt = []
    for i in range(0,lngth):
        ele = map_func(i,ol[i],*map_func_args)
        rslt.append(ele)
    return(rslt)