def rand_sub(arr,*args,**kwargs):
    '''
        arr = ['scheme', 'username', 'password', 'hostname', 'port', 'path', 'params', 'query', 'fragment']
        rand_sub(arr,3)
        rand_sub(arr,3)
        rand_sub(arr,3)
        rand_sub(arr)
        rand_sub(arr)
        rand_sub(arr)
    '''
    arr = copy.deepcopy(arr)
    lngth = arr.__len__()
    args = list(args)
    if(args.__len__() == 0):
        n = random.randrange(0,lngth)
    else:
        n = args[0]
        if(n>lngth):
            n = lngth
        else:
            pass
    indexes = rand_some_indexes(0,lngth,n,**kwargs)
    narr = select_seqs_keep_order(arr,indexes)
    return(narr)