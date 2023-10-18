def _init_unhandled(l,inited_matrix):
    '''
        from elist.elist import *
        from elist.jprint import pobj
        l = [1,[4],2,[3,[5,6]]]
        desc_matrix = init_desc_matrix(l)
        unhandled = _init_unhandled(l,desc_matrix)
        unhandled_data = unhandled['data']
        unhandled_desc = unhandled['desc']
        unhandled_data[0]
        unhandled_desc[0]
        unhandled_data[1]
        unhandled_desc[1]
    '''
    root_desc = inited_matrix[0][0]
    unhandled = {'data':[],'desc':[]}
    length = l.__len__()
    root_desc['sons_count'] = length
    root_desc['leaf_son_paths'] = []
    root_desc['non_leaf_son_paths'] = []    
    if(length == 0):
        pass
    else:
        inited_matrix.append([])
        level = inited_matrix[1]
        for i in range(0,length):
            child = l[i]
            desc = copy.deepcopy(root_desc)
            desc = reset_parent_desc_template(desc)
            desc['depth'] = 1
            desc['breadth'] = i
            desc['parent_breadth_path'] = copy.deepcopy(desc['breadth_path'])
            desc['breadth_path'].append(i)
            desc['sib_seq'] = i
            desc['parent_path'] = copy.deepcopy(desc['path'])
            desc['path'].append(i)
            if(i==0):
                pass
            else:
                desc['lsib_path'] = [i-1]
            if(i == (length - 1)):
                pass
            else:
                desc['rsib_path'] = [i+1]
            if(is_leaf(child)):
                desc['leaf'] = True
                desc['sons_count'] = 0
                root_desc['leaf_son_paths'].append(copy.deepcopy(desc['path']))
            else:
                desc['leaf'] = False
                root_desc['non_leaf_son_paths'].append(copy.deepcopy(desc['path']))
                unhandled['data'].append(child)
                unhandled['desc'].append(desc)
            level.append(desc)
    return(unhandled)