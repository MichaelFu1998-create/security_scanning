def for_each(ol,test_func,*args):
    '''
        from elist.elist import *
        def show_func(ele):
            print("<{0}>".format(ele))
        
        ol = [1,2,3,4]
        for_each(ol,show_func)
        
        ####forEach is the same as for_each
        ####forEach have no return value
    '''
    rslt = (True,None)
    length = ol.__len__()
    for i in range(0,length):
        test_func(ol[i],*args)