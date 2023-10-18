def value_interval(ol,value):
    '''
        ol = [0, 4, 6, 8, 10, 14]
        value_interval(ol,-1)
        value_interval(ol,1)
        value_interval(ol,2)
        value_interval(ol,3)
        value_interval(ol,4)
        value_interval(ol,9)
        value_interval(ol,14)
        value_interval(ol,17)
    '''
    si,ei = where(ol,value)
    if(si == None):
        sv = None
    else:
        sv = ol[si]
    if(ei == None):
        ev = None
    else:
        ev = ol[ei]
    return((sv,ev))