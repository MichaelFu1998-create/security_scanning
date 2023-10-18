def slice(ol,start,end=None,**kwargs):
    '''
        from elist.elist import *
        ol = [1,2,3,4,5]
        id(ol)
        new = slice(ol,2,4)
        new
        id(new)
        ####
        id(ol)
        rslt = slice(ol,1,-2,mode="original")
        rslt
        id(rslt)
    '''
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = "new"
    length = ol.__len__()
    new = copy.deepcopy(ol)
    if(end == None):
        end = length
    else:
        end = uniform_index(end,length)
    start = uniform_index(start,length)
    if(mode == "new"):
        return(new[start:end])
    else:
        ol.clear()
        ol.extend(new[start:end])
        return(ol)