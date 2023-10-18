def insert_sections_some(ol,*secs,**kwargs):
    '''
        ol = initRange(0,20,1)
        ol
        loc = 6
        rslt = insert_sections_some(ol,['a','a','a'],['c','c','c','c'],index=loc)
        rslt
        ####
    '''
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    loc = kwargs['index']
    secs = list(secs)
    secs = [concat(*secs)]
    locs = [loc]
    return(insert_sections_many(ol,secs,locs,mode=mode))