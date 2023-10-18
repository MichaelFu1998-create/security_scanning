def select_seqs(ol,seqs):
    '''
        from elist.elist import *
        ol = ['a','b','c','d']
        select_seqs(ol,[1,2])
    '''
    rslt =copy.deepcopy(ol)
    rslt = itemgetter(*seqs)(ol)
    if(seqs.__len__()==0):
        rslt = []
    elif(seqs.__len__()==1):
        rslt = [rslt]
    else:
        rslt = list(rslt)
    return(rslt)