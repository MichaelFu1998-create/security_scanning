def pop_range(ol,start_index,end_index,**kwargs):
    '''
        from elist.jprint import pobj
        from elist.elist import *
        ol = [1,2,3,4,5,6]
        id(ol)
        rslt = pop_range(ol,2,4)
        ol
        id(ol)
        id(rslt['list'])
        ####
        ol = [1,2,3,4,5,6]
        id(ol)
        rslt = pop_range(ol,2,4,mode="original")
        rslt
        ol
        id(ol)
    '''
    length = ol.__len__()
    start_index = uniform_index(start_index,length)
    end_index = uniform_index(end_index,length)
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    if(mode == "new"):
        cpol = copy.deepcopy(ol)
        new = []
        popped = []
        for i in range(0,start_index):
            new.append(cpol[i])
        for i in range(start_index,end_index):
            popped.append(cpol[i])
        for i in range(end_index,length):
            new.append(cpol[i])
        return({'popped':popped,'list':new})
    else:
        tmp = []
        popped = []
        for i in range(0,start_index):
            tmp.append(ol[i])
        for i in range(start_index,end_index):
            popped.append(ol[i])
        for i in range(end_index,length):
            tmp.append(ol[i])
        ol.clear()
        for i in range(0,tmp.__len__()):
            ol.append(tmp[i])
        return(popped)