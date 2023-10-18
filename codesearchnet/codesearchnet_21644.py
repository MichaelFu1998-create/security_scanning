def which_continuous_indexes_slice(ol,value,which):
    '''
        from elist.elist import *
        ol = [1,"a","a",2,3,"a",4,"a","a","a",5]
        which_continuous_indexes_slice(ol,"a",0)
        which_continuous_indexes_slice(ol,"a",1)
        which_continuous_indexes_slice(ol,"a",2)
        which_continuous_indexes_slice(ol,"a",3)
        which_continuous_indexes_slice(ol,"b",0)
    '''
    length = ol.__len__()
    seq = -1
    cursor = 0
    begin = None
    slice = []
    while(cursor < length):
        cond1 = (ol[cursor] == value)
        cond2 = (begin == None)
        if(cond1 & cond2):
            begin = cursor
            slice.append(cursor)
            cursor = cursor + 1
        elif(cond1 & (not(cond2))):
            slice.append(cursor)
            cursor = cursor + 1
        elif((not(cond1)) & (not(cond2))):
            seq = seq + 1
            if(seq == which):
                return(slice)
            else:
                cursor = cursor + 1
                begin = None
                slice = []
        else:
            cursor = cursor + 1
    if(slice):
        seq = seq + 1
    else:
        pass
    if(seq == which):
        return(slice)
    else:
        return([])