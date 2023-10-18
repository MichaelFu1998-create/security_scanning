def array_map(ol,map_func,*args):
    '''
        obseleted,just for compatible
        from elist.elist import *
        ol = [1,2,3,4]
        def map_func(ele,mul,plus):
            return(ele*mul+plus)

        array_map(ol,map_func,2,100)
    '''
    rslt = list(map(lambda ele:map_func(ele,*args),ol))
    return(rslt)