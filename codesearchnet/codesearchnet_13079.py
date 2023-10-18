def get_total(tots, node):
    """ get total number of quartets possible for a split"""
    if (node.is_leaf() or node.is_root()):
        return 0
    else:
        ## Get counts on down edges. 
        ## How to treat polytomies here?
        if len(node.children) > 2:
            down_r = node.children[0]
            down_l = node.children[1]
            for child in node.children[2:]:
                down_l += child
        else:
            down_r, down_l = node.children
        lendr = sum(1 for i in down_r.iter_leaves())
        lendl = sum(1 for i in down_l.iter_leaves())

        ## get count on up edge sister
        up_r = node.get_sisters()[0]
        lenur = sum(1 for i in up_r.iter_leaves())

        ## everyone else
        lenul = tots - (lendr + lendl + lenur)

        ## return product
        return lendr * lendl * lenur * lenul