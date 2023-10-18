def pop_indexes(ol,indexes,**kwargs):
    '''
        from elist.jprint import pobj
        from elist.elist import *
        ol = [1,2,3,4,5,6]
        id(ol)
        rslt = pop_indexes(ol,{0,-3,5})
        ol
        id(ol)
        id(rslt['list'])
        ####
        ol = [1,2,3,4,5,6]
        id(ol)
        rslt = pop_indexes(ol,{0,-3,5},mode="original")
        rslt
        ol
        id(ol)
    '''
    length = ol.__len__()
    indexes = list(map(lambda index:uniform_index(index,length),list(indexes)))
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    if(mode == "new"):
        cpol = copy.deepcopy(ol)
        new = []
        popped = []
        for i in range(0,length):
            if(i in indexes):
                popped.append(cpol[i])
            else:
                new.append(cpol[i])
        return({'popped':popped,'list':new})
    else:
        tmp = []
        popped = []
        for i in range(0,length):
            if(i in indexes):
                popped.append(ol[i])
            else:
                tmp.append(ol[i])
        ol.clear()
        for i in range(0,tmp.__len__()):
            ol.append(tmp[i])
        return(popped)