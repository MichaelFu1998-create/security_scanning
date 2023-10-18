def new_ele_description(**kwargs):
    '''
        from elist.elist import *
        from elist.jprint import pobj
        root_desc = new_ele_description(leaf=False,depth=0,breadth_path=[],path=[],parent_path=[],parent_breadth_path=[])
        pobj(root_desc)
        #None means not handled
    '''
    desc = {
        'leaf':None,
        'depth':None,
        'breadth':None,
        'breadth_path':None,
        'sib_seq':None,
        'path':None,
        'parent_path':None,
        'parent_breadth_path':None,
        'lsib_path':None,
        'rsib_path':None,
        'lcin_path':None,
        'rcin_path':None,
        'sons_count':None,
        'leaf_son_paths':None,
        'non_leaf_son_paths':None,
        'leaf_descendant_paths':None,
        'non_leaf_descendant_paths':None,
        'flat_offset':None,
        'flat_len':None
    }
    for key in kwargs:
        desc[key.lower()] = kwargs[key]
    return(desc)