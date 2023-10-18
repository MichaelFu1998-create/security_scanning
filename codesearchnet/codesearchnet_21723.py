def update_desc_lcin_path(desc,pdesc_level):
    '''
        leftCousin
        previousCousin
        leftCin
        prevCin
        lcin
        pcin
        
        parents are neighbors,and on the left
    '''
    parent_breadth = desc['parent_breadth_path'][-1]
    if(desc['sib_seq']==0):
        if(parent_breadth==0):
            pass
        else:
            parent_lsib_breadth = parent_breadth - 1
            plsib_desc = pdesc_level[parent_lsib_breadth]
            if(plsib_desc['leaf']):
                pass
            else:
                lcin_path = copy.deepcopy(plsib_desc['path'])
                lcin_path.append(plsib_desc['sons_count'] - 1)
                desc['lcin_path'] = lcin_path
    else:
        pass
    return(desc)