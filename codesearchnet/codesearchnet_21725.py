def scan(l,**kwargs):
    '''
        from elist.elist import *
        from elist.jprint import pobj
        l = [1,[4],2,[3,[5,6]]]
        desc = description(l)
        l = [1,2,[4],[3,[5,6]]]
        desc = description(l)
    '''
    if('itermode' in kwargs):
        itermode = True
    else:
        itermode = False
    ####level ==  0
    desc_matrix = init_desc_matrix(l)
    if(desc_matrix[0][0]['leaf'] == True):
        return(desc_matrix)
    else:
        pass
    ####cache
    lcache=LevelCache(datas=l,descs=desc_matrix[0][0])
    scache=StateCache(desc_matrix)
    pcache = init_pcache_handler_inline(kwargs)
    ####level > 0
    while(lcache.data.__len__() > 0):
        #add next desc_level 
        scache.update()
        for unhandled_seq in range(0,lcache.data.__len__()):
            #handle parent
            pcache.update_pdesc(lcache,unhandled_seq)
            for sib_seq in range(0,pcache.sibs_len):
                #handle child
                pcache.update_desc(lcache,scache,sib_seq)
        #update level lcache
        lcache.update()
    return(desc_matrix)