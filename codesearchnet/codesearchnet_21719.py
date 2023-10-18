def init_desc_matrix(l):
    '''
        from elist.elist import *
        from elist.jprint import pobj
        l = [1,[4],2,[3,[5,6]]]
        desc_matrix = init_desc_matrix(l)
        pobj(desc_matrix)
    '''
    leaf = is_leaf(l)
    root_desc = new_ele_description(leaf=leaf,depth=0,breadth_path=[],path=[],parent_path=[],parent_breadth_path=[])
    if(leaf):
        root_desc['sons_count'] = 0
    else:
        pass
    desc_matrix = [
        [root_desc]
    ]
    return(desc_matrix)