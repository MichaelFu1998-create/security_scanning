def build_trees(fclade_counts, namedict):
    """ 
    A subfunc of consensus_tree(). Build an unrooted consensus tree 
    from filtered clade counts. 
    """

    ## storage
    nodes = {}
    idxarr = np.arange(len(fclade_counts[0][0]))
    queue = []

    ## create dict of clade counts and set keys
    countdict = defaultdict(int)
    for clade, count in fclade_counts:
        mask = np.int_(list(clade)).astype(np.bool)
        ccx = idxarr[mask]
        queue.append((len(ccx), frozenset(ccx)))
        countdict[frozenset(ccx)] = count

    while queue:
        queue.sort()
        (clade_size, clade) = queue.pop(0)
        new_queue = []
    
        # search for ancestors of clade
        for (_, ancestor) in queue:
            if clade.issubset(ancestor):
                # update ancestor such that, in the following example:
                # ancestor == {1, 2, 3, 4}
                # clade == {2, 3}
                # new_ancestor == {1, {2, 3}, 4}
                new_ancestor = (ancestor - clade) | frozenset([clade])          
                countdict[new_ancestor] = countdict.pop(ancestor)
                ancestor = new_ancestor
            
            new_queue.append((len(ancestor), ancestor))
   
        # if the clade is a tip, then we have a name
        if clade_size == 1:
            name = list(clade)[0]
            name = namedict[name]
        else:
            name = None 
        
        # the clade will not be in nodes if it is a tip
        children = [nodes.pop(c) for c in clade if c in nodes]
        node = ete3.Tree(name=name)    
        #node = toytree.tree(name=name).tree
        for child in children:
            node.add_child(child)
        if not node.is_leaf():
            node.dist = int(round(100*countdict[clade]))
            node.support = int(round(100*countdict[clade]))
        else:
            node.dist = int(100) 
            node.support = int(100)
        
        nodes[clade] = node
        queue = new_queue
    tre = nodes.values()[0]
    tre.unroot()
    ## return the tree and other trees if present
    return tre, list(nodes.values())