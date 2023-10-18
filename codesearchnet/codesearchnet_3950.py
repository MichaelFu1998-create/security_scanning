def SHD(target, pred, double_for_anticausal=True):
    r"""Compute the Structural Hamming Distance.
    
    The Structural Hamming Distance (SHD) is a standard distance to compare
    graphs by their adjacency matrix. It consists in computing the difference
    between the two (binary) adjacency matrixes: every edge that is either 
    missing or not in the target graph is counted as a mistake. Note that 
    for directed graph, two mistakes can be counted as the edge in the wrong
    direction is false and the edge in the good direction is missing ; the 
    `double_for_anticausal` argument accounts for this remark. Setting it to 
    `False` will count this as a single mistake.

    Args:
        target (numpy.ndarray or networkx.DiGraph): Target graph, must be of 
            ones and zeros.
        prediction (numpy.ndarray or networkx.DiGraph): Prediction made by the
            algorithm to evaluate.
        double_for_anticausal (bool): Count the badly oriented edges as two 
            mistakes. Default: True
 
    Returns:
        int: Structural Hamming Distance (int).

            The value tends to zero as the graphs tend to be identical.
        
    Examples:
        >>> from numpy.random import randint
        >>> tar, pred = randint(2, size=(10, 10)), randint(2, size=(10, 10))
        >>> SHD(tar, pred, double_for_anticausal=False) 
    """
    true_labels = retrieve_adjacency_matrix(target)
    predictions = retrieve_adjacency_matrix(pred, target.nodes() 
                                            if isinstance(target, nx.DiGraph) else None)
    
    diff = np.abs(true_labels - predictions)
    if double_for_anticausal:
        return np.sum(diff)
    else:
        diff = diff + diff.transpose()
        diff[diff > 1] = 1  # Ignoring the double edges.
        return np.sum(diff)/2