def value_indexes_mapping(l):
    '''
        from elist.elist import *
        from elist.jprint import pobj
        l = ['a','b','b','a','c','b']
        desc = value_indexes_mapping(l)
        pobj(desc)
    '''
    pt = copy.deepcopy(l)
    desc = {}
    vset = set({})
    for v in pt:
        vset.add(v)
    for v in vset:
        desc[v] = []
    for i in range(0,l.__len__()):
        desc[l[i]].append(i)
    return(desc)