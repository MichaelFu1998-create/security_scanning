def reduce_left(ol,callback,initialValue):
    '''
        from elist.elist import *
        def callback(accumulator,currentValue):
            accumulator.append(currentValue[0])
            accumulator.append(currentValue[1])
            return(accumulator)
        
        ol = [(1,2),("a","b"),("x","y")]
        reduce_left(ol,callback,[])
        #array_reduce, reduceLeft ,reduce_left  are the same
    '''
    length = ol.__len__()
    accumulator = initialValue
    for i in range(0,length):
        accumulator = callback(accumulator,ol[i])
    return(accumulator)