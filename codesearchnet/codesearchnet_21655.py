def remove_which(ol,value,which,**kwargs):
    '''
        from elist.elist import *
        ol = [1,'a',3,'a',5,'a']
        id(ol)
        new = remove_which(ol,'a',1)
        ol
        new
        id(ol)
        id(new)
        ####
        ol = [1,'a',3,'a',5,'a']
        id(ol)
        rslt = remove_which(ol,'a',1,mode="original")
        ol
        rslt
        id(ol)
        id(rslt)
    '''
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    new = copy.deepcopy(ol)
    length = ol.__len__()
    if(mode == "new"):
        l = new 
    else:
        l = ol
    seq = -1
    for i in range(0,length):
        if(ol[i]==value):
            seq = seq + 1
            if(seq == which):
                l.pop(i)
                break
            else:
                pass
        else:
            pass
    return(l)