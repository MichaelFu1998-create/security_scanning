def update_desc_rsib_path(desc,sibs_len):
    '''
        rightSibling
        nextSibling
        rightSib
        nextSib
        rsib
        nsib
        
        have the same parent,and on the right
    '''
    if(desc['sib_seq']<(sibs_len-1)):
        rsib_path = copy.deepcopy(desc['path'])
        rsib_path[-1] = desc['sib_seq']+1
        desc['rsib_path'] = rsib_path
    else:
        pass
    return(desc)