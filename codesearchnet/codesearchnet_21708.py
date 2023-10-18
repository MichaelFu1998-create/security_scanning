def range_compress(ol):
    '''
        #only support sorted-ints or sorted-ascii
        l = [1,5,6,7,8,13,14,18,30,31,32,33,34]
        range_compress(l)
        l = [1,5,6,7,8,13,14,18,30,31,32,33,34,40]
        range_compress(l)
        l = ['a','b','c','d','j','k','l','m','n','u','y','z']
        range_compress(l)
    '''
    T = (type(ol[0]) == type(0))
    if(T):
        l = ol
    else:
        l = array_map(ol,ord)
    length = l.__len__()
    secs = []
    si = 0
    ei = 0
    prev = l[0]
    for i in range(1,length):
        curr = l[i]
        cond = (curr == (prev+1))
        if(cond):
            ei = i
            prev = curr
        else:
            if(T):
                sec = (l[si],l[ei])
            else:
                sec = (ol[si],ol[ei])
            if(si == ei):
                sec = sec[0]
            else:
                pass
            secs.append(sec)
            si = i
            ei = i 
            prev = curr
    if(T):
        sec = (l[si],l[ei])
    else:
        sec = (ol[si],ol[ei])
    if(si == ei):
        sec = sec[0]
    else:
        pass
    secs.append(sec)
    return(secs)