def fullfill_descendants_info(desc_matrix):
    '''
       flat_offset
    '''
    pathloc_mapping = {}
    locpath_mapping = {}
    #def leaf_handler(desc,pdesc,offset):
    def leaf_handler(desc,pdesc):
        #desc['flat_offset'] = (offset,offset+1)
        desc['non_leaf_son_paths'] = []
        desc['leaf_son_paths'] = []
        desc['non_leaf_descendant_paths'] = []
        desc['leaf_descendant_paths'] = []
        desc['flat_len'] = 1
        if(pdesc['flat_len']):
            pdesc['flat_len'] = pdesc['flat_len'] + 1
        else:
            pdesc['flat_len'] = 1
    #def non_leaf_handler(desc,pdesc,offset):
    def non_leaf_handler(desc,pdesc):
        #desc['flat_offset'] = (offset,offset+desc['flat_len'])
        pdesc['non_leaf_descendant_paths'].extend(copy.deepcopy(desc['non_leaf_descendant_paths']))
        pdesc['leaf_descendant_paths'].extend(copy.deepcopy(desc['leaf_descendant_paths']))
        if(pdesc['flat_len']):
            pdesc['flat_len'] = pdesc['flat_len'] + desc['flat_len']
        else:
            pdesc['flat_len'] = desc['flat_len']
    def fill_path_mapping(desc):
        pmk = tuple(desc['path'])
        pmv = tuple(DescMatrix.loc(desc))
        pathloc_mapping[pmk] = pmv
        locpath_mapping[pmv] = pmk
    dm = DescMatrix(desc_matrix)
    depth = desc_matrix.__len__()
    desc_level = desc_matrix[depth - 1]
    length = desc_level.__len__()
    #the last level
    #offset = 0
    for j in range(length - 1,-1,-1):
        desc = desc_level[j]
        fill_path_mapping(desc)
        pdesc = dm.pdesc(desc)
        leaf_handler(desc,pdesc)
        #leaf_handler(desc,pdesc,offset)
        #offset = offset + 1
    for i in range(depth-2,0,-1):
        #offset = 0
        desc_level = desc_matrix[i]
        length = desc_level.__len__()
        for j in range(length-1,-1,-1):
            desc = desc_level[j]
            fill_path_mapping(desc)
            pdesc = dm.pdesc(desc)
            if(desc['leaf']):
                leaf_handler(desc,pdesc)
                #leaf_handler(desc,pdesc,offset)
                #offset = offset + 1
            else:
                non_leaf_handler(desc,pdesc)
                #non_leaf_handler(desc,pdesc,offset)
                #offset = offset + desc['flat_len']
    desc_matrix[0][0]['flat_offset'] = (0,desc_matrix[0][0]['flat_len'])
    for i in range(0,depth-1):
        pdesc_level = desc_matrix[i]
        length = pdesc_level.__len__()
        for j in range(0,length):
            pdesc = pdesc_level[j]
            si = pdesc['flat_offset'][0]
            for i in range(0,pdesc['sons_count']):
                spl = append(pdesc['path'],i,mode='new')
                pk = tuple(spl)
                locx,locy = pathloc_mapping[pk]
                son = desc_matrix[locx][locy]
                ei = si + son['flat_len']
                son['flat_offset'] = (si,ei)
                si = ei
    return(desc_matrix,pathloc_mapping,locpath_mapping)