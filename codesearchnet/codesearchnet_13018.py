def _decompose_tree(ttree, orient='right', use_edge_lengths=True): 
    """ decomposes tree into component parts for plotting """

    ## set attributes
    ttree._orient = orient
    ttree._use_edge_lengths = use_edge_lengths
    ult = use_edge_lengths == False

    ## map numeric values to internal nodes from root to tips
    names = {}
    idx = 0
    for node in ttree.tree.traverse("preorder"):
        if not node.is_leaf():
            if node.name:
                names[idx] = node.name
            else:
                names[idx] = idx
                node.name = str(idx)
            node.idx = idx
            idx += 1
            
    ## map number to the tips, these will be the highest numbers
    for node in ttree.tree.get_leaves(): 
        names[idx] = node.name
        node.idx = idx
        idx += 1

    ## create empty edges and coords arrays
    ttree.node_labels = names
    ttree.tip_labels = ttree.tree.get_leaf_names()
    #self.tip_labels = self.tree.get_leaf_names()[::-1]
    #self.node_labels = self.names
    ttree.edges = np.zeros((idx - 1, 2), dtype=int)
    ttree.verts = np.zeros((idx, 2), dtype=float)
    ttree._lines = []        # np.zeros((ntips-1), dtype=int)
    ttree._coords = []       # np.zeros((idx * 2 - ntips), dtype=float)

    ## postorder: first children and then parents. This moves up the list .
    nidx = 0
    tip_num = len(ttree.tree.get_leaves()) - 1
    
    ## tips to root to fill in the verts and edges
    for node in ttree.tree.traverse("postorder"):
        if node.is_leaf():
            ## set the xy-axis positions of the tips
            node.y = ttree.tree.get_distance(node)
            if ult:
                node.y = 0. 
            node.x = tip_num
            tip_num -= 1
            
            ## edges connect this vert to
            ttree.verts[node.idx] = [node.x, node.y]
            ttree.edges[nidx] = [node.up.idx, node.idx]

        elif node.is_root():
            node.y = ttree.tree.get_distance(node)
            if ult:
                node.y = -1 * node.get_farthest_leaf(True)[1] - 1
            node.x = sum(i.x for i in node.children) / float(len(node.children))
            ttree.verts[node.idx] = [node.x, node.y]
        
        else:
            ## create new nodes left and right
            node.y = ttree.tree.get_distance(node)
            if ult:
                node.y = -1 * node.get_farthest_leaf(True)[1] - 1
            node.x = sum(i.x for i in node.children) / float(len(node.children))
            ttree.edges[nidx, :] = [node.up.idx, node.idx]
            ttree.verts[node.idx] = [node.x, node.y]
        nidx += 1
        
    ## root to tips to fill in the coords and lines
    cidx = 0
    for node in ttree.tree.traverse():
        ## add yourself
        if not node.is_leaf():
            ttree._coords += [[node.x, node.y]]
            pidx = cidx
            cidx += 1
            for child in node.children:
                ## add children
                ttree._coords += [[child.x, node.y], [child.x, child.y]]
                ttree._lines += [[pidx, cidx]]    ## connect yourself to newx
                ttree._lines += [[cidx, cidx+1]]  ## connect newx to child
                cidx += 2
    ttree._coords = np.array(ttree._coords, dtype=float)
    ttree._lines = np.array(ttree._lines, dtype=int)

    ## invert for sideways trees
    if ttree._orient in ['up', 0]:
        pass
    if ttree._orient in ['left', 1]:
        ttree.verts[:, 1] = ttree.verts[:, 1] * -1
        ttree.verts = ttree.verts[:, [1, 0]]
        ttree._coords[:, 1] = ttree._coords[:, 1] * -1
        ttree._coords = ttree._coords[:, [1, 0]]
    if ttree._orient in ['down', 0]:
        ttree.verts[:, 1] = ttree.verts[:, 1] * -1
        ttree._coords[:, 1] = ttree._coords[:, 1] * -1
    if ttree._orient in ['right', 3]:
        ttree.verts = ttree.verts[:, [1, 0]]
        ttree._coords = ttree._coords[:, [1, 0]]