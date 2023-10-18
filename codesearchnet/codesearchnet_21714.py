def where(ol,value):
    '''
        ol = [0, 4, 6, 8, 10, 14]
        where(ol,-1)
        where(ol,1)
        where(ol,2)
        where(ol,3)
        where(ol,4)
        where(ol,9)
        where(ol,14)
        where(ol,17)
    '''
    si = None
    ei = None
    for i in range(0,ol.__len__()):
        ele = ol[i]
        if(value >ele):
            si = i 
        elif(value == ele):
            return((i,i))
        else:
            ei = i 
            return((si,ei))
    return((si,ei))