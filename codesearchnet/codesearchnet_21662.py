def array_from(obj,func,*args):
    '''
        from elist.elist import *
        array_from("abcd",None)
        #####
        def map_func(ele,x,y):
            return(int(ele)+x+y)
        
        array_from("1234",map_func,1000,100)
        
        def map_func(ele):
            return(int(ele)*2)
        
        array_from("1234",map_func)
        
        array_from("1234",None)
    '''
    if(func):
        l = list(obj)
        rslt = list(map(lambda ele:func(ele,*args),l))
        return(rslt)
    else:
        return(list(obj))