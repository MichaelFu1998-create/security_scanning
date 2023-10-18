def range_decompress(cl):
    '''
        #only support sorted-ints or sorted-ascii
        cl = [1, (5, 8), (13, 14), 18, (30, 34)]
        range_decompress(cl)
        cl = [1, (5, 8), (13, 14), 18, (30, 34), 40]
        range_decompress(cl)
        cl = [('a', 'd'), ('j', 'n'), 'u', ('y', 'z')]
        range_decompress(cl)
    '''
    def cond_func(ele):
        length = ele.__len__()
        cond = (length == 1)
        if(cond):
            return(ord(ele))
        else:
            x = ord(ele[0])
            y = ord(ele[1])
            return((x,y))
    if(type(cl[0])==type(0)):
        T = True
    elif(cl[0].__len__() == 1):
        T = (type(cl[0]) == type(0))
    else:
        T = (type(cl[0][0]) == type(0))
    if(T):
        l = cl 
    else:
        l = array_map(cl,cond_func)
    rslt = []
    for i in range(0,l.__len__()):
        ele = l[i]
        if(type(ele) == type(0)):
            arr = [ele]
        elif(ele.__len__() == 1):
            arr = [ele]
        else:
            sv = ele[0]
            ev = ele[1]
            arr = init_range(sv,ev+1,1)
        if(T):
            pass
        else:
            arr = array_map(arr,chr)
        rslt.extend(arr)
    return(rslt)