def concat(*arrays):
    '''
        from elist.elist import *
        l1 = [1,2,3]
        l2 = ["a","b","c"]
        l3 = [100,200]
        id(l1)
        id(l2)
        id(l3)
        arrays = [l1,l2,l3]
        new = concat(arrays)
        new
        id(new)
    '''
    new = []
    length = arrays.__len__()
    for i in range(0,length):
        array = copy.deepcopy(arrays[i])
        new.extend(array)
    return(new)