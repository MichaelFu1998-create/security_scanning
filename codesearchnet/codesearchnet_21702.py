def replace_some(ol,value,*indexes,**kwargs):
    '''
        from elist.elist import *
        ol = [1,'a',3,'a',5,'a',6,'a']
        id(ol)
        new = replace_some(ol,'AAA',1,3,7)
        ol
        new
        id(ol)
        id(new)
        ####
        ol = [1,'a',3,'a',5,'a',6,'a']
        id(ol)
        rslt = replace_some(ol,'AAA',1,3,7,mode="original")
        ol
        rslt
        id(ol)
        id(rslt)
    '''
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    indexes = list(indexes)
    return(replace_seqs(ol,value,indexes,mode=mode))