def interleave(*arrays,**kwargs):
    '''
        arr1 = [1,2,3,4]
        arr2 = ['a','b','c','d']
        arr3 = ['@','#','%','*']
        interleave(arr1,arr2,arr3)
    '''
    anum = arrays.__len__()
    rslt = []
    length = arrays[0].__len__()
    for j in range(0,length):
        for i in range(0,anum):
            array = arrays[i]
            rslt.append(array[j])
    return(rslt)