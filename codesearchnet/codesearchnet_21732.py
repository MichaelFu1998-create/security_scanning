def get_wfsmat(l):
    '''
       l = ['v_7', 'v_3', 'v_1', 'v_4', ['v_4', 'v_2'], 'v_5', 'v_6', 'v_1', 'v_6', 'v_7', 'v_5', ['v_4', ['v_1', 'v_8', 'v_3', 'v_4', 'v_2', 'v_7', [['v_3', 'v_2'], 'v_4', 'v_5', 'v_1', 'v_3', 'v_1', 'v_2', 'v_5', 'v_8', 'v_8', 'v_7'], 'v_5', 'v_8', 'v_7', 'v_1', 'v_5'], 'v_6'], 'v_4', 'v_5', 'v_8', 'v_5']
       get_wfs(l)
    '''
    ltree = ListTree(l)
    vdescmat = ltree.desc
    wfsmat = matrix_map(vdescmat,lambda v,ix,iy:v['path'])
    wfsmat.pop(0)
    return(wfsmat)