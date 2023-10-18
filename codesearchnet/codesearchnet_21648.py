def pop(ol,index,**kwargs):
    '''
        from elist.jprint import pobj
        from elist.elist import *
        ol = [1,2,3,4]
        id(ol)
        rslt = pop(ol,2)
        pobj(rslt)
        ol
        id(ol)
        id(rslt['list'])
        ####
        ol = [1,2,3,4]
        id(ol)
        rslt = pop(ol,2,mode="original")
        rslt
        ol
        id(ol)
    '''
    index = uniform_index(index,ol.__len__())
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    if(mode == "new"):
        new = copy.deepcopy(ol)
        popped = new.pop(index)
        return({'popped':popped,'list':new})
    else:
        popped = ol.pop(index)
        return(popped)