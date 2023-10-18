def insert_section(ol,sec,loc,**kwargs):
    '''
        ol = initRange(0,20,1)
        ol
        loc = 6
        sec = ['a','b','c','d']
        rslt = insert_section(ol,sec,loc)
        rslt
        ####
    '''
    if('mode' in kwargs):
        mode = kwargs["mode"]
    else:
        mode = "new"
    secs = [sec]
    locs = [loc]
    return(insert_sections_many(ol,secs,locs,mode=mode))