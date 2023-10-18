def find_seqs(ol,seqs,test_func,*args):
    '''
        from elist.elist import *
        def test_func(ele,x):
            cond = (ele > x)
            return(cond)
        
        ol = [1,2,3,4,5,6,7]
        some = find_seqs(ol,[0,3],test_func,3)
        some
        some = find_some(ol,[0,1,2],test_func,3)
        some
        #find_some is the same as find_seqs
    '''
    rslt =[]
    seqs = list(seqs)
    length = ol.__len__()
    seq = -1
    for i in range(0,length):
        cond = test_func(ol[i],*args)
        if(cond):
            seq = seq + 1
            if(seq in seqs):
                rslt.append({'index':i,'value':ol[i]})
            else:
                pass
        else:
            pass
    return(rslt)