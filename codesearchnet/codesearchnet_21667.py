def splice(ol,start,deleteCount,*eles,**kwargs):
    '''
        from elist.elist import *
        ol = ["angel", "clown", "mandarin", "surgeon"]
        id(ol)
        new = splice(ol,2,0,"drum")
        new
        id(new)
        ####
        ol = ["angel", "clown", "mandarin", "surgeon"]
        id(ol)
        new = splice(ol,2,1,"drum",mode="original")
        new
        id(new)
        ####
        ol = [1,2,3,4,5,6]
        id(ol)
        new = splice(ol,2,2,77,777)
        new
        id(new)
    '''
    if('mode' in kwargs):
        mode = kwargs['mode']
    else:
        mode = "new"
    length = ol.__len__()
    new = copy.deepcopy(ol)
    if(start >= length):
        eles = list(eles)
        new.extend(eles)
    else:
        start = uniform_index(start,length)
        end = start + deleteCount
        tmp = pop_range(new,start,end,mode="new")['list']
        new = insert_some(tmp,*eles,index=start,mode="new")
    if(mode == "new"):
        return(new)
    else:
        ol.clear()
        ol.extend(new)
        return(ol)