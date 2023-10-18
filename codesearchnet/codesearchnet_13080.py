def get_sampled(data, totn, node):
    """ get total number of quartets sampled for a split"""
    ## convert tip names to ints
    names = sorted(totn)
    cdict = {name: idx for idx, name in enumerate(names)}
    
    ## skip some nodes
    if (node.is_leaf() or node.is_root()):
        return 0
    else:
        ## get counts on down edges
        if len(node.children) > 2:
            down_r = node.children[0]
            down_l = node.children[1]
            for child in node.children[2:]:
                down_l += child
        else:
            down_r, down_l = node.children

        lendr = set(cdict[i] for i in down_r.get_leaf_names())
        lendl = set(cdict[i] for i in down_l.get_leaf_names())

        ## get count on up edge sister
        up_r = node.get_sisters()[0]
        lenur = set(cdict[i] for i in up_r.get_leaf_names())

        ## everyone else
        lenul = set(cdict[i] for i in totn) - set.union(lendr, lendl, lenur)

    idx = 0
    sampled = 0
    with h5py.File(data.database.output, 'r') as io5:
        end = io5["quartets"].shape[0]
        while 1:
            ## break condition
            if idx >= end:
                break

            ## counts matches
            qrts = io5["quartets"][idx:idx+data._chunksize]
            for qrt in qrts:
                sqrt = set(qrt)
                if all([sqrt.intersection(i) for i in [lendr, lendl, lenur, lenul]]):
                    sampled += 1

            ## increase span
            idx += data._chunksize
    return sampled