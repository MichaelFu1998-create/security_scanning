def same_indexes(l1,l2):
    '''
        from elist.elist import *
        l1 = [1,2,3,5]
        l2 = [0,2,3,4]
        same_indexes(l1,l2)
    '''
    rslt = []
    for i in range(0,l1.__len__()):
        if(l1[i]==l2[i]):
            rslt.append(i)
    return(rslt)