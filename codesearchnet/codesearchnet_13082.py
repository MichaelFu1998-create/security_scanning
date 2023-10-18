def find_clades(trees, names):
    """ 
    A subfunc of consensus_tree(). Traverses trees to count clade occurrences.
    Names are ordered by names, else they are in the order of the first
    tree. 
    """
    ## index names from the first tree
    if not names:
        names = trees[0].get_leaf_names()
    ndict = {j:i for i, j in enumerate(names)}
    namedict = {i:j for i, j in enumerate(names)}

    ## store counts
    clade_counts = defaultdict(int)
    ## count as bitarray clades in each tree
    for tree in trees:
        tree.unroot()
        for node in tree.traverse('postorder'):
            #bits = bitarray('0'*len(tree))
            bits = np.zeros(len(tree), dtype=np.bool_)
            for child in node.iter_leaf_names():
                bits[ndict[child]] = True
            ## if parent is root then mirror flip one child (where bit[0]=0)
            # if not node.is_root():
            #     if node.up.is_root():
            #         if bits[0]:
            #             bits.invert()
            bitstring = "".join([np.binary_repr(i) for i in bits])
            clade_counts[bitstring] += 1

    ## convert to freq
    for key, val in clade_counts.items():
        clade_counts[key] = val / float(len(trees))

    ## return in sorted order
    clade_counts = sorted(clade_counts.items(), 
                          key=lambda x: x[1],
                          reverse=True)
    return namedict, clade_counts