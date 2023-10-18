def replace_value_seqs(ol,src_value,dst_value,seqs,**kwargs):
    '''
        from elist.elist import *
        ol = [1,'a',3,'a',5,'a',6,'a']
        id(ol)
        new = replace_value_seqs(ol,'a','AAA',[0,1])
        ol
        new
        id(ol)
        id(new)
        ####
        ol = [1,'a',3,'a',5,'a',6,'a']
        id(ol)
        rslt = replace_value_seqs(ol,'a','AAA',[0,1],mode="original")
        ol
        rslt
        id(ol)
        id(rslt)
    '''
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    indexes = indexes_seqs(ol,src_value,seqs)
    return(replace_indexes(ol,dst_value,indexes,mode=mode))