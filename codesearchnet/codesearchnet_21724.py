def update_desc_rcin_path(desc,sibs_len,pdesc_level):
    '''
        rightCousin
        nextCousin
        rightCin
        nextCin
        rcin
        ncin
        
        parents are neighbors,and on the right
    '''
    psibs_len = pdesc_level.__len__()
    parent_breadth = desc['parent_breadth_path'][-1]
    if(desc['sib_seq']==(sibs_len - 1)):
        if(parent_breadth==(psibs_len -1)):
            pass
        else:
            parent_rsib_breadth = parent_breadth + 1
            prsib_desc = pdesc_level[parent_rsib_breadth]
            #because from left to right to handle each level
            #sons_count will only be updated in the next-round 
            if(prsib_desc['leaf']):
                pass
            else:
                rcin_path = copy.deepcopy(prsib_desc['path'])
                rcin_path.append(0)
                desc['rcin_path'] = rcin_path
    else:
        pass
    return(desc)