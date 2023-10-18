def fill(ol,value,start=None, end=None,**kwargs):
    '''
        from elist.elist import *
        ol = [1, 2, 3,4,5]
        id(ol)
        rslt = fill(ol,4)
        rslt
        id(rslt)
        ####
        ol = [1, 2, 3,4,5]
        id(ol)
        rslt = fill(ol,4,1)
        rslt
        id(rslt)
        ####
        ol = [1, 2, 3,4,5]
        id(ol)
        rslt = fill(ol,6,1,3,mode="original")
        rslt
        id(rslt)
    '''
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = "new"
    length = ol.__len__()
    if(start==None):
        start = 0
    else:
        pass
    if(end==None):
        end = length
    else:
        pass
    start = uniform_index(start,length)
    end = uniform_index(end,length)
    new = copy.deepcopy(ol)
    for i in range(start,end):
        new[i] = value
    if(mode == "new"):
        return(new)
    else:
        ol.clear()
        ol.extend(new)
        return(ol)