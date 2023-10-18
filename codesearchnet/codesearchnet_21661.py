def init(len,default_element=None):
    '''
        from elist.elist import *
        init(5)
        init(5,"x")
    '''
    rslt = []
    for i in range(0,len):
        rslt.append(copy.deepcopy(default_element))
    return(rslt)