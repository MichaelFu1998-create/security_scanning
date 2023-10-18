def remove_many(ol,values,seqs,**kwargs):
    '''
        from elist.elist import *
        ol = [1,'a',3,'b',5,'a',6,'a',7,'b',8,'b',9]
        id(ol)
        new = remove_many(ol,['a','b'],[1,2])
        ol
        new
        id(ol)
        id(new)
        ####
        ol = [1,'a',3,'b',5,'a',6,'a',7,'b',8,'b',9]
        id(ol)
        rslt = remove_many(ol,['a','b'],[1,2],mode="original")
        ol
        rslt
        id(ol)
        id(rslt)
    '''
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    values = copy.deepcopy(values)
    seqs = copy.deepcopy(seqs)
    cursors = [-1] * values.__len__()
    new = []
    length = ol.__len__()
    cpol = copy.deepcopy(ol)
    for i in range(0,length):
        label = True
        for j in range(0,cursors.__len__()):
            which = seqs[j]
            value = values[j]
            if(cpol[i] == value):
                cursors[j] = cursors[j] + 1
                if(cursors[j] == which):
                    label = False
                    break
                else:
                    pass
            else:
                pass
        if(label):
            new.append(cpol[i])
        else:
            pass
    if(mode == "new"):
        return(new) 
    else:
        ol.clear()
        ol.extend(new)
        return(ol)