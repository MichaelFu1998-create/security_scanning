def update_desc_lsib_path(desc):
    '''
        leftSibling
        previousSibling
        leftSib
        prevSib
        lsib
        psib
        
        have the same parent,and on the left
    '''
    if(desc['sib_seq']>0):
        lsib_path = copy.deepcopy(desc['path'])
        lsib_path[-1] = desc['sib_seq']-1
        desc['lsib_path'] = lsib_path
    else:
        pass
    return(desc)