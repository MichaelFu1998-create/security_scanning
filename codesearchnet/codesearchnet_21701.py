def replace_seqs(ol,value,indexes,**kwargs):
    '''
        from elist.elist import *
        ol = [1,'a',3,'a',5,'a',6,'a']
        id(ol)
        new = replace_seqs(ol,'AAA',[1,3,7])
        ol
        new
        id(ol)
        id(new)
        ####
        ol = [1,'a',3,'a',5,'a',6,'a']
        id(ol)
        rslt = replace_seqs(ol,'AAA',[1,3,7],mode="original")
        ol
        rslt
        id(ol)
        id(rslt)
        #replace_indexes = replace_seqs
    '''
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    indexes = list(indexes)
    new = []
    length = ol.__len__()
    cpol = copy.deepcopy(ol)
    for i in range(0,length):
        if(i in indexes):
            new.append(value)
        else:
            new.append(cpol[i])
    if(mode == "new"):
        return(new)
    else:
        ol.clear()
        ol.extend(new)
        return(ol)