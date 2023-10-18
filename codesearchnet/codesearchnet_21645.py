def seqs_continuous_indexesnot_slices(ol,value,seqs):
    '''
        from elist.elist import *
        ol = [1,"a","a",2,3,"a",4,"a","a","a",5]
        seqs_continuous_indexesnot_slices(ol,"a",{0,2})
    '''
    rslt = []
    length = ol.__len__()
    seq = -1
    cursor = 0
    begin = None
    slice = []
    while(cursor < length):
        cond1 = not(ol[cursor] == value)
        cond2 = (begin == None)
        if(cond1 & cond2):
            begin = cursor
            slice.append(cursor)
        elif(cond1 & (not(cond2))):
            slice.append(cursor)
        elif((not(cond1)) & (not(cond2))):
            seq = seq + 1
            if(seq in seqs):
                rslt.append(slice)
            else:
                pass
            begin = None
            slice = []
        else:
            pass
        cursor = cursor + 1
    if(slice):
        seq = seq + 1
        if(seq in seqs):
            rslt.append(slice)
        else:
            pass
    else:
        pass
    return(rslt)