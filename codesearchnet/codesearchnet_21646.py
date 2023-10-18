def all_continuous_indexes_slices(ol,value):
    '''
        from elist.elist import *
        ol = [1,"a","a",2,3,"a",4,"a","a","a",5]
        all_continuous_indexes_slices(ol,"a")
    '''
    rslt = []
    length = ol.__len__()
    cursor = 0
    begin = None
    slice = []
    while(cursor < length):
        cond1 = (ol[cursor] == value)
        cond2 = (begin == None)
        if(cond1 & cond2):
            begin = cursor
            slice.append(cursor)
        elif(cond1 & (not(cond2))):
            slice.append(cursor)
        elif((not(cond1)) & (not(cond2))):
            rslt.append(slice)
            begin = None
            slice = []
        else:
            pass
        cursor = cursor + 1
    if(slice):
        rslt.append(slice)
    else:
        pass
    return(rslt)